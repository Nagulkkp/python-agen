import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from ssh_sandbox import sandboxed_ssh

cmd = sys.argv[1] if len(sys.argv) > 1 else "ls -la"
out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir="/L9/nagul/himes-ai")
print(out)
