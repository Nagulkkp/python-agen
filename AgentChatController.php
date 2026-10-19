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
        // Read from config/services.php or .env, fallback to default local port 8000
        $this->agentUrl = config('services.python_agent.url', env('PYTHON_AGENT_URL', 'http://127.0.0.1:8000/api/chat'));
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
        $sessionId   = $validated['session_id'] ?? session()->getId() ?? 'default_session';
        $model       = $validated['preferred_model'] ?? 'auto';

        // Additional context (e.g., authenticated user, app information)
        $context = array_merge([
            'user_id' => auth()->id() ?? 'guest',
            'app'     => 'himes',
            'ip'      => $request->ip(),
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
                    'preferred_model'   => $model,
                    'context'           => $context,
                    'is_developer_mode' => $validated['is_developer_mode'] ?? null,
                    'attachments'       => $validated['attachments'] ?? [],
                ]);

            // 3. Check for successful response
            if ($response->successful()) {
                $responseData = $response->json();

                return response()->json([
                    'status'              => $responseData['status'] ?? 'success',
                    'reply'               => $responseData['reply'] ?? 'No reply generated.',
                    'mode'                => $responseData['mode'] ?? 'user',
                    'model_used'          => $responseData['model_used'] ?? 'Python Agent',
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
                'reply'  => '⚠️ Connection Error: Could not reach Python AI Agent at ' . $this->agentUrl . '. Please ensure uvicorn is running on port 8000.',
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
