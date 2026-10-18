import os
from ssh_tool import get_ssh_client

client = get_ssh_client()
sftp = client.open_sftp()
local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codebase_scan_result.json")
remote_path = "/L9/nagul/himes-ai/codebase_scan_result.json"

print(f"Downloading {remote_path} to {local_path}...")
sftp.get(remote_path, local_path)
sftp.close()
client.close()

size = os.path.getsize(local_path)
print(f"Downloaded successfully! Size: {size / 1024 / 1024:.2f} MB")
