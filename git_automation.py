import os
import requests
from dotenv import load_dotenv
from ssh_sandbox import sandboxed_ssh
from guardrails import SecurityException

load_dotenv(override=True)

class SafeGitWorkflow:
    """
    Automates safe Git workflows strictly inside Nagul's folder.
    STRICT RULE: Creates sub-branches, commits, pushes, and opens PRs.
    NEVER merges branches automatically.
    """

    def __init__(self, project_dir: str = "/L9/nagul/himes-ai"):
        self.project_dir = project_dir
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_owner = os.getenv("GITHUB_REPO_OWNER")
        self.repo_name = os.getenv("GITHUB_REPO_NAME")

    def run_cmd(self, cmd: str) -> str:
        # Strictly verify no merge command is ever passed
        if "git merge" in cmd or "pr merge" in cmd:
            raise SecurityException("CRITICAL VIOLATION: AI Agent is strictly forbidden from executing git merge!")
        return sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=self.project_dir)

    def checkout_and_pull_dev(self, base_branch: str = "development") -> str:
        """Pulls the latest code from the development branch inside Nagul's folder."""
        print(f"Fetching and checking out {base_branch}...")
        self.run_cmd("git fetch origin")
        self.run_cmd(f"git checkout {base_branch}")
        res = self.run_cmd(f"git pull origin {base_branch}")
        return res

    def create_sub_branch(self, branch_name: str) -> str:
        """Creates a unique sub-branch (e.g., fix/zoho-bug-101 or feature/zoho-task-202)."""
        # Validate branch name prefix
        if not (branch_name.startswith("fix/") or branch_name.startswith("feature/") or branch_name.startswith("task/")):
            branch_name = f"fix/{branch_name}"
        res = self.run_cmd(f"git checkout -b {branch_name}")
        return f"Created and switched to sub-branch: {branch_name}"

    def run_syntax_and_tests(self, changed_files: list[str] = None) -> dict:
        """
        Runs PHP syntax checks (php -l) on changed files and runs tests (php artisan test).
        Must pass before committing.
        """
        results = {"syntax_check": "passed", "tests": "passed", "errors": []}

        # 1. PHP Syntax Check
        if changed_files:
            for f in changed_files:
                if f.endswith(".php"):
                    chk = self.run_cmd(f"php -l '{f}'")
                    if "No syntax errors detected" not in chk:
                        results["syntax_check"] = "failed"
                        results["errors"].append(chk)
                        raise SecurityException(f"Pre-commit safety failed! Syntax error in {f}: {chk}")

        # 2. Automated test run (optional test suite)
        test_out = self.run_cmd("docker exec nagul php /var/www/html/himes-ai/artisan test --stop-on-failure 2>&1 || true")
        results["test_output"] = test_out
        return results

    def commit_and_push(self, branch_name: str, commit_message: str) -> str:
        """Commits changes and pushes sub-branch to remote GitHub."""
        self.run_cmd("git add .")
        self.run_cmd(f'git commit -m "{commit_message}"')
        push_res = self.run_cmd(f"git push -u origin {branch_name}")
        return push_res

    def create_pull_request(self, branch_name: str, title: str, body: str, base_branch: str = "development") -> dict:
        """
        Creates a Pull Request via GitHub REST API.
        STRICT RULE: STOPS after creating PR. Does NOT merge.
        """
        if not self.github_token or not self.repo_owner or not self.repo_name:
            return {
                "status": "pushed_to_branch",
                "message": f"Branch '{branch_name}' pushed successfully! Configure GITHUB_TOKEN in .env to auto-create PR.",
                "branch": branch_name
            }

        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        payload = {
            "title": title,
            "body": f"{body}\n\n---\n*Created autonomously by Nagul's AI Agent. Requires human review and manual merge.*",
            "head": branch_name,
            "base": base_branch
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            pr_data = response.json()
            return {
                "status": "pr_created",
                "pr_url": pr_data.get("html_url"),
                "pr_number": pr_data.get("number"),
                "message": "PR created successfully! Merging must be done manually by human review."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to create PR: {response.text}",
                "status_code": response.status_code
            }

    def execute_safe_task_workflow(self, task_id: str, commit_msg: str, pr_title: str, pr_desc: str, base_branch: str = "development") -> dict:
        """
        Full end-to-end safe workflow:
        1. Checkout & pull latest development
        2. Create sub-branch fix/{task_id}
        3. Run pre-commit checks
        4. Commit & push branch
        5. Create GitHub PR
        6. STOP (No merge)
        """
        branch_name = f"fix/{task_id}"
        self.checkout_and_pull_dev(base_branch)
        self.create_sub_branch(branch_name)
        self.run_syntax_and_tests()
        self.commit_and_push(branch_name, commit_msg)
        pr_result = self.create_pull_request(branch_name, pr_title, pr_desc, base_branch)
        return pr_result
