import os
import paramiko
from dotenv import load_dotenv
from langchain_core.tools import tool

# Ensure .env is loaded
load_dotenv(override=True)

def find_default_ssh_key():
    """Finds default SSH key if not explicitly set."""
    home = os.path.expanduser("~")
    for key_name in ["id_ed25519", "id_rsa", "id_ecdsa"]:
        p = os.path.join(home, ".ssh", key_name)
        if os.path.exists(p):
            return p
    return None

def get_ssh_client():
    """Establishes and returns an authenticated Paramiko SSH client."""
    load_dotenv(override=True)
    
    host = os.getenv("SSH_HOST")
    port = int(os.getenv("SSH_PORT", 22))
    user = os.getenv("SSH_USER", "root")
    password = os.getenv("SSH_PASSWORD")
    key_path = os.getenv("SSH_KEY_PATH")

    if not host or not user:
        raise ValueError("SSH_HOST and SSH_USER must be configured in .env")

    if not key_path and not password:
        key_path = find_default_ssh_key()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connect_kwargs = {
        "hostname": host,
        "port": port,
        "username": user,
        "timeout": 10,
    }

    if key_path and os.path.exists(key_path):
        connect_kwargs["key_filename"] = key_path
    elif password:
        connect_kwargs["password"] = password
    else:
        raise ValueError("Either SSH_PASSWORD or SSH_KEY_PATH must be provided in .env")

    client.connect(**connect_kwargs)
    return client

def test_ssh_connection() -> dict:
    """Tests the SSH connection and returns server details."""
    try:
        client = get_ssh_client()
        stdin, stdout, stderr = client.exec_command("uname -a || ver", timeout=10)
        stdin.close()
        output = stdout.read().decode("utf-8", errors="replace").strip()
        client.close()
        return {
            "status": "success",
            "message": "SSH Connection successful!",
            "system_info": output
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"SSH Connection failed: {str(e)}"
        }

@tool
def execute_ssh_command(command: str) -> str:
    """
    Executes a shell command on the remote server via SSH.
    """
    try:
        client = get_ssh_client()
        stdin, stdout, stderr = client.exec_command(command, timeout=15)
        stdin.close()
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        client.close()

        if err and not out:
            return f"Error: {err}"
        return out if out else "(Command executed successfully with no output)"
    except Exception as e:
        return f"SSH Execution Error: {str(e)}"
