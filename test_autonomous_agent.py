import sys
sys.stdout.reconfigure(encoding='utf-8')
from autonomous_agent import autonomous_agent

if __name__ == "__main__":
    task = "global view billing la yesterday evlo patient ku bill pannirukaanga and evlo pending la iruku?"
    print(f"Testing Autonomous Agent on: {task}\n")
    res = autonomous_agent.run(task)
    print("\n=== AGENT RESPONSE ===")
    print("Status:", res.get("status"))
    print("Steps:", res.get("steps"))
    print("Actions Taken:")
    for a in res.get("actions_taken", []):
        print(f"  Step {a['step']}: Tool={a['tool']}, Args={a['args']}")
    print("\nReply:")
    print(res.get("reply"))
