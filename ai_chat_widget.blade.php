<!-- HIMES AI Dev Assistant Floating Chat Widget with Full-Screen Modal, Multi-Media Attachments & Dual Mode System -->
@auth
@if(!request()->is('login') && !request()->is('*/login'))
@php
    $currentUser = Auth::user();
    $currentUserId = (string) (Auth::id() ?? 'guest');
    $currentUserName = $currentUser->name ?? $currentUser->username ?? $currentUser->User_Name ?? 'User';
    $isAdmin = (bool) ($currentUser->is_admin ?? ($currentUser->role === 'admin') ?? ($currentUser->user_type === 'admin') ?? false);
@endphp
<style>
  #himes-ai-widget {
    position: fixed;
    bottom: 25px;
    right: 25px;
    z-index: 9999999;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  #himes-ai-backdrop {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    z-index: 9999998;
    animation: himesFadeIn 0.2s ease-out;
  }
  #himes-ai-trigger {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.2);
  }
  #himes-ai-trigger:hover {
    transform: scale(1.08) translateY(-2px);
    box-shadow: 0 12px 30px rgba(79, 70, 229, 0.6);
  }
  #himes-ai-trigger svg {
    width: 30px;
    height: 30px;
    fill: currentColor;
  }
  #himes-ai-window {
    display: none;
    position: fixed;
    bottom: 100px;
    right: 25px;
    width: 450px;
    max-width: calc(100vw - 40px);
    height: 650px;
    max-height: calc(100vh - 130px);
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05);
    flex-direction: column;
    overflow: hidden;
    color: #e5e7eb;
    animation: himesAiSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    transition: width 0.3s ease, height 0.3s ease, transform 0.3s ease;
  }
  #himes-ai-window.maximized {
    top: 50% !important;
    left: 50% !important;
    bottom: auto !important;
    right: auto !important;
    transform: translate(-50%, -50%) !important;
    width: 90vw !important;
    max-width: 1250px !important;
    height: 88vh !important;
    max-height: 900px !important;
    border-radius: 18px !important;
    box-shadow: 0 35px 100px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.15) !important;
    z-index: 9999999;
  }
  @keyframes himesAiSlideUp {
    from { opacity: 0; transform: translateY(20px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  @keyframes himesFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  .himes-ai-header {
    padding: 14px 18px;
    background: #1f2937;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-shrink: 0;
  }
  .himes-ai-title-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .himes-ai-avatar {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
  }
  .himes-ai-title {
    font-weight: 700;
    font-size: 14.5px;
    color: #f9fafb;
    margin: 0;
  }
  .himes-ai-status {
    font-size: 11.5px;
    color: #10b981;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .himes-ai-dot {
    width: 7px;
    height: 7px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
  }
  .himes-ai-header-controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .himes-ai-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    user-select: none;
  }
  .himes-ai-mode-badge.user-mode {
    background: rgba(16, 185, 129, 0.15);
    border-color: rgba(16, 185, 129, 0.35);
    color: #34d399;
  }
  .himes-ai-mode-badge.user-mode:hover {
    background: rgba(16, 185, 129, 0.28);
    transform: translateY(-1px);
  }
  .himes-ai-mode-badge.dev-mode {
    background: rgba(139, 92, 246, 0.2);
    border-color: rgba(168, 85, 247, 0.45);
    color: #c084fc;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.25);
  }
  .himes-ai-mode-badge.dev-mode:hover {
    background: rgba(139, 92, 246, 0.35);
    transform: translateY(-1px);
  }
  .himes-ai-icon-btn {
    background: transparent;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }
  .himes-ai-icon-btn:hover {
    color: white;
    background: rgba(255, 255, 255, 0.1);
  }
  .himes-ai-close {
    background: transparent;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    font-size: 19px;
    padding: 3px 8px;
    border-radius: 6px;
    transition: all 0.2s;
  }
  .himes-ai-close:hover {
    color: white;
    background: rgba(255, 255, 255, 0.1);
  }
  .himes-ai-chips {
    padding: 10px 14px;
    display: flex;
    gap: 8px;
    overflow-x: auto;
    background: #182234;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    scrollbar-width: none;
    flex-shrink: 0;
  }
  .himes-ai-chips::-webkit-scrollbar { display: none; }
  .himes-ai-chip {
    white-space: nowrap;
    background: rgba(79, 70, 229, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    font-size: 12px;
    padding: 5px 12px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .himes-ai-chip:hover {
    background: rgba(79, 70, 229, 0.3);
    color: #ffffff;
    transform: translateY(-1px);
  }
  .himes-ai-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    position: relative;
  }
  .himes-ai-msg {
    max-width: 90%;
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 13.5px;
    line-height: 1.55;
    word-break: break-word;
  }
  .himes-ai-msg.user {
    align-self: flex-end;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: #ffffff;
    border-bottom-right-radius: 4px;
  }
  .himes-ai-msg.agent {
    align-self: flex-start;
    background: #1f2937;
    color: #e5e7eb;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom-left-radius: 4px;
  }
  /* Code Card Styling with Copy Button */
  .himes-code-card {
    margin: 10px 0;
    border-radius: 8px;
    border: 1px solid #30363d;
    background: #0d1117;
    overflow: hidden;
  }
  .himes-code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #161b22;
    padding: 6px 12px;
    border-bottom: 1px solid #30363d;
    font-size: 11px;
    color: #8b949e;
  }
  .himes-code-lang {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #58a6ff;
  }
  .himes-copy-btn {
    background: transparent;
    border: 1px solid #30363d;
    color: #c9d1d9;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: all 0.2s;
  }
  .himes-copy-btn:hover {
    background: #21262d;
    color: #ffffff;
    border-color: #8b949e;
  }
  .himes-ai-msg pre {
    background: transparent;
    padding: 10px 12px;
    margin: 0;
    overflow-x: auto;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 12px;
    color: #79c0ff;
    line-height: 1.45;
  }
  .himes-ai-msg code {
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 5px;
    border-radius: 4px;
    font-family: Consolas, Monaco, monospace;
    font-size: 12px;
    color: #93c5fd;
  }
  /* Status Alert Cards in User Mode */
  .himes-status-card {
    background: rgba(16, 185, 129, 0.1);
    border-left: 3px solid #10b981;
    padding: 8px 12px;
    margin: 8px 0;
    border-radius: 4px;
    font-size: 13px;
  }
  .himes-status-card.warning {
    background: rgba(245, 158, 11, 0.1);
    border-left-color: #f59e0b;
  }
  /* Attachment Preview Tray */
  .himes-ai-attachments-tray {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px 16px;
    background: #161f2e;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    max-height: 110px;
    overflow-y: auto;
    flex-shrink: 0;
  }
  .himes-att-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(79, 70, 229, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.35);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11.5px;
    color: #e0e7ff;
    max-width: 220px;
  }
  .himes-att-chip .himes-att-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .himes-att-chip .himes-att-del {
    background: transparent;
    border: none;
    color: #f87171;
    cursor: pointer;
    font-weight: bold;
    font-size: 13px;
    padding: 0 2px;
    line-height: 1;
  }
  .himes-att-chip .himes-att-del:hover {
    color: #ef4444;
  }
  /* Input Wrap */
  .himes-ai-input-wrap {
    padding: 10px 14px;
    background: #1f2937;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    gap: 8px;
    align-items: flex-end;
    flex-shrink: 0;
  }
  .himes-ai-input-actions {
    display: flex;
    gap: 4px;
    padding-bottom: 5px;
  }
  .himes-ai-attach-btn {
    background: transparent;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    padding: 6px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }
  .himes-ai-attach-btn:hover {
    color: #6366f1;
    background: rgba(99, 102, 241, 0.15);
  }
  .himes-ai-input {
    flex: 1;
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 9px 12px;
    color: white;
    font-size: 13.5px;
    outline: none;
    resize: none;
    line-height: 1.45;
    min-height: 38px;
    max-height: 120px;
    font-family: inherit;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .himes-ai-input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }
  .himes-ai-send-btn {
    background: #4f46e5;
    color: white;
    border: none;
    padding: 10px 14px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-bottom: 2px;
  }
  .himes-ai-send-btn:hover {
    background: #4338ca;
    transform: translateY(-1px);
  }
  .himes-ai-typing {
    display: none;
    align-self: flex-start;
    padding: 8px 14px;
    background: #1f2937;
    border-radius: 12px;
    font-size: 12px;
    color: #9ca3af;
    font-style: italic;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }
  /* Drag and Drop Overlay */
  .himes-ai-drop-overlay {
    display: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(17, 24, 39, 0.92);
    z-index: 50;
    align-items: center;
    justify-content: center;
    border: 2px dashed #6366f1;
    border-radius: 20px;
    pointer-events: none;
  }
  .himes-ai-drop-box {
    text-align: center;
    color: #c7d2fe;
  }
</style>

<!-- Full-Screen Modal Backdrop -->
<div id="himes-ai-backdrop" onclick="toggleHimesMaximize()"></div>

<div id="himes-ai-widget">
  <!-- Floating Button -->
  <div id="himes-ai-trigger" onclick="toggleHimesAi()" title="Open HIMES AI Assistant">
    <svg viewBox="0 0 24 24">
      <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5Z"/>
    </svg>
  </div>

  <!-- Chat Window -->
  <div id="himes-ai-window" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)">
    <!-- Drag & Drop Overlay -->
    <div id="himes-ai-drop-overlay" class="himes-ai-drop-overlay">
      <div class="himes-ai-drop-box">
        <div style="font-size: 34px; margin-bottom: 6px;">📂</div>
        <div style="font-weight: 700; font-size: 15px; color: #ffffff;">Drop Files to Attach</div>
        <div style="font-size: 12px; color: #a5b4fc; margin-top: 4px;">Images (.jpg, .png) & Documents (.pdf, .log, .txt, .json, .sql)</div>
      </div>
    </div>

    <!-- Header -->
    <div class="himes-ai-header">
      <div class="himes-ai-title-wrap">
        <div class="himes-ai-avatar">🤖</div>
        <div>
          <div class="himes-ai-title">HIMES AI Assistant</div>
          <div class="himes-ai-status"><span class="himes-ai-dot"></span> Autonomous Agent Active</div>
        </div>
      </div>
      <div class="himes-ai-header-controls">
        @if($isAdmin)
        <!-- Dual Mode Badge Toggle (Admin Only) -->
        <div id="himes-ai-mode-badge" class="himes-ai-mode-badge user-mode" onclick="toggleModeClick()" title="Click to toggle User View / Developer View">
          <span id="himes-mode-icon">👤</span>
          <span id="himes-mode-text">User View</span>
        </div>
        @endif
        <!-- Maximize / Popup Modal Button -->
        <button id="himes-ai-max-btn" class="himes-ai-icon-btn" onclick="toggleHimesMaximize()" title="Expand to Full Popup Modal">
          <svg id="himes-max-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M4 4h6v2H6v4H4V4zm10 0h6v6h-2V6h-4V4zM4 14h2v4h4v2H4v-6zm16 4h-4v2h6v-6h-2v4z"/>
          </svg>
          <svg id="himes-restore-icon" style="display:none;" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M4 8h4V4h2v6H4V8zm12-4h2v4h4v2h-6V4zM8 16H4v-2h6v6H8v-4zm8 4h-2v-6h6v2h-4v4z"/>
          </svg>
        </button>
        <!-- Close Button -->
        <button class="himes-ai-close" onclick="toggleHimesAi()" title="Minimize Chatbox">✕</button>
      </div>
    </div>

    <!-- Quick Action Chips -->
    <div class="himes-ai-chips">
      <div class="himes-ai-chip" onclick="quickTask('price list management menu enga iruku?')">💰 Price List Menu</div>
      <div class="himes-ai-chip" onclick="quickTask('Global View of OP Pharmacy screen-la records count evlo?')">💊 Pharmacy Records</div>
      <div class="himes-ai-chip" onclick="quickTask('Recent patient visits list kaattu')">📋 Patient Visits</div>
      <div class="himes-ai-chip" onclick="quickTask('Check server disk space, memory, and uptime')">🩺 System Health</div>
      <div class="himes-ai-chip" onclick="quickTask('Show recent git changes and current branch in himes-ai')">🌿 Git Status</div>
    </div>

    <!-- Chat Messages -->
    <div class="himes-ai-messages" id="himes-ai-msg-list">
      <div class="himes-ai-msg agent">
        <div style="font-size: 14px; font-weight: 700; margin-bottom: 6px;">👋 Vanakkam {{ Auth::user()->name ?? $currentUserName }}!</div>
        <div style="margin-bottom: 8px;">I am your HIMES Autonomous AI Developer & Assistant Agent.</div>
        <div style="font-size: 12.5px; line-height: 1.5; color: #cbd5e1; margin-bottom: 10px;">
          • <strong>In User View:</strong> I provide clean, plain-language hospital summaries, status cards, screen locations, and optional SQL query views.<br>
          • <strong>In Developer View:</strong> I provide full technical diagnostics, live SELECT SQL queries, Valkey cache states, file paths, and git traces.
        </div>
        <div style="font-size: 11.5px; color: #94a3b8; background: rgba(255, 255, 255, 0.05); padding: 6px 10px; border-radius: 6px;">
          💡 <strong>Tip:</strong> You can drag & drop error logs, SQL files, or images directly into this chat!
        </div>
      </div>
    </div>

    <!-- Typing Indicator -->
    <div class="himes-ai-typing" id="himes-ai-typing">⚡ AI Agent is inspecting HIMES application & database...</div>

    <!-- Attachment Preview Tray -->
    <div id="himes-ai-attachments-tray" class="himes-ai-attachments-tray" style="display: none;"></div>

    <!-- Input Box -->
    <div class="himes-ai-input-wrap">
      <!-- Hidden File Inputs -->
      <input type="file" id="himes-ai-img-input" accept="image/png,image/jpeg,image/jpg,image/webp,image/gif" multiple style="display:none;" onchange="handleFileSelect(event)">
      <input type="file" id="himes-ai-doc-input" accept=".pdf,.log,.txt,.json,.csv,.sql,.md,text/*" multiple style="display:none;" onchange="handleFileSelect(event)">

      <!-- Attachment Action Icons -->
      <div class="himes-ai-input-actions">
        <button type="button" class="himes-ai-attach-btn" onclick="document.getElementById('himes-ai-img-input').click()" title="Attach Image (.jpg, .png)">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
            <path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
          </svg>
        </button>
        <button type="button" class="himes-ai-attach-btn" onclick="document.getElementById('himes-ai-doc-input').click()" title="Attach Document (.pdf, .log, .txt, .json, .sql)">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
            <path d="M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 0 1 5 0v10.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5V6H9v9.5a3 3 0 0 0 6 0V5a4 4 0 0 0-8 0v12.5a5.5 5.5 0 0 0 11 0V6h-1.5z"/>
          </svg>
        </button>
      </div>

      <!-- Multi-Line Textarea -->
      <textarea id="himes-ai-input" class="himes-ai-input" rows="1" placeholder="Ask AI... (Shift+Enter for newline, Enter to send)" onkeydown="handleHimesKey(event)" oninput="autoResizeTextarea(this)"></textarea>

      <!-- Send Button -->
      <button class="himes-ai-send-btn" onclick="sendHimesMessage()" title="Send Message">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
        </svg>
      </button>
    </div>
  </div>
