# HIMES AI Architect: Automated System Audit & Production Prompts
**Generated on:** 2026-10-19 14:05:41  
**Scope:** HIMES Laravel Application (`/L9/nagul/himes-ai`), MSSQL Database (414 Tables), ChromaDB Vector Base (434 Docs), Valkey In-Memory Index (8 Namespaces).

---

## Executive Summary & System Health Dashboard

| Dimension | Metric | Status | Finding / Architecture Note |
| :--- | :--- | :---: | :--- |
| **Controllers & Routes** | 1,164 Controllers / 12,485 Routes | ⚠️ | High modularity, but extreme lack of dedicated FormRequests (only 6 exist). |
| **Database Schema** | 414 Tables | 🟢 | Comprehensive MSSQL schema covering PA, Claims, Billing, Pharmacy, EMR, and Masters. |
| **Knowledge Base** | 434 Document Chunks in ChromaDB | 🟢 | Full workflow and rule documentation indexed. |
| **Valkey Memory Store** | 8 Namespaces (`himes:module:*`) | ⚡ | Sub-millisecond hybrid retrieval operational at `192.168.20.152:6379`. |
| **Log Health** | 9 Recent Unhandled Exceptions | ⚠️ | Emergency logger and vendor file path exceptions in `laravel.log`. |

---

## Top 3 Critical Enhancements Identified

1. **Form Request Security & Validation Hardening (GAP-01):**
   * *Problem:* Out of 1,164 controllers, only 6 FormRequest classes exist. Controllers rely on inline validation or direct unvalidated `$request->all()`.
   * *Action:* Migrate high-risk controllers (`RegistrationAppointmentPostController`, `PatientBillingBackendController`, `AutoEclaimPostController`) to strict FormRequests.
2. **Insurance E-Claim Failure Recovery & Batch Auto-Requeue (GAP-02):**
   * *Problem:* Network disconnects with DHPO/Shafafiya trap claims in unsubmitted limbo without an automated retry worker.
   * *Action:* Implement an asynchronous queue worker with exponential backoff and dead-letter queue for failed claim batches.
3. **Proactive Self-Healing Log Listener (Proposal 2):**
   * *Problem:* Agent is purely reactive; bugs remain live until reported by front-desk users.
   * *Action:* Implement a real-time `laravel.log` tailer that autonomously analyzes 500 errors, locates the file/line, and drafts validated PRs.

---

## Structured Ready-to-Run Prompts

### Category A: Immediate Bug Fixes & Code Gap Filling Prompts

#### Prompt A1: Centralized FormRequest Validation for Patient Registration & Billing
```markdown
Act as a Senior Laravel Architect. In my HIMES application (/L9/nagul/himes-ai), migrate the unvalidated request handling in:
1. App\Http\Controllers\RegistrationAppointmentPostController
2. App\Http\Controllers\PatientBillingBackendController

Create dedicated FormRequest classes:
- app/Http/Requests/StorePatientRegistrationRequest.php
- app/Http/Requests/ProcessPatientBillingRequest.php

Requirements:
- Validate required patient demographics (Emirates ID format, First Name, Mobile number).
- Validate billing items (Service_USSDB_Serial_No, Quantity >= 1, Payment_Type_Serial_No).
- Implement authorize() returning true with permission check.
- Replace inline request handling in the controllers with these injected FormRequests.
- Run `php -l` to verify syntax and test via Tinker before committing.
```

#### Prompt A2: Insurance Claim Batch Submission Failure Queue & Automated Retry
```markdown
Act as a Healthcare Claims Specialist and Backend Engineer. 
Audit `AutoEclaimPostController.php` and the `claim_` tables (`Claim_Detail`, `claim_batch_header`).

Implement an automated Claim Batch Re-queue and Retry Mechanism:
1. When gateway submission to DHPO / Shafafiya returns HTTP 502/504 or network timeout:
   - Catch the exception cleanly without terminating the transaction.
   - Set `claim_batch_header.Batch_Submission_Status = 'RETRY_PENDING'`.
   - Log the failure code in `API_Request_Response_Log_Details`.
2. Create an artisan command `php artisan himes:retry-failed-claims` scheduled to run every 15 minutes.
3. Ensure no duplicate claim batches are ever submitted.
4. Verify execution on branch `fix/claims-retry-worker`.
```

#### Prompt A3: Prior Authorization (PA) Guard for Unapproved Clinical Services
```markdown
Act as an EMR & Billing Integration Specialist.
In HIMES, CPT services requiring Prior Authorization must not be billed or rendered without an approval code.

Audit `PatientBillingGetController.php` and `PA_Patient_Visit_Insurance_Service_Cover_Details`:
1. Check if an active service in `Patient_Visit_Services` has `Requires_Prior_Approval = 'Y'`.
2. If YES, verify whether `Prior_Authorization_Details.Approval_Status = 'APPROVED'`.
3. If PENDING or REJECTED:
   - In `addPatientBilling` view, highlight the service with an amber badge "PA Pending Approval".
   - Disable bill finalization for that specific item until approved, or allow converting to Cash patient with explicit consent.
4. Implement this check cleanly and verify via PHP syntax check.
```

