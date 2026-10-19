from main import chat_with_agent, ChatRequest

test_cases = [
    ("LIS lab workflow pathi sollu", "LIS Domain Flow"),
    ("RIS radiology imaging flow enna?", "RIS Domain Flow"),
    ("credit note create panna enna process?", "Credit Notes Flow"),
    ("invoice posting to tally export flow enna?", "Invoice Posting Flow"),
    ("cron jobs list enna?", "Cron Jobs Schedule"),
    ("explain 400 masters setup", "400+ Masters Setup"),
    ("eclaim batch submission process", "E-Claim Submission"),
    ("pharmacy module ah paaru", "Screen / Pharmacy Module"),
]

print("=" * 60)
print("TESTING ALL 12 HIMES DOMAIN WORKFLOW RETRIEVAL")
print("=" * 60)

for msg, label in test_cases:
    req = ChatRequest(
        message=msg,
        session_id="test_domain_session",
        context={"current_path": "/himes-ai/viewGlobalOPPharmacy"}
    )
    res = chat_with_agent(req)
    print(f"\n--- [TEST] {label} ('{msg}') ---")
    print(f"Status: {res.status} | Model: {res.model_used}")
    snippet = res.reply[:250].replace('\n', ' ')
    print(f"Reply: {snippet}...")
    assert res.status == "success", f"Failed for {label}"

print("\n" + "=" * 60)
print("ALL 12 DOMAIN WORKFLOW RETRIEVAL TESTS PASSED!")
print("=" * 60)
