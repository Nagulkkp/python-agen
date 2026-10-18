<!-- HIMES AI Dev Assistant Floating Chat Widget -->
<style>
  #himes-ai-widget {
    position: fixed;
    bottom: 25px;
    right: 25px;
    z-index: 9999999;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
    width: 440px;
    max-width: calc(100vw - 40px);
    height: 620px;
    max-height: calc(100vh - 130px);
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05);
    flex-direction: column;
    overflow: hidden;
    color: #e5e7eb;
    animation: himesAiSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes himesAiSlideUp {
    from { opacity: 0; transform: translateY(20px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  .himes-ai-header {
    padding: 16px 20px;
    background: #1f2937;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
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
  }
  .himes-ai-title {
    font-weight: 700;
    font-size: 15px;
    color: #f9fafb;
    margin: 0;
  }
  .himes-ai-status {
    font-size: 12px;
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
  .himes-ai-close {
    background: transparent;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    font-size: 20px;
    padding: 4px 8px;
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
  }
  .himes-ai-chips::-webkit-scrollbar { display: none; }
  .himes-ai-chip {
    white-space: nowrap;
    background: rgba(79, 70, 229, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    font-size: 12px;
    padding: 6px 12px;
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
  }
  .himes-ai-msg {
    max-width: 90%;
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 13.5px;
    line-height: 1.5;
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
  .himes-ai-msg pre {
    background: #0d1117;
    border: 1px solid #30363d;
    padding: 10px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: Consolas, monospace;
    font-size: 12px;
    color: #58a6ff;
    margin: 8px 0;
  }
  .himes-ai-msg code {
    background: rgba(255, 255, 255, 0.1);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 12px;
  }
  .himes-ai-input-wrap {
    padding: 14px 16px;
    background: #1f2937;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    gap: 10px;
    align-items: center;
  }
  .himes-ai-input {
    flex: 1;
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 10px 14px;
    color: white;
    font-size: 13.5px;
    outline: none;
    transition: border-color 0.2s;
  }
  .himes-ai-input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }
  .himes-ai-send-btn {
    background: #4f46e5;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .himes-ai-send-btn:hover {
    background: #4338ca;
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
  }
</style>

<div id="himes-ai-widget">
  <!-- Floating Button -->
  <div id="himes-ai-trigger" onclick="toggleHimesAi()">
    <svg viewBox="0 0 24 24">
      <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5Z"/>
    </svg>
  </div>

  <!-- Chat Window -->
  <div id="himes-ai-window">
    <div class="himes-ai-header">
      <div class="himes-ai-title-wrap">
        <div class="himes-ai-avatar">🤖</div>
        <div>
          <div class="himes-ai-title">HIMES AI Assistant</div>
          <div class="himes-ai-status"><span class="himes-ai-dot"></span> Autonomous Agent Active</div>
        </div>
      </div>
      <button class="himes-ai-close" onclick="toggleHimesAi()">✕</button>
    </div>

    <!-- Quick Action Chips -->
    <div class="himes-ai-chips">
      <div class="himes-ai-chip" onclick="quickTask('Check the latest error in storage/logs/laravel.log and explain how to fix it')">🔍 Check Latest Error</div>
      <div class="himes-ai-chip" onclick="quickTask('price list management menu enga iruku?')">💰 Price List Menu</div>
      <div class="himes-ai-chip" onclick="quickTask('Check server disk space, memory, and uptime')">🩺 System Health</div>
      <div class="himes-ai-chip" onclick="quickTask('Show recent git changes and current branch in himes-ai')">🌿 Git Status</div>
    </div>

    <!-- Chat Messages -->
    <div class="himes-ai-messages" id="himes-ai-msg-list">
      <div class="himes-ai-msg agent">
        👋 <strong>Vanakkam Nagul!</strong><br>
        I am your <strong>HIMES Autonomous AI Developer Agent</strong>. You can ask me where menus are located, inspect error logs, diagnose bugs, or help with Laravel coding tasks!
      </div>
    </div>

    <!-- Typing Indicator -->
    <div class="himes-ai-typing" id="himes-ai-typing">⚡ AI Agent is inspecting HIMES application & server...</div>

    <!-- Input Box -->
    <div class="himes-ai-input-wrap">
      <input type="text" id="himes-ai-input" class="himes-ai-input" placeholder="Ask AI: e.g. price list enga iruku? Check error..." onkeydown="handleHimesKey(event)">
      <button class="himes-ai-send-btn" onclick="sendHimesMessage()">Send</button>
    </div>
  </div>
</div>

<script>
  // Primary endpoint points to Laravel Controller (/agent/chat); 
  // falls back to direct FastAPI endpoint if running outside Laravel.
  const LARAVEL_AI_ENDPOINT = "/agent/chat";
  const DIRECT_AI_ENDPOINT = "http://127.0.0.1:8000/api/chat";

  function toggleHimesAi() {
    const win = document.getElementById("himes-ai-window");
    if (win.style.display === "flex") {
      win.style.display = "none";
    } else {
      win.style.display = "flex";
      document.getElementById("himes-ai-input").focus();
    }
  }

  function quickTask(text) {
    document.getElementById("himes-ai-input").value = text;
    sendHimesMessage();
  }

  function handleHimesKey(e) {
    if (e.key === "Enter") {
      sendHimesMessage();
    }
  }

  function appendHimesMessage(text, role, metaInfo) {
    const list = document.getElementById("himes-ai-msg-list");
    const msg = document.createElement("div");
    msg.className = "himes-ai-msg " + role;
    
    // Clean markdown formatting
    let str = (typeof text === 'string') ? text : JSON.stringify(text);
    let formatted = str
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/```([\s\S]*?)```/g, '<pre>$1</pre>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/### (.*?)\n/g, '<h4 style="margin:8px 0 4px 0;color:#93c5fd;">$1</h4>')
      .replace(/## (.*?)\n/g, '<h3 style="margin:10px 0 4px 0;color:#bfdbfe;">$1</h3>')
      .replace(/\n\* /g, '<br>• ')
      .replace(/\n- /g, '<br>• ')
      .replace(/\n/g, '<br>');

    if (metaInfo && role === "agent") {
      formatted += `<div style="margin-top:6px;font-size:11px;opacity:0.65;font-style:italic;">⚡ ${metaInfo}</div>`;
    }
      
    msg.innerHTML = formatted;
    list.appendChild(msg);
    list.scrollTop = list.scrollHeight;
  }

  async function sendHimesMessage() {
    const input = document.getElementById("himes-ai-input");
    const task = input.value.trim();
    if (!task) return;

    appendHimesMessage(task, "user");
    input.value = "";

    const typing = document.getElementById("himes-ai-typing");
    typing.style.display = "block";

    // Prepare headers including CSRF token for Laravel if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
                      document.querySelector('input[name="_token"]')?.value || "";

    const headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    };
    if (csrfToken) {
      headers["X-CSRF-TOKEN"] = csrfToken;
    }

    const payload = JSON.stringify({
      message: task,
      task: task,
      session_id: "himes_chat_session",
      preferred_model: "auto",
      context: {
        app: "himes-ai",
        path: "/L9/nagul/himes-ai",
        user: "nagul"
      }
    });

    let targetUrl = LARAVEL_AI_ENDPOINT;

    try {
      let response;
      try {
        // First try calling Laravel Controller route (/agent/chat)
        response = await fetch(targetUrl, {
          method: "POST",
          headers: headers,
          body: payload
        });

        // If route does not exist in Laravel (404), fall back to direct FastAPI agent
        if (response.status === 404) {
          targetUrl = DIRECT_AI_ENDPOINT;
          response = await fetch(targetUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: payload
          });
        }
      } catch (networkErr) {
        // Fallback to direct FastAPI agent if Laravel endpoint unreachable
        targetUrl = DIRECT_AI_ENDPOINT;
        response = await fetch(targetUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payload
        });
      }

      const data = await response.json();
      typing.style.display = "none";

      let reply = "";
      if (data.reply) {
        reply = data.reply;
      } else if (data.result && data.result.ai_response) {
        reply = data.result.ai_response;
      } else if (data.message) {
        reply = data.message;
      } else {
        reply = "Received response from AI agent.";
      }

      let metaInfo = data.model_used ? `${data.model_used}` : "";
      if (data.action_executed && data.action_executed.cache_hit) {
        metaInfo = "ChromaDB Semantic Cache (Instant Hit)";
      }

      appendHimesMessage(reply, "agent", metaInfo);
    } catch (err) {
      typing.style.display = "none";
      appendHimesMessage(
        "⚠️ Connection Error: Could not reach AI Agent service at " + targetUrl + ". Please ensure your Laravel server or Python agent (`uvicorn main:app --port 8000`) is running.",
        "agent"
      );
    }
  }
</script>
