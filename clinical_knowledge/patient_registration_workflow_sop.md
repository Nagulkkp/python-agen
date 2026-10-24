# HIMES Patient Registration & Visit Management SOP

This standard operating procedure details the patient registration workflow, insurance adjudication, and visit creation rules in HIMES.

## 1. Simple Registration vs Detailed Registration
- **Simple Registration (Quick Registration)** (`/viewQuickRegistration`): Single-screen rapid entry for walk-ins and emergencies. Captures essential demographics, auto-loads previous visit insurance (`loadPreviousVisitPayment`), assigns default consultation CPT, generates queue token (`Token_Number`), and routes directly to EMR Caseload or Billing.
- **Detailed Registration** (`/patientRegistration`): 4-tab enterprise registration handling complete demographics, secondary insurance, Coordination of Benefits (COB), TPAs, corporate sponsorship, package services, EMR Treatment Plan import, formal Inpatient admission (`Patient_Visit_Admission_Details`), and medical certificates.

## 2. Demographics, Card Reader & Mandatory Validations
- **Emirates ID / National ID Chip Reader**: Parses full English/Arabic names, ID number, DOB, gender, nationality, and captures photo attachment. Compares `Card_Expiry_Date` against current date.
- **Duplicate ID Detection**: Checks `Patient_Identification_Details` across the branch and triggers merge or redirect if an existing MRN owns that ID.
- **Mandatory Status**: Validates fields configured as `MV` (Mandatory during Visit) or `MB` (Mandatory at Both).

## 3. Provider Role Allocations
- **`AD` (Attending Doctor)**: Mandated for every Consultation visit. Owns EMR Caseload.
- **`CD` (Consulting Doctor)**: Secondary cross-speciality opinion.
- **`RD` (Referring Doctor)**: Internal or external referrer for incentive calculations.

## 4. Insurance, Copay & Deductibles Engine
- **Master Plan Cover** (`Insurance_Plan_Department_Cover`): Department coinsurance (`Percentage_Consulting_Service`, `Percentage_Non_Consulting_Service`), fixed copays (`Amount_Consulting_Service`, `Amount_Non_Consulting_Service`), limit thresholds, and visit caps (`Patient_Share_Limit`).
- **Category Copays** (`Insurance_Plan_Copay_Category_Link`): Granular copays for Pharmacy, Lab, Radiology, and Dental.
- **Point-in-Time Snapshot**: Clones plan rules into `Patient_Visit_Insurance_Plan_Department_Cover` at the moment of registration to permanently freeze the contract terms.
- **Excluded Services**: Flagged `'E'` in master or via front-desk checkbox. Coverage = 0.00 AED, Patient Share = 100%.

## 5. Prior Approval (Pre-Auth) Flow & Suppression Mechanics
- Triggered if service is flagged `'P'`, department requires PA, or gross price exceeds `PA_Limit_Value`.
- **Suppression**: If pre-approval reference (`Authorization_Reference_No`) exists from a prior visit, `Insurance_Prior_Approval_Status = 'A'` is set and re-submission to the payer is suppressed to prevent duplicate claim rejections.

## 6. Patient Merging Workflow (Duplicate MRN Reconciliation)
- Re-points all encounters, appointments, bills, EMR records, and lab/radiology history from duplicate patient (`frompbdsno`) to target master patient (`topbdsno`).
- Audited in `Patient_Basic_Details_Link_Merging` (`Patient_Is_Duplicate = 'Y'`).
- Retires source patient with `Active_Status = 'D'`.

## 7. Service Deletion & Edit Lockouts
- **Deletion Blocked**: If service is invoiced (`Is_Service_Billed = 'Y'`), lab sample collected/processed, radiology study initiated, or visit checked out.
- **Registration Locked**: When visit is checked out (`Visit_Is_Checkedout == 'Y'`), patient discharged, invoice generated, or e-claim batch generated for DHA/Waseel submission.
