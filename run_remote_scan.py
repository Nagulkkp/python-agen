import os
from ssh_sandbox import sandboxed_ssh

local_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "remote_scanner.py")
with open(local_file, "r", encoding="utf-8") as f:
    content = f.read()

res = sandboxed_ssh.write_file("/L9/nagul/himes-ai/remote_scanner.py", content)
print("Write result:", res)

out = sandboxed_ssh.execute_sandboxed_command("python3 remote_scanner.py")
print("Scan output:", out)
