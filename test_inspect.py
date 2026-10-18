import sys
sys.stdout.reconfigure(encoding='utf-8')
from ssh_sandbox import sandboxed_ssh

if __name__ == "__main__":
    out = sandboxed_ssh.execute_sandboxed_command("grep -rn 'ai_chat_widget' /L9/nagul/himes-ai/resources/views/ | head -n 10")
    print("Widget views:", out)
