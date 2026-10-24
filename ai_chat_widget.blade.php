<!-- HIMES AI Dev Assistant Floating Chat Widget with Full-Screen Modal, Multi-Media Attachments & Dual Mode System -->
@php
    $sessUserId = Session::get('User_Id');
    $authUserId = Auth::id();
    $currentUserId = (string) ($sessUserId ?? $authUserId ?? 'admin');
    $sessUserName = Session::get('User_Name') ?? Session::get('user.user_name');
    $currentUserName = (string) ($sessUserName ?? (Auth::check() ? (Auth::user()->name ?? Auth::user()->username) : 'User'));
    $isAdmin = (bool) (
        Session::get('isAdmin') === true ||
        in_array(strtolower((string)$currentUserId), ['admin', 'adminsuper', 'admin super']) ||
        (Auth::check() && (Auth::user()->is_admin ?? false))
    );
@endphp
@if(!request()->is('login') && !request()->is('*/login'))
<style>
  #himes-ai-widget {
    position: fixed;
    bottom: 68px;
    right: 20px;
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
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
    box-shadow: 0 4px 16px rgba(79, 70, 229, 0.45), 0 0 10px rgba(168, 85, 247, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.3);
    user-select: none;
  }
  #himes-ai-trigger:hover {
    transform: scale(1.12) translateY(-2px);
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.65), 0 0 16px rgba(168, 85, 247, 0.5);
  }
  #himes-ai-trigger svg {
    width: 22px;
    height: 22px;
    fill: currentColor;
    flex-shrink: 0;
  }
  #himes-ai-window {
    display: none;
    position: fixed;
    bottom: 120px;
    right: 20px;
    width: 490px;
    min-width: 350px;
    max-width: calc(100vw - 30px);
    height: 660px;
    min-height: 420px;
    max-height: calc(100vh - 120px);
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.05);
    flex-direction: column;
    overflow: hidden;
    color: #e5e7eb;
    animation: himesAiSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    resize: none;
    transition: transform 0.2s ease, opacity 0.2s ease;
  }
  #himes-ai-window.minimized {
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    width: 360px !important;
    overflow: hidden !important;
    resize: none !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
  }
  #himes-ai-window.minimized .himes-ai-messages,
  #himes-ai-window.minimized .himes-ai-input-wrap,
  #himes-ai-window.minimized #himes-ai-drop-overlay,
  #himes-ai-window.minimized .himes-resize-edge,
  #himes-ai-window.minimized #himes-resize-handle {
    display: none !important;
  }
  #himes-ai-window.minimized .himes-ai-header {
    cursor: pointer;
    border-bottom: none !important;
  }
  #himes-ai-window.maximized {
    top: 50% !important;
    left: 50% !important;
    bottom: auto !important;
    right: auto !important;
    transform: translate(-50%, -50%) !important;
    width: 92vw !important;
    max-width: 1350px !important;
    height: 90vh !important;
    max-height: 920px !important;
    border-radius: 18px !important;
    box-shadow: 0 35px 100px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255, 255, 255, 0.15) !important;
    z-index: 9999999;
    resize: none !important;
  }
  .himes-resize-edge {
    position: absolute;
    z-index: 100;
  }
  .himes-resize-left {
    top: 0;
    left: 0;
    width: 8px;
    height: 100%;
    cursor: ew-resize;
  }
  .himes-resize-left:hover {
    background: rgba(99, 102, 241, 0.35);
  }
  .himes-resize-top {
    top: 0;
    left: 0;
    width: 100%;
    height: 8px;
    cursor: ns-resize;
  }
  .himes-resize-top:hover {
    background: rgba(99, 102, 241, 0.35);
  }
  #himes-resize-handle {
    position: absolute;
    top: 0;
    left: 0;
    width: 22px;
    height: 22px;
    cursor: nwse-resize;
    z-index: 102;
    border-top: 3px solid rgba(99, 102, 241, 0.7);
    border-left: 3px solid rgba(99, 102, 241, 0.7);
    border-top-left-radius: 20px;
    transition: all 0.2s;
  }
  #himes-resize-handle:hover {
    border-color: #a855f7;
    background: rgba(168, 85, 247, 0.2);
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
    padding: 13px 18px;
    background: #1f2937;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-shrink: 0;
    position: relative;
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
  /* 3-Dots Kebab Menu & Settings Dropdown */
  .himes-kebab-wrapper {
    position: relative;
    display: inline-block;
  }
  #himes-kebab-menu {
    display: none;
    position: absolute;
    top: 38px;
    right: 0;
    width: 220px;
    background: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.65);
    z-index: 1000;
    padding: 6px;
    animation: himesFadeIn 0.15s ease-out;
  }
  .himes-menu-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 12px;
    border-radius: 9px;
    cursor: pointer;
    transition: background 0.15s;
    user-select: none;
  }
  .himes-menu-item:hover {
    background: rgba(255, 255, 255, 0.08);
  }
  .himes-toggle-switch {
    width: 36px;
    height: 20px;
    background: #475569;
    border-radius: 10px;
    position: relative;
    transition: background 0.2s;
    flex-shrink: 0;
  }
  .himes-toggle-switch.active {
    background: #8b5cf6;
  }
  .himes-toggle-knob {
    width: 16px;
    height: 16px;
    background: white;
    border-radius: 50%;
    position: absolute;
    top: 2px;
    left: 2px;
    transition: transform 0.2s;
  }
  .himes-toggle-switch.active .himes-toggle-knob {
    transform: translateX(16px);
  }
  /* SQL queries go directly through chat input - drawer removed */
  .himes-details {
    margin: 8px 0;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
  }
  .himes-summary {
    cursor: pointer;
    color: #93c5fd;
    font-weight: 600;
    outline: none;
    user-select: none;
  }
  .himes-summary:hover {
    color: #bfdbfe;
  }
  /* HIMES Responsive Interactive Data Tables */
  .himes-table-wrapper {
    margin: 10px 0;
    width: 100%;
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: #0f172a;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  }
  .himes-data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: left;
    white-space: nowrap;
  }
  .himes-data-table th {
    background: #1e293b;
    color: #93c5fd;
    font-weight: 700;
    padding: 9px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    letter-spacing: 0.3px;
    position: sticky;
    top: 0;
  }
  .himes-data-table td {
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    color: #e2e8f0;
  }
  .himes-data-table tr:nth-child(even) {
    background: rgba(255, 255, 255, 0.02);
  }
  .himes-data-table tr:hover {
    background: rgba(99, 102, 241, 0.12);
  }
  .himes-badge-success {
    background: rgba(16, 185, 129, 0.18);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 2px 7px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
  }
  .himes-badge-warning {
    background: rgba(245, 158, 11, 0.18);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
    padding: 2px 7px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
  }
  .himes-badge-danger {
    background: rgba(239, 68, 68, 0.18);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.35);
    padding: 2px 7px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
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
    <!-- Multi-Edge Drag-to-Resize Handles -->
    <div class="himes-resize-edge himes-resize-left" title="Drag left edge to resize width"></div>
    <div class="himes-resize-edge himes-resize-top" title="Drag top edge to resize height"></div>
    <!-- Corner Drag-to-Resize Handle -->
    <div id="himes-resize-handle" title="Drag corner to resize width & height"></div>

    <!-- Drag & Drop Overlay -->
    <div id="himes-ai-drop-overlay" class="himes-ai-drop-overlay">
      <div class="himes-ai-drop-box">
        <div style="font-size: 34px; margin-bottom: 6px;">📂</div>
        <div style="font-weight: 700; font-size: 15px; color: #ffffff;">Drop Files to Attach</div>
        <div style="font-size: 12px; color: #a5b4fc; margin-top: 4px;">Images (.jpg, .png) & Documents (.pdf, .log, .txt, .json, .sql)</div>
      </div>
    </div>

    <!-- Header -->
    <div class="himes-ai-header" onclick="handleHeaderClick(event)">
      <div class="himes-ai-title-wrap">
        <div class="himes-ai-avatar">🤖</div>
        <div>
          <div class="himes-ai-title">HIMES AI Assistant</div>
          <div class="himes-ai-status"><span class="himes-ai-dot"></span> Autonomous Agent Active</div>
        </div>
      </div>
      <div class="himes-ai-header-controls" onclick="event.stopPropagation()">
        <!-- 3-Dots Settings & Mode Kebab Menu -->
        <div class="himes-kebab-wrapper">
          <button id="himes-kebab-btn" class="himes-ai-icon-btn" onclick="toggleHimesKebabMenu(event)" title="Settings & View Mode">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
            </svg>
          </button>
          <!-- Dropdown -->
          <div id="himes-kebab-menu" onclick="event.stopPropagation()">
            @if($isAdmin)
            <div class="himes-menu-item" onclick="toggleDeveloperModeFromMenu()">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:15px;">💻</span>
                <div>
                  <div style="font-weight:600;font-size:12.5px;color:#f1f5f9;">Developer Mode</div>
                  <div id="himes-dev-mode-sub" style="font-size:10.5px;color:#94a3b8;">Disabled (User View)</div>
                </div>
              </div>
              <div id="himes-menu-dev-switch" class="himes-toggle-switch">
                <div class="himes-toggle-knob"></div>
              </div>
            </div>
            @endif
            <div class="himes-menu-item" onclick="setWindowPreset('small')">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:15px;">📱</span>
                <div>
                  <div style="font-weight:600;font-size:12.5px;color:#f1f5f9;">Compact Size</div>
                  <div style="font-size:10.5px;color:#94a3b8;">380 × 520px</div>
                </div>
              </div>
            </div>
            <div class="himes-menu-item" onclick="setWindowPreset('standard')">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:15px;">💻</span>
                <div>
                  <div style="font-weight:600;font-size:12.5px;color:#f1f5f9;">Standard Size</div>
                  <div style="font-size:10.5px;color:#94a3b8;">490 × 660px</div>
                </div>
              </div>
            </div>
            <div class="himes-menu-item" onclick="setWindowPreset('large')">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:15px;">🖥️</span>
                <div>
                  <div style="font-weight:600;font-size:12.5px;color:#f1f5f9;">Large Size</div>
                  <div style="font-size:10.5px;color:#94a3b8;">700 × 780px</div>
                </div>
              </div>
            </div>
            <div class="himes-menu-item" onclick="toggleHimesMaximize();const m=document.getElementById('himes-kebab-menu');if(m)m.style.display='none';">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:15px;">⛶</span>
                <div>
                  <div style="font-weight:600;font-size:12.5px;color:#f1f5f9;">Full Screen Modal</div>
                  <div style="font-size:10.5px;color:#94a3b8;">92vw × 90vh</div>
                </div>
              </div>
            </div>
            <!-- Custom Dimensions Input Row -->
            <div style="border-top:1px solid rgba(255,255,255,0.08);margin:6px 0 4px 0;"></div>
            <div style="padding:6px 8px;" onclick="event.stopPropagation()">
              <div style="font-weight:600;font-size:11px;color:#94a3b8;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.4px;">Custom Size (px):</div>
              <div style="display:flex;align-items:center;gap:5px;">
                <input type="number" id="himes-custom-w" placeholder="Width" min="320" max="1920" style="width:72px;background:#0f172a;border:1px solid #334155;color:#f8fafc;padding:4px 6px;border-radius:6px;font-size:11.5px;outline:none;">
                <span style="color:#64748b;font-size:12px;">×</span>
                <input type="number" id="himes-custom-h" placeholder="Height" min="380" max="1200" style="width:72px;background:#0f172a;border:1px solid #334155;color:#f8fafc;padding:4px 6px;border-radius:6px;font-size:11.5px;outline:none;">
                <button type="button" onclick="applyCustomDimensions()" style="background:#4f46e5;color:white;border:none;padding:4px 9px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;">Apply</button>
              </div>
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.08);margin:4px 0 6px 0;"></div>
            <div class="himes-menu-item" onclick="clearHimesChat()">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:15px;">🗑️</span>
                <div>
                  <div style="font-weight:600;font-size:12.5px;color:#f87171;">Clear Chat</div>
                  <div style="font-size:10.5px;color:#94a3b8;">Reset conversation</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Size Toggle Preset Button -->
        <button id="himes-ai-size-btn" class="himes-ai-icon-btn" onclick="cycleWindowSize()" title="Toggle Size (Small / Standard / Large)">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M19 12h-2v3h-3v2h5v-5zM7 9h3V7H5v5h2V9zm14-6H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16.01H3V4.99h18v14.02z"/>
          </svg>
        </button>

        <!-- Minimize Button -->
        <button id="himes-ai-min-btn" class="himes-ai-icon-btn" onclick="toggleHimesMinimize(event)" title="Minimize Chat Window (—)">
          <svg id="himes-min-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M19 13H5v-2h14v2z"/>
          </svg>
          <svg id="himes-min-restore-icon" style="display:none;" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M12 8l6 6H6z"/>
          </svg>
        </button>

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
        <button class="himes-ai-close" onclick="toggleHimesAi()" title="Close Assistant (✕)">✕</button>
      </div>
    </div>

    <!-- Queries go directly through chat input -->
    <!-- Type SELECT queries or natural language questions in the chat box below -->

    <!-- Chat Messages -->
    <div class="himes-ai-messages" id="himes-ai-msg-list">
      <div class="himes-ai-msg agent">
        <div style="font-size: 15px; font-weight: 600; color: #f8fafc;">
          👋 Hi {{ $currentUserName ?? 'Admin' }}!
        </div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">
          How can I help you with HIMES today? Ask a question or run a database query below.
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
    const devSwitch = document.getElementById("himes-menu-dev-switch");
    const devSub = document.getElementById("himes-dev-mode-sub");
    if (devSwitch) {
      if (isDeveloperMode) {
        devSwitch.classList.add("active");
        if (devSub) devSub.innerText = "Enabled (Technical View)";
      } else {
        devSwitch.classList.remove("active");
        if (devSub) devSub.innerText = "Disabled (User View)";
      }
    }
  }

  function toggleHimesKebabMenu(e) {
    e.stopPropagation();
    const menu = document.getElementById("himes-kebab-menu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
  }

  document.addEventListener("click", function(e) {
    const menu = document.getElementById("himes-kebab-menu");
    if (menu && menu.style.display === "block") {
      menu.style.display = "none";
    }
  });

  function toggleDeveloperModeFromMenu() {
    if (!IS_USER_ADMIN) {
      alert("Developer Mode is restricted to Administrator accounts only.");
      return;
    }
    const nextMode = !isDeveloperMode;
    const cmd = nextMode ? "enable developer mode" : "disable developer mode";
    document.getElementById("himes-ai-input").value = cmd;
    sendHimesMessage();
    const menu = document.getElementById("himes-kebab-menu");
    if (menu) menu.style.display = "none";
  }

  let isHimesMinimized = false;
  let preMinDimensions = { width: '490px', height: '660px' };

  function toggleHimesMinimize(e) {
    if (e) e.stopPropagation();
    const win = document.getElementById("himes-ai-window");
    const minIcon = document.getElementById("himes-min-icon");
    const restoreIcon = document.getElementById("himes-min-restore-icon");
    const backdrop = document.getElementById("himes-ai-backdrop");
    const minBtn = document.getElementById("himes-ai-min-btn");

    if (!isHimesMinimized) {
      if (win.classList.contains("maximized")) {
        toggleHimesMaximize();
      }
      preMinDimensions.width = win.style.width || "490px";
      preMinDimensions.height = win.style.height || "660px";
      win.classList.add("minimized");
      isHimesMinimized = true;
      if (minIcon) minIcon.style.display = "none";
      if (restoreIcon) restoreIcon.style.display = "block";
      if (minBtn) minBtn.title = "Restore Chatbox (Expand)";
      if (backdrop) backdrop.style.display = "none";
    } else {
      win.classList.remove("minimized");
      win.style.width = preMinDimensions.width;
      win.style.height = preMinDimensions.height;
      isHimesMinimized = false;
      if (minIcon) minIcon.style.display = "block";
      if (restoreIcon) restoreIcon.style.display = "none";
      if (minBtn) minBtn.title = "Minimize Chat Window (—)";
    }
  }

  function handleHeaderClick(e) {
    if (isHimesMinimized) {
      toggleHimesMinimize();
    }
  }

  let currentPresetIndex = 1; // 0: small, 1: standard, 2: large
  const PRESET_SIZES = [
    { name: 'small', w: '380px', h: '520px', label: 'Compact (380x520)' },
    { name: 'standard', w: '490px', h: '660px', label: 'Standard (490x660)' },
    { name: 'large', w: '700px', h: '780px', label: 'Large (700x780)' }
  ];

  function cycleWindowSize() {
    const win = document.getElementById("himes-ai-window");
    if (isHimesMinimized) {
      toggleHimesMinimize();
    }
    if (win.classList.contains("maximized")) {
      toggleHimesMaximize();
    }
    currentPresetIndex = (currentPresetIndex + 1) % PRESET_SIZES.length;
    const p = PRESET_SIZES[currentPresetIndex];
    setWindowPreset(p.name);
  }

  function setWindowPreset(preset) {
    const win = document.getElementById("himes-ai-window");
    const backdrop = document.getElementById("himes-ai-backdrop");
    win.classList.remove("maximized");
    if (isHimesMinimized) {
      win.classList.remove("minimized");
      isHimesMinimized = false;
      const minIcon = document.getElementById("himes-min-icon");
      const restoreIcon = document.getElementById("himes-min-restore-icon");
      if (minIcon) minIcon.style.display = "block";
      if (restoreIcon) restoreIcon.style.display = "none";
    }
    backdrop.style.display = "none";

    const maxIcon = document.getElementById("himes-max-icon");
    const restoreIcon = document.getElementById("himes-restore-icon");
    if (maxIcon) maxIcon.style.display = "block";
    if (restoreIcon) restoreIcon.style.display = "none";

    let targetW = 490, targetH = 660;
    if (preset === 'small') {
      currentPresetIndex = 0;
      targetW = 380; targetH = 520;
    } else if (preset === 'large') {
      currentPresetIndex = 2;
      targetW = 700; targetH = 780;
    } else {
      currentPresetIndex = 1;
      targetW = 490; targetH = 660;
    }
    win.style.width = targetW + "px";
    win.style.height = targetH + "px";

    const customW = document.getElementById("himes-custom-w");
    const customH = document.getElementById("himes-custom-h");
    if (customW) customW.value = targetW;
    if (customH) customH.value = targetH;

    const sizeBtn = document.getElementById("himes-ai-size-btn");
    if (sizeBtn) sizeBtn.title = `Current: ${PRESET_SIZES[currentPresetIndex].label} - Click to switch size`;
    const menu = document.getElementById("himes-kebab-menu");
    if (menu) menu.style.display = "none";
  }

  function applyCustomDimensions() {
    const win = document.getElementById("himes-ai-window");
    const customW = document.getElementById("himes-custom-w");
    const customH = document.getElementById("himes-custom-h");
    if (!win || !customW || !customH) return;

    let w = parseInt(customW.value, 10);
    let h = parseInt(customH.value, 10);

    if (isNaN(w) || w < 320) w = 380;
    if (w > window.innerWidth - 30) w = window.innerWidth - 30;

    if (isNaN(h) || h < 380) h = 520;
    if (h > window.innerHeight - 80) h = window.innerHeight - 80;

    if (isHimesMinimized) {
      win.classList.remove("minimized");
      isHimesMinimized = false;
      const minIcon = document.getElementById("himes-min-icon");
      const restoreIcon = document.getElementById("himes-min-restore-icon");
      if (minIcon) minIcon.style.display = "block";
      if (restoreIcon) restoreIcon.style.display = "none";
    }
    if (win.classList.contains("maximized")) {
      win.classList.remove("maximized");
      const backdrop = document.getElementById("himes-ai-backdrop");
      if (backdrop) backdrop.style.display = "none";
    }

    win.style.width = w + "px";
    win.style.height = h + "px";
    customW.value = w;
    customH.value = h;

    const menu = document.getElementById("himes-kebab-menu");
    if (menu) menu.style.display = "none";
  }

  function clearHimesChat() {
    const list = document.getElementById("himes-ai-msg-list");
    list.innerHTML = `
      <div class="himes-ai-msg agent">
        <div style="font-size: 15px; font-weight: 600; color: #f8fafc;">
          👋 Hi ${CURRENT_USERNAME || 'Admin'}!
        </div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">
          Chat cleared. How can I help you with HIMES today? Ask a question or run a database query below.
        </div>
      </div>
    `;
    const menu = document.getElementById("himes-kebab-menu");
    if (menu) menu.style.display = "none";
  }

  // Multi-Edge Drag-to-Resize Logic (Left edge, Top edge, Top-Left Corner)
  (function initResizeHandles() {
    const win = document.getElementById("himes-ai-window");
    const corner = document.getElementById("himes-resize-handle");
    const leftEdge = document.querySelector(".himes-resize-left");
    const topEdge = document.querySelector(".himes-resize-top");
    if (!win) return;

    let resizeMode = null; // 'corner', 'left', 'top'
    let startX, startY, startWidth, startHeight;

    function startResize(e, mode) {
      if (win.classList.contains("maximized") || win.classList.contains("minimized")) return;
      resizeMode = mode;
      startX = e.clientX;
      startY = e.clientY;
      startWidth = parseInt(document.defaultView.getComputedStyle(win).width, 10);
      startHeight = parseInt(document.defaultView.getComputedStyle(win).height, 10);
      document.documentElement.addEventListener("mousemove", doResize, false);
      document.documentElement.addEventListener("mouseup", stopResize, false);
      e.preventDefault();
      e.stopPropagation();
    }

    if (corner) corner.addEventListener("mousedown", (e) => startResize(e, "corner"));
    if (leftEdge) leftEdge.addEventListener("mousedown", (e) => startResize(e, "left"));
    if (topEdge) topEdge.addEventListener("mousedown", (e) => startResize(e, "top"));

    function doResize(e) {
      if (!resizeMode) return;
      if (resizeMode === "corner" || resizeMode === "left") {
        const newWidth = startWidth - (e.clientX - startX);
        if (newWidth >= 320 && newWidth <= (window.innerWidth - 30)) {
          win.style.width = newWidth + "px";
          const cw = document.getElementById("himes-custom-w");
          if (cw) cw.value = newWidth;
        }
      }
      if (resizeMode === "corner" || resizeMode === "top") {
        const newHeight = startHeight - (e.clientY - startY);
        if (newHeight >= 380 && newHeight <= (window.innerHeight - 80)) {
          win.style.height = newHeight + "px";
          const ch = document.getElementById("himes-custom-h");
          if (ch) ch.value = newHeight;
        }
      }
    }

    function stopResize() {
      resizeMode = null;
      document.documentElement.removeEventListener("mousemove", doResize, false);
      document.documentElement.removeEventListener("mouseup", stopResize, false);
    }
  })();

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

    // Markdown Table Parser (Converts | col | col | into responsive HTML table)
    escaped = escaped.replace(/(?:^|\n)(\|[^\n]+\|\r?\n\|(?:\s*:?-+:?\s*\|)+\r?\n(?:\|[^\n]+\|\r?\n?)+)/g, function(match, tableBlock) {
      const rawLines = tableBlock.trim().split(/\r?\n/).map(l => l.trim()).filter(l => l.startsWith('|') && l.endsWith('|'));
      if (rawLines.length < 2) return match;
      
      let html = '<div class="himes-table-wrapper"><table class="himes-data-table">';
      let isHeader = true;
      
      for (let i = 0; i < rawLines.length; i++) {
        const line = rawLines[i];
        if (/^\|(?:\s*:?-+:?\s*\|)+$/.test(line)) {
          isHeader = false;
          continue;
        }
        const cells = line.slice(1, -1).split('|').map(c => c.trim());
        if (isHeader) {
          html += '<thead><tr>';
          cells.forEach(c => { html += `<th>${c}</th>`; });
          html += '</tr></thead><tbody>';
          isHeader = false;
        } else {
          html += '<tr>';
          cells.forEach(c => {
            let content = c;
            if (content === 'A' || content === 'Active' || content === 'Approved' || content === 'Y' || content === 'Billed') {
              content = `<span class="himes-badge-success">${content}</span>`;
            } else if (content === 'N' || content === 'Pending' || content === 'Unbilled') {
              content = `<span class="himes-badge-warning">${content}</span>`;
            } else if (content === 'Cancelled' || content === 'Rejected' || content === 'Deleted') {
              content = `<span class="himes-badge-danger">${content}</span>`;
            } else if (/^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i.test(content)) {
              content = `<span style="display:inline-flex;align-items:center;gap:6px;"><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:${content};border:1px solid rgba(255,255,255,0.3);flex-shrink:0;"></span><code style="font-size:11px;">${content}</code></span>`;
            }
            html += `<td>${content}</td>`;
          });
          html += '</tr>';
        }
      }
      html += '</tbody></table></div>';
      return html;
    });

    // Unescape details, summary and b tags for interactive accordion tables
    escaped = escaped.replace(/&lt;details&gt;/gi, '<details class="himes-details">')
                     .replace(/&lt;\/details&gt;/gi, '</details>')
                     .replace(/&lt;summary&gt;/gi, '<summary class="himes-summary">')
                     .replace(/&lt;\/summary&gt;/gi, '</summary>')
                     .replace(/&lt;b&gt;/gi, '<b>')
                     .replace(/&lt;\/b&gt;/gi, '</b>');

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
