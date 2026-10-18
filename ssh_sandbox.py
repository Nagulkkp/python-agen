import os
from dotenv import load_dotenv
from ssh_tool import get_ssh_client
from guardrails import SecurityException, validate_command_directory_safety, is_path_inside_allowed_dir

load_dotenv(override=True)

# User's designated workspace directory
NAGUL_BASE_DIR = os.getenv("NAGUL_BASE_DIR", "/L9/nagul")
NAGUL_PROJECT_DIR = os.getenv("NAGUL_PROJECT_DIR", "/L9/nagul/himes-ai")

class SandboxedSSHClient:
    """
    Paramiko SSH wrapper enforcing Nagul's Directory Lock.
    Guarantees all commands, file reads, and file writes are confined
    strictly inside Nagul's folder.
    """

    def __init__(self, base_dir: str = NAGUL_BASE_DIR, project_dir: str = NAGUL_PROJECT_DIR):
        self.base_dir = base_dir
        self.project_dir = project_dir

    def execute_sandboxed_command(self, command: str, working_dir: str = None) -> str:
        """
        Executes a command strictly within Nagul's directory.
        Raises SecurityException if the command attempts to navigate out.
        """
        target_dir = working_dir or self.project_dir

        # 1. Verify working_dir is within allowed folder
        if not is_path_inside_allowed_dir(target_dir, self.base_dir):
            raise SecurityException(
                f"Directory Lock: Working directory '{target_dir}' is outside Nagul's allowed base '{self.base_dir}'!"
            )

        # 2. Validate command safety
        validate_command_directory_safety(command, allowed_dir=self.base_dir)

        # 3. Anchor command execution inside Nagul's directory
        # If the command already specifies cd inside allowed dir, keep it; otherwise prepend cd
        if command.strip().startswith("docker exec") or command.strip().startswith("df") or command.strip().startswith("free"):
            sandboxed_cmd = command.strip()
        else:
            sandboxed_cmd = f"cd {target_dir} && {command.strip()}"

        client = get_ssh_client()
        try:
            stdin, stdout, stderr = client.exec_command(sandboxed_cmd, timeout=30)
            stdin.close()
            out = stdout.read().decode("utf-8", errors="replace").strip()
            err = stderr.read().decode("utf-8", errors="replace").strip()

            if err and not out:
                return f"Error: {err}"
            return out if out else "(Command executed successfully with no output)"
        finally:
            client.close()

    def read_file(self, remote_filepath: str) -> str:
        """
        Safely reads a file strictly within Nagul's directory.
        """
        if not is_path_inside_allowed_dir(remote_filepath, self.base_dir):
            raise SecurityException(
                f"Access Denied: Attempted to read file outside Nagul's folder: {remote_filepath}"
            )
        return self.execute_sandboxed_command(f"cat '{remote_filepath}'")

    def write_file(self, remote_filepath: str, content: str) -> str:
        """
        Safely writes content to a file strictly within Nagul's directory.
        """
        if not is_path_inside_allowed_dir(remote_filepath, self.base_dir):
            raise SecurityException(
                f"Access Denied: Attempted to write file outside Nagul's folder: {remote_filepath}"
            )
        # Write via SSH SFTP or cat EOF
        client = get_ssh_client()
        try:
            sftp = client.open_sftp()
            with sftp.file(remote_filepath, "w") as f:
                f.write(content)
            sftp.close()
            return f"Successfully wrote to {remote_filepath}"
        finally:
            client.close()

# Singleton helper
sandboxed_ssh = SandboxedSSHClient()