</div>

<script>
  // Helper to dynamically resolve application base path (e.g. /himes-ai or /himes2)
  function getHimesBasePath() {
    const segments = window.location.pathname.split('/').filter(Boolean);
    if (segments.length > 0 && (segments[0].toLowerCase().startsWith('himes') || segments[0].toLowerCase().startsWith('kool'))) {
      return '/' + segments[0];
    }
    return '';
  }

  // Endpoints: primary Laravel route, fallback direct FastAPI
  const LARAVEL_AI_ENDPOINT = (function() {
    const bladeUrl = "{{ url('agent/chat') }}";
    if (bladeUrl && bladeUrl.indexOf('{' + '{') === -1) {
      return bladeUrl;
    }
    return getHimesBasePath() + "/agent/chat";
  })();

  const DIRECT_AI_ENDPOINT = "http://127.0.0.1:8050/api/chat";

  // Dynamic User & Role Binding
  const CURRENT_USER_ID = "{{ $currentUserId ?? 'guest' }}";
  const CURRENT_USERNAME = "{{ addslashes($currentUserName ?? 'User') }}";
  const IS_USER_ADMIN = {{ !empty($isAdmin) ? 'true' : 'false' }};

  // User-Isolated Session ID format: himes_user_{user_id}_{session_uuid}
  let himesSessionUuid = sessionStorage.getItem("himes_session_uuid");
  if (!himesSessionUuid) {
    himesSessionUuid = Math.random().toString(36).substring(2, 10);
    sessionStorage.setItem("himes_session_uuid", himesSessionUuid);
  }
  const USER_SESSION_ID = "himes_user_" + CURRENT_USER_ID + "_" + himesSessionUuid;

  // State Management
  let isDeveloperMode = false; // Default User Mode
  let pendingAttachments = [];

  function toggleHimesAi() {
    const win = document.getElementById("himes-ai-window");
    const backdrop = document.getElementById("himes-ai-backdrop");
    if (win.style.display === "flex") {
      win.style.display = "none";
      backdrop.style.display = "none";
    } else {
      win.style.display = "flex";
      if (win.classList.contains("maximized")) {
        backdrop.style.display = "block";
      }
      setTimeout(() => document.getElementById("himes-ai-input").focus(), 100);
    }
  }

  function toggleHimesMaximize() {
    const win = document.getElementById("himes-ai-window");
    const backdrop = document.getElementById("himes-ai-backdrop");
    const maxIcon = document.getElementById("himes-max-icon");
    const restoreIcon = document.getElementById("himes-restore-icon");
    const maxBtn = document.getElementById("himes-ai-max-btn");

    if (win.classList.contains("maximized")) {
      win.classList.remove("maximized");
      backdrop.style.display = "none";
      maxIcon.style.display = "block";
      restoreIcon.style.display = "none";
      maxBtn.title = "Expand to Full Popup Modal";
    } else {
      win.classList.add("maximized");
      backdrop.style.display = "block";
      maxIcon.style.display = "none";
      restoreIcon.style.display = "block";
      maxBtn.title = "Restore Normal Chatbox View";
    }
  }

  function setMode(devMode) {
    isDeveloperMode = !!devMode;
    const badge = document.getElementById("himes-ai-mode-badge");
    const icon = document.getElementById("himes-mode-icon");
    const text = document.getElementById("himes-mode-text");

    if (isDeveloperMode) {
      badge.className = "himes-ai-mode-badge dev-mode";
      icon.innerText = "💻";
      text.innerText = "Developer View";
    } else {
      badge.className = "himes-ai-mode-badge user-mode";
      icon.innerText = "👤";
      text.innerText = "User View";
    }
  }

  function toggleModeClick() {
    if (!IS_USER_ADMIN) {
      alert("Developer Mode is restricted to Administrator accounts only.");
      return;
    }
    const nextMode = !isDeveloperMode;
    const cmd = nextMode ? "enable developer mode" : "disable developer mode";
    document.getElementById("himes-ai-input").value = cmd;
    sendHimesMessage();
  }

  function autoResizeTextarea(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";
  }

  function handleHimesKey(e) {
    if (e.key === "Enter") {
      if (e.shiftKey) {
        // Shift + Enter -> Allow default newline insertion
        return;
      }
      // Enter alone -> Submit message
      e.preventDefault();
      sendHimesMessage();
    }
  }

  function quickTask(text) {
    document.getElementById("himes-ai-input").value = text;
    sendHimesMessage();
  }

  // --- File Attachment & Drag-and-Drop Handling ---
  function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById("himes-ai-drop-overlay").style.display = "flex";
  }

  function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    const rect = document.getElementById("himes-ai-window").getBoundingClientRect();
    if (e.clientX <= rect.left || e.clientX >= rect.right || e.clientY <= rect.top || e.clientY >= rect.bottom) {
      document.getElementById("himes-ai-drop-overlay").style.display = "none";
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById("himes-ai-drop-overlay").style.display = "none";
    if (e.dataTransfer && e.dataTransfer.files) {
      processFiles(e.dataTransfer.files);
    }
  }

  function handleFileSelect(e) {
    if (e.target.files) {
      processFiles(e.target.files);
      e.target.value = ""; // Reset file input
    }
  }

  function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
  }

  function processFiles(fileList) {
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      if (file.size > 15 * 1024 * 1024) {
        alert("File '" + file.name + "' is larger than 15MB limit.");
        continue;
      }
      const reader = new FileReader();
      reader.onload = function(evt) {
        pendingAttachments.push({
          name: file.name,
          type: file.type || "application/octet-stream",
          size: file.size,
          data: evt.target.result // Base64 Data URL
        });
        renderAttachmentTray();
      };
      reader.readAsDataURL(file);
    }
  }

  function removeAttachment(index) {
    pendingAttachments.splice(index, 1);
    renderAttachmentTray();
  }

  function renderAttachmentTray() {
    const tray = document.getElementById("himes-ai-attachments-tray");
    if (pendingAttachments.length === 0) {
      tray.style.display = "none";
      tray.innerHTML = "";
      return;
    }
    tray.style.display = "flex";
    tray.innerHTML = "";
    pendingAttachments.forEach((att, idx) => {
      const chip = document.createElement("div");
      chip.className = "himes-att-chip";
      const icon = att.type.startsWith("image/") ? "📷" : "📎";
      chip.innerHTML = `
        <span>${icon}</span>
        <span class="himes-att-name" title="${att.name}">${att.name} (${formatFileSize(att.size)})</span>
        <button class="himes-att-del" onclick="removeAttachment(${idx})">✕</button>
      `;
      tray.appendChild(chip);
    });
  }

  // --- Copy to Clipboard for Code Blocks ---
  function copyHimesCode(id, btn) {
    const pre = document.getElementById(id);
    if (!pre) return;
    const text = pre.innerText || pre.textContent;
    navigator.clipboard.writeText(text).then(() => {
      const origHtml = btn.innerHTML;
      btn.innerHTML = `<span style="color:#10b981;font-weight:600;">✓ Copied!</span>`;
      setTimeout(() => { btn.innerHTML = origHtml; }, 2000);
    }).catch(err => {
      console.error("Clipboard copy error:", err);
    });
  }

  // --- Message Formatting & Rendering ---
  function appendHimesMessage(text, role, metaInfo) {
    const list = document.getElementById("himes-ai-msg-list");
    const msg = document.createElement("div");
    msg.className = "himes-ai-msg " + role;

    let str = (typeof text === 'string') ? text : JSON.stringify(text);

    // Escape raw HTML tags for security
    let escaped = str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Code blocks with Syntax Highlighting header & copy buttons
    escaped = escaped.replace(/```(?:([a-zA-Z0-9_\-]+)\n)?([\s\S]*?)```/g, function(match, lang, code) {
      const langLabel = (lang || "CODE").toUpperCase();
      const codeId = "code-" + Math.random().toString(36).substring(2, 9);
      return `
        <div class="himes-code-card">
          <div class="himes-code-header">
            <span class="himes-code-lang">${langLabel}</span>
            <button class="himes-copy-btn" onclick="copyHimesCode('${codeId}', this)" title="Copy Code">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
              <span>Copy</span>
            </button>
          </div>
          <pre id="${codeId}"><code>${code.trim()}</code></pre>
        </div>
      `;
    });

    // Inline codes
    escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold & Italics
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    escaped = escaped.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Headers
    escaped = escaped.replace(/### (.*?)\n/g, '<h4 style="margin:8px 0 4px 0;color:#93c5fd;font-size:14px;">$1</h4>');
    escaped = escaped.replace(/## (.*?)\n/g, '<h3 style="margin:10px 0 4px 0;color:#bfdbfe;font-size:15px;">$1</h3>');

    // Blockquotes & Status Cards (> ✅ or > ⚠️)
    escaped = escaped.replace(/&gt; (✅[^\n]+)/g, '<div class="himes-status-card">$1</div>');
    escaped = escaped.replace(/&gt; (⚠️[^\n]+)/g, '<div class="himes-status-card warning">$1</div>');
    escaped = escaped.replace(/&gt; (ℹ️[^\n]+)/g, '<div class="himes-status-card" style="border-left-color:#38bdf8;background:rgba(56,189,248,0.1);">$1</div>');
    escaped = escaped.replace(/&gt; ([^\n]+)/g, '<blockquote style="border-left:3px solid #6366f1;padding-left:10px;margin:6px 0;opacity:0.85;">$1</blockquote>');

    // Bullet lists
    escaped = escaped.replace(/\n• /g, '<br>• ');
    escaped = escaped.replace(/\n\* /g, '<br>• ');
    escaped = escaped.replace(/\n- /g, '<br>• ');
    escaped = escaped.replace(/\n/g, '<br>');

    if (metaInfo && role === "agent") {
      escaped += `<div style="margin-top:8px;font-size:11px;opacity:0.7;display:flex;align-items:center;gap:4px;">⚡ ${metaInfo}</div>`;
    }

    msg.innerHTML = escaped;
    list.appendChild(msg);
    list.scrollTop = list.scrollHeight;
  }

  // --- Send Message Function ---
  async function sendHimesMessage() {
    const input = document.getElementById("himes-ai-input");
    const task = input.value.trim();
    if (!task && pendingAttachments.length === 0) return;

    // Display user message in UI
    let userDisplay = task;
    if (pendingAttachments.length > 0) {
      const attSummary = pendingAttachments.map(a => `📎 ${a.name}`).join(", ");
      userDisplay = (task ? task + "<br><br>" : "") + `<small style="opacity:0.85;">Attached: ${attSummary}</small>`;
    }
    appendHimesMessage(userDisplay, "user");

    // Copy attachments to send and reset
    const attachmentsToSend = [...pendingAttachments];
    pendingAttachments = [];
    renderAttachmentTray();

    input.value = "";
    input.style.height = "auto";

    const typing = document.getElementById("himes-ai-typing");
    typing.style.display = "block";

    // CSRF Token for Laravel
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
                      document.querySelector('input[name="_token"]')?.value || "";

    const headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    };
    if (csrfToken) {
      headers["X-CSRF-TOKEN"] = csrfToken;
    }

    // Dynamic Live Page Context
    const pageTitleElem = document.querySelector('.page-title, h1, .title, .content-header, .module-title');
    const pageTitle = pageTitleElem ? pageTitleElem.innerText.trim() : (document.title || "");
    const selectedText = (window.getSelection && window.getSelection()) ? window.getSelection().toString().trim() : "";

    const payload = JSON.stringify({
      message: task || "Please inspect the attached files.",
      session_id: USER_SESSION_ID,
      user_id: String(CURRENT_USER_ID),
      username: CURRENT_USERNAME,
      is_admin: IS_USER_ADMIN,
      preferred_model: "auto",
      is_developer_mode: IS_USER_ADMIN ? isDeveloperMode : false,
      attachments: attachmentsToSend,
      context: {
        app: "himes-ai",
        path: "/L9/nagul/himes-ai",
        user: CURRENT_USERNAME,
        user_id: CURRENT_USER_ID,
        is_admin: IS_USER_ADMIN,
        current_url: window.location.href,
        current_path: window.location.pathname,
        page_title: pageTitle,
        selected_text: selectedText
      }
    });

    let targetUrl = DIRECT_AI_ENDPOINT;

    try {
      let response;
      try {
        // 1. Try local Python agent directly (http://127.0.0.1:8050/api/chat)
        response = await fetch(targetUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payload
        });
        if (!response.ok && response.status !== 200) {
          throw new Error("Direct local returned HTTP " + response.status);
        }
      } catch (directErr) {
        // 2. Fallback to Laravel endpoint
        targetUrl = LARAVEL_AI_ENDPOINT;
        response = await fetch(targetUrl, {
          method: "POST",
          headers: headers,
          body: payload
        });
      }

      const data = await response.json();
      typing.style.display = "none";

      // Sync active mode from server response
      if (data.mode) {
        setMode(data.mode === "developer");
      }

      let reply = "";
      if (data.reply) {
        reply = data.reply;
      } else if (data.response) {
        reply = data.response;
      } else if (data.result && data.result.ai_response) {
        reply = data.result.ai_response;
      } else if (data.message) {
        reply = data.message;
      } else {
        reply = "Received response from AI agent.";
      }

      let metaInfo = data.model_used ? `${data.model_used}` : "";
      if (data.mode === "developer") {
        metaInfo += " • 💻 Developer Mode";
      }

      appendHimesMessage(reply, "agent", metaInfo);
    } catch (err) {
      typing.style.display = "none";
      appendHimesMessage(
        "⚠️ Connection Error: Could not reach AI Agent service at " + targetUrl + ". Please ensure your Laravel server or Python agent (`uvicorn main:app --port 8050`) is running.",
        "agent"
      );
    }
  }
</script>
@endif
@endauth
