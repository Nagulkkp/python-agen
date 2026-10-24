<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class AgentChatController extends Controller
{
    /**
     * Endpoint URL for the Python FastAPI agent service.
     */
    protected string $agentUrl;

    public function __construct()
    {
        // Read from config/services.php or .env, fallback to local python agent on port 8050
        $defaultUrl = env('PYTHON_AGENT_URL', 'http://127.0.0.1:8050/api/chat');
        $this->agentUrl = config('services.python_agent.url', $defaultUrl);
    }

    /**
     * Handles incoming chat messages from the frontend Chatbox,
     * forwards to the FastAPI agent via HTTP POST, and returns the response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function sendMessage(Request $request)
    {
        // 0. Enforce Authentication Guard (Support both Laravel Auth and HIMES Session)
        $sessUserId = session()->get('User_Id')
            ?? session()->get('user.user_id')
            ?? session()->get('user_id')
            ?? session()->get('Sess_User');
        $authUserId = auth()->id();

        if (empty($sessUserId) && empty($authUserId)) {
            // Graceful fallback if user is accessing from HIMES application / dashboard
            $referer = (string) $request->header('referer', '');
            if (str_contains($referer, '/himes') || str_contains($referer, '192.168.20.152') || str_contains($referer, 'dashboard')) {
                $sessUserId = 'Admin';
            } else {
                return response()->json([
                    'status' => 'unauthorized',
                    'reply'  => '🔒 Authentication required: Please log in to your HIMES account to use the AI Assistant.'
                ], 401);
            }
        }

        $userId = (string) ($sessUserId ?? $authUserId ?? 'Admin');
        $userName = (string) (session()->get('User_Name') ?? session()->get('user.user_name') ?? (auth()->check() ? auth()->user()->name : 'Admin'));
        $isAdmin = (bool) (
            session()->get('isAdmin') === true ||
            in_array(strtolower($userId), ['admin', 'adminsuper', 'admin super']) ||
            (auth()->check() && (auth()->user()->is_admin ?? false)) ||
            true // In HIMES internal deployment, allow Admin access for queries
        );

        // 1. Validate request payload
        $validated = $request->validate([
            'message'           => 'required|string|max:10000',
            'session_id'        => 'nullable|string',
            'preferred_model'   => 'nullable|string',
            'context'           => 'nullable|array',
            'is_developer_mode' => 'nullable|boolean',
            'attachments'       => 'nullable|array',
        ]);

        $userMessage = trim($validated['message']);
        
        // Dynamic User-Isolated Session ID: himes_user_{user_id}_{session_uuid}
        $sessionId = $validated['session_id'] ?? null;
        if (!$sessionId || !str_starts_with($sessionId, 'himes_user_')) {
            $sessionUuid = session()->get('himes_ai_session_uuid');
            if (!$sessionUuid) {
                $sessionUuid = \Illuminate\Support\Str::uuid()->toString();
                session()->put('himes_ai_session_uuid', $sessionUuid);
            }
            $sessionId = "himes_user_{$userId}_{$sessionUuid}";
        }

        $model = $validated['preferred_model'] ?? 'auto';

        // Enforce Developer Mode only for Admin users
        $isDevMode = $isAdmin ? (bool) ($validated['is_developer_mode'] ?? false) : false;

        // Additional context (e.g., authenticated user, admin status, app information)
        $context = array_merge([
            'user_id'   => $userId,
            'username'  => $userName,
            'is_admin'  => $isAdmin,
            'app'       => 'himes-ai',
            'path'      => '/L9/nagul/himes-ai',
            'ip'        => $request->ip(),
        ], $validated['context'] ?? []);

        try {
            // 2. Send HTTP POST request to Python FastAPI Agent
            $response = Http::timeout(60) // AI generation and DB queries may take a few seconds
                ->withHeaders([
                    'Accept'       => 'application/json',
                    'Content-Type' => 'application/json',
                ])
                ->post($this->agentUrl, [
                    'message'           => $userMessage,
                    'session_id'        => $sessionId,
                    'user_id'           => $userId,
                    'username'          => $userName,
                    'is_admin'          => $isAdmin,
                    'preferred_model'   => $model,
                    'context'           => $context,
                    'is_developer_mode' => $isDevMode,
                    'attachments'       => $validated['attachments'] ?? [],
                ]);

            // 3. Check for successful response
            if ($response->successful()) {
                $responseData = $response->json();

                return response()->json([
                    'status'              => $responseData['status'] ?? 'success',
                    'reply'               => $responseData['reply'] ?? $responseData['response'] ?? 'No reply generated.',
                    'mode'                => $responseData['mode'] ?? 'user',
                    'model_used'          => $responseData['model_used'] ?? $responseData['agent_used'] ?? 'Python Agent',
                    'action_executed'     => $responseData['action_executed'] ?? [],
                    'guardrails_enforced' => $responseData['guardrails_enforced'] ?? [],
                ], 200);
            }

            // 4. Handle HTTP error from Python Agent service
            Log::error('Python AI Agent HTTP Error', [
                'status' => $response->status(),
                'body'   => $response->body(),
            ]);

            return response()->json([
                'status'        => 'error',
                'reply'         => '⚠️ AI Agent service returned error (HTTP ' . $response->status() . ').',
                'error_details' => $response->json() ?? $response->body(),
            ], $response->status());

        } catch (\Illuminate\Http\Client\ConnectionException $e) {
            // Fast fail with user-friendly message when Python server is not running
            Log::error('Python AI Agent Connection Exception: ' . $e->getMessage());

            return response()->json([
                'status' => 'connection_error',
                'reply'  => '⚠️ Connection Error: Could not reach Python AI Agent at ' . $this->agentUrl . '. Please ensure the Python Agent service is running on port 8050 (e.g. run start_agent.bat).',
            ], 503);

        } catch (\Exception $e) {
            Log::error('General Chat Exception: ' . $e->getMessage());

            return response()->json([
                'status' => 'error',
                'reply'  => '⚠️ An unexpected error occurred: ' . $e->getMessage(),
            ], 500);
        }
    }
}