---

### Category B: Advanced Autonomous Agent Features Prompts

#### Prompt B1: Self-Healing Laravel Log Listener Service (`himes_log_listener.py`)
```markdown
Act as an AI SRE and DevOps Engineer.
Create a Python background daemon `himes_log_listener.py` in `c:\Nagul\python-agent\`:

Requirements:
1. Connect via SSH to /L9/nagul/himes-ai and tail `storage/logs/laravel.log` in real time.
2. Filter for fatal errors: `laravel.EMERGENCY`, `laravel.ERROR`, `SQLSTATE`, `Uncaught Exception`.
3. When an error is detected:
   - Parse the stack trace, identifying the exact file path and line number in `/L9/nagul/himes-ai`.
   - Read 40 lines of context around the fault using `read_code`.
   - Use Google Gemini or GPT-4o to analyze the root cause and propose a minimal, safe code fix.
   - Validate the fix with `php -l`.
   - Create an isolated sub-branch `fix/auto-heal-<timestamp>` and push to GitHub.
   - Send an alert to Nagul via chat widget with the patch diff and PR link.
```

#### Prompt B2: Autonomous Pest/PHPUnit Test Scaffolder
```markdown
Act as a QA Automation Architect.
Create an automated test generation tool `auto_test_generator.py` for HIMES:

Requirements:
1. Whenever the AI agent modifies any controller or service in `/L9/nagul/himes-ai`:
   - Inspect the modified method inputs, outputs, and database queries.
   - Generate a dedicated Pest or PHPUnit feature test in `tests/Feature/`.
   - Test covers: Positive path (valid payload), Validation failure (empty inputs), and Authorization checks.
2. Run the test inside Docker: `docker exec nagul php /var/www/html/himes-ai/artisan test --filter=<TestName>`.
3. Only if the test passes (Green) allow git commit and push.
```

#### Prompt B3: Insurance & Eligibility API Mocking Sandbox
```markdown
Act as a Healthcare API Integration Architect.
Build an internal Mock Insurance Gateway `mock_insurance_gateway.py` in `c:\Nagul\python-agent`:

Requirements:
1. Provide mock HTTP endpoints simulating DHPO (Dubai Health Post Office) & Shafafiya:
   - POST `/api/mock/eligibility`: Returns valid insurance eligibility with co-pay % and network tier.
   - POST `/api/mock/prior-auth`: Returns instant PA approval with authorization code `AUTH-998822`.
   - POST `/api/mock/eclaim/submit`: Returns XML 200 OK acceptance receipt.
2. Configure HIMES `.env` `MOCK_INSURANCE_GATEWAY=true` for offline development and testing.
```

---

### Category C: Performance & Valkey/ChromaDB Optimization Prompts

#### Prompt C1: Multi-tier Valkey Hot-Cache Warming for Active Encounters
```markdown
Act as a High-Performance Database Engineer.
Write a cache-warming script `warm_valkey_active_visits.py` in `c:\Nagul\python-agent`:

Requirements:
1. Query MSSQL for all patients registered today:
   `SELECT Permanent_Visit_No, Patient_Basic_Details_Serial_No FROM Patient_Visit_Basic_Details WHERE CAST(Patient_Visit_Registered_Date_Time AS DATE) = CAST(GETDATE() AS DATE) AND Active_Status = 'A'`.
2. For each active visit:
   - Pre-fetch active services, patient name, and applicable tariff base rates (SRFNI / SRFI).
   - Pre-load into Valkey under `himes:active_visit:{visit_no}` with 12-hour TTL.
3. In `PatientBillingGetController` and FastAPI `/api/chat`:
   - Read directly from Valkey hot-cache in 2 milliseconds instead of hitting MSSQL every turn!

```

#### Prompt C2: ChromaDB Semantic Re-Ranking with Medical Domain Cross-Encoder
```markdown
Act as an AI Search & Retrieval Engineer.
Enhance `memory_manager.py` with two-stage Cross-Encoder re-ranking:

Requirements:
1. Stage 1: Fast vector search in ChromaDB `agent_knowledge_base` retrieving Top 15 documents.
2. Stage 2: Re-rank using a lightweight cross-encoder (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) scoring clinical relevance for medical terms, CPT codes, and billing jargon.
3. Benchmark latency and ensure total hybrid retrieval completes under 250ms before auto-caching into Valkey.
```

#### Prompt C3: Distributed Valkey Transaction Locks for High-Concurrency Billing Counters
```markdown
Act as a Distributed Systems Engineer.
Implement high-concurrency billing counter locks using Valkey:

Requirements:
1. When multiple billing operators at different counters finalize bills simultaneously for the same patient or visit:
   - Acquire Valkey distributed lock `himes:lock:bill:{visit_no}`.
   - Enforce atomicity on receipt sequence incrementing (`pbpr.Patient_Bill_Header_Payments_Received_Serial_No`).
   - Prevent race conditions where two receipts receive the same number or invoice duplicate claims.

2. Integrate with `AgentChatController` and `PatientBillingBackendController`.
```
