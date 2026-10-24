import os
import sys
from dotenv import load_dotenv
from ssh_tool import get_ssh_client
from ssh_sandbox import sandboxed_ssh

load_dotenv(override=True)

REMOTE_BASE = "/L9/nagul/himes-ai"
LOCAL_BASE = os.path.dirname(os.path.abspath(__file__))

def deploy_to_laravel():
    print("=" * 60)
    print("DEPLOYING AGENT CHAT CONTROLLER & ROUTE TO LARAVEL")
    print("=" * 60)

    client = get_ssh_client()
    sftp = client.open_sftp()

    # 1. Upload AgentChatController.php
    local_controller = os.path.join(LOCAL_BASE, "AgentChatController.php")
    remote_controller = f"{REMOTE_BASE}/app/Http/Controllers/AgentChatController.php"
    print(f"\n1. Uploading {local_controller} -> {remote_controller}...")
    sftp.put(local_controller, remote_controller)
    print("   Uploaded AgentChatController.php successfully.")

    # 2. Upload ai_chat_widget.blade.php to resources/views
    local_widget = os.path.join(LOCAL_BASE, "ai_chat_widget.blade.php")
    remote_widget = f"{REMOTE_BASE}/resources/views/ai_chat_widget.blade.php"
    print(f"\n2. Uploading {local_widget} -> {remote_widget}...")
    sftp.put(local_widget, remote_widget)
    print("   Uploaded ai_chat_widget.blade.php successfully.")

    # 3. Check PHP syntax of AgentChatController.php
    lint_res = sandboxed_ssh.execute_sandboxed_command(
        f"php -l {remote_controller}",
        working_dir=REMOTE_BASE
    )
    print(f"\n3. Syntax check for Controller:\n   {lint_res.strip()}")

    # 4. Check & Append Route to routes/web.php
    remote_web_routes = f"{REMOTE_BASE}/routes/web.php"
    print(f"\n4. Checking routes in {remote_web_routes}...")
    grep_res = sandboxed_ssh.execute_sandboxed_command(
        f"grep -n 'agent/chat' {remote_web_routes} || true",
        working_dir=REMOTE_BASE
    )

    with sftp.open(remote_web_routes, "r") as rf:
        current_content = rf.read().decode("utf-8")

    route_definition = (
        "// AI Assistant Chatbox Endpoint\n"
        "Route::post('/agent/chat', [\\App\\Http\\Controllers\\AgentChatController::class, 'sendMessage'])\n"
        "    ->withoutMiddleware([\\App\\Http\\Middleware\\VerifyCsrfToken::class])\n"
        "    ->name('agent.chat');"
    )

    if "agent/chat" in current_content:
        import re
        current_content = re.sub(
            r"// AI Assistant Chatbox Endpoint\s*Route::post\('/agent/chat'.*?->name\('agent\.chat'\);",
            lambda m: route_definition,
            current_content,
            flags=re.DOTALL
        )
    else:
        current_content = current_content.rstrip() + "\n\n" + route_definition + "\n"

    with sftp.open(remote_web_routes, "w") as wf:
        wf.write(current_content)
    print("   Route updated in routes/web.php with CSRF exemption.")

    # 5. Check PHP syntax of routes/web.php
    routes_lint = sandboxed_ssh.execute_sandboxed_command(
        f"php -l {remote_web_routes}",
        working_dir=REMOTE_BASE
    )
    print(f"\n5. Syntax check for routes/web.php:\n   {routes_lint.strip()}")

    # 6. Clear Laravel View and Route caches
    print("\n6. Clearing Laravel view and route cache...")
    sandboxed_ssh.execute_sandboxed_command("php artisan view:clear && php artisan route:clear", working_dir=REMOTE_BASE)
    print("   View and route caches cleared.")

    # 7. Verify with php artisan route:list
    print("\n7. Verifying route with 'php artisan route:list --name=agent.chat'...")
    route_list = sandboxed_ssh.execute_sandboxed_command(
        "php artisan route:list --name=agent.chat",
        working_dir=REMOTE_BASE
    )
    safe_out = route_list.encode("ascii", errors="replace").decode("ascii")
    print(f"   {safe_out.strip()}")

    sftp.close()
    client.close()
    print("\n" + "=" * 60)
    print("DEPLOYMENT TO LARAVEL COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    deploy_to_laravel()
