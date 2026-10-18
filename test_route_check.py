import sys
from ssh_sandbox import sandboxed_ssh

if __name__ == "__main__":
    out = sandboxed_ssh.execute_sandboxed_command("grep -nC 3 'PBED' /L9/nagul/himes-ai/app/Http/Controllers/GlobalViewBillingController.php | head -n 25")
    print("PBED table:\n", out)
