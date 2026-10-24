---
name: registration-workflow
description: >-
  Comprehensive architectural reference and master guide for the HIMES Patient Registration Workflow.
  Covers Simple Registration (Quick Registration) vs Detailed Registration (Full Multi-Tab Registration),
  Demographics & ID card validations, Provider & Speciality hierarchy (Attending AD, Consulting CD, Referring RD),
  Service selection (Consultation vs Non-consultation, Packages, Treatment Plans), Inpatient/Daycare Admission details,
  Payment & Insurance engines (Cash, Insurance, Corporate, TPA, Primary/Secondary Coordination of Benefits,
  Copay & Deductible limits, Excluded and Covered services at Plan vs Visit levels, Pre-auth rules),
  Prior Approval lifecycle & suppression mechanics, Patient Merge architecture (Duplicate MRN reconciliation),
  Replication & Carry-forward flows (Previous visit, insurance, diagnosis, treatment plans),
  Visit Type transitions (New, Free/Paid Follow-up), Check-In & Visit Creation, Service deletion restrictions,
  and Privilege-based edit lockouts.
---

# HIMES Patient Registration Workflow: Senior Architect Specification

This document provides the definitive, comprehensive architectural specification of the **Patient Registration & Visit Management System** in HIMES. It details all underlying master tables, business rules, calculation algorithms, controller methods, and operational workflows.

---

## 1. Architectural Overview: Simple Registration vs. Detailed Registration

HIMES implements two purpose-built registration engines:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REGISTRATION ENGINES                            │
├───────────────────────────────────┬────────────────────────────────────┤
│ Simple Registration (Quick Reg)   │ Detailed Registration (Full Reg)   │
│ URL: /viewQuickRegistration       │ URL: /patientRegistration          │
│ Controller: QuickRegistrationCont │ Controller: RegistrationTabControl │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Single-screen rapid entry       │ • Multi-tab enterprise intake      │
│ • Minimal demographics            │ • Full demographics & IDs          │
│ • Fast consultation / walk-in     │ • Secondary insurance & TPAs       │
│ • Instant token generation        │ • Formal Inpatient Admission       │
│ • Auto-loads previous insurance   │ • Patient Merge & Relationships    │
│ • Direct billing handoff          │ • Certificate & Document uploads   │
└───────────────────────────────────┴────────────────────────────────────┘
```

### 1.1 Simple Registration (Quick Registration / DRP)
- **Primary Controller**: `app/Http/Controllers/DRP/QuickRegistrationController.php` & `QuickDemoRegController.php`
- **Views**: `resources/views/registration/quickRegistration/` & `FPQuickRegistration/`
- **Purpose**: Rapid outpatient walk-ins, emergency desk intake, and quick follow-ups.
- **Workflow**:
  1. **Patient Search / Quick Demographics**: Input Phone or Name or scan Emirates ID. If existing, loads patient; if new, inputs First Name, Gender, Mobile, DOB.
  2. **Doctor & Service**: Selecting doctor invokes `getCurrentResourceNameSelection` and automatically loads default consultation CPT (`IsDefault = 'Y'`).
  3. **Payment & Previous Insurance**: Invokes `loadPreviousVisitPayment` to automatically fetch last visit's Insurance Company, TPA, Plan, Network, Card Number, Expiry, and Copay limits.
  4. **One-Click Check-In**: `postQuickRegistrationDetails` persists visit, creates `Patient_Visit_Basic_Details`, generates clinic queue `Token_Number`, and passes encounter to Doctor EMR Caseload or Billing.

### 1.2 Detailed Registration (Full Enterprise Registration)
- **Primary Controllers**:
  - `RegistrationTabController.php`: Tab state coordinator and navigation.
  - `RegistrationController.php`: Demographics persistence and core visit validation.
  - `RegistrationPartOneController.php`: Ancillary services, LIS/RIS links, certificates.
  - `RegistrationPartTwoController.php`: Merging, checkout validation, follow-up status, admission.
  - `RegistrationInsuranceController.php`: Multi-payer insurance engine, copay, deductibles, prior authorization.
- **Views**: `resources/views/registration/patientRegistration.blade.php` (Tabbed Layout).
- **Tab Layout**:
  - **Tab 1: Demographics**: Full personal, contact, identification documents, photo capture, DND communication preferences, family relationship linking, patient merging.
  - **Tab 2: Insurance & Payment**: Primary Card, Secondary Card (Coordination of Benefits), Corporate sponsorship, TPA selection, Plan coverage, Copay/Deductible caps, manual service exclusions and pre-auth overrides.
  - **Tab 3: Visit & Services**: Encounter types (OPD/IPD/DAY/ER), Doctor allocation (Attending `AD`, Consulting `CD`, Referring `RD`), Package services, EMR Treatment Plan import, Inpatient admission details, Primary Care physician mapping.
  - **Tab 4: Documents & Certificates**: Sick leave certificates, fitness certificates, medical report attachments, clinical notes, gate pass slips.

---

## 2. Complete Master Tables Inventory

The Registration module is powered by an extensive suite of master tables:

| Domain | Master Table Name | Description & Key Columns |
| :--- | :--- | :--- |
| **Demographics** | `Patient_Basic_Details` | Master patient record: `Patient_Basic_Details_Serial_No`, `Permanent_MRN_No`, `Temporary_MRN_No`, `Gender_Code`, `Patient_DOB`, `Nationality_Code`, `Branch_Code`. |
| | `Patient_Basic_Encript_Details` | AES Encrypted PII: `Patient_First_Name`, `Patient_Middle_Name`, `Patient_Last_Name`, `Contact_Phone_Mobile`, `Contact_Email`, `Patient_Address`. |
| | `Patient_Basic_Details_Link_Merging` | Audit log for merged MRNs: `From_Patient_Basic_Details_Serial_No`, `To_Patient_Basic_Details_Serial_No`, `Patient_Is_Duplicate = 'Y'`, `Default_MRN_No_To_Search = 'Y'`. |
| | `Gender`, `Nationality`, `Country` | Standard demographic reference lookups. |
| | `Registration_Common_Masters` | Schools, universities, referral channels (`Registration_Common_Type = 'SC'`). |
| | `Patient_Basic_Notification` & `_Modules_Link` | Communication preferences: SMS/Email consent, DND (Do Not Disturb) settings for Module `APS` and `REG`. |
| **Identifications** | `Identification_Type` | Master ID types: Emirates ID (`EID`), Passport (`PAS`), National ID (`NID`), Iqama (`IQA`). |
| | `Country_Identification_Type` | Country-specific rules, mandatory flags (`mandatory_status`: `MA`, `MV`, `MB`, `NM`), validation regex. |
| | `Patient_Identification_Details` | Patient ID entries: `Identification_Type_Code`, `Identification_Number`, `Expiry_Date`, `Card_Front_Image`, `Card_Back_Image`. |
| **Organization & Provider** | `Company` & `Branch` | Multi-facility enterprise organizational hierarchy. |
| | `Department` & `Department_Branch` | Hospital clinical departments (e.g., Cardiology, Dental, Radiology). |
| | `Sub_Department` | Sub-specialities within departments. |
| | `Speciality` & `Speciality_Sub_Department_Branch` | Clinical specialities mapped to branches (`ssdb`). |
| | `Resource_Parent` & `Resource_Parent_User` | Doctor/Practitioner master entity linked to system login `User_Id`. |
| | `Resource` | Service delivery node referencing `Resource_Parent_Serial_No` and `Speciality_Sub_Department_Branch_Serial_No`. |
| | `Resource_Service` & `Resource_Service_Operating_Hours` | Doctor service mappings, default flag (`IsDefault = 'Y'`), duration (`Resource_Service_Time_Slot`), working hours. |
| | `Resource_Non_Availability` | Doctor leaves, breaks, conferences, emergency blocks (`Resource_Non_Availability_Start/End_Date_Time`). |
| **Visit & Clinical** | `Visit_Encounter_Type` | Encounter classifications: `OPD` (Outpatient), `IPD` (Inpatient), `DAY` (Daycare), `ER` (Emergency). |
| | `Patient_Visit_Basic_Details` | Master visit encounter: `Permanent_Visit_No`, `Is_Patient_Visit_Registered`, `Visit_Is_Checkedout`, `Visit_Is_Non_Consultation`, `Token_Number`. |
| | `Patient_Visit_Resources` | Doctor allocation per visit: `Visit_Doctor_Type_Code` (`AD`=Attending, `CD`=Consulting, `RD`=Referring). |
| | `Patient_Visit_Services` | Services ordered in encounter: `Is_Service_Billed`, `Service_Delivery_Status`, `Prior_Approval_Required_Flag`. |
| | `Patient_Visit_Admission_Details` | Formal admission details: `AccompaniedName`, `Relation`, `ArrivalMode`, `AdmissionType`, `ReasonForAdmission`, `EstimatedLengthofStay`. |
| | `Patient_Visit_Appointments` | Relational bridge linking `Patient_Appointment_Serial_No` to `Patient_Visit_Basic_Details_Serial_No`. |
| **Insurance & Pricing** | `Patient_Payment_Types` | Payment modalities: `CSH` (Cash), `INS` (Insurance), `CRP` (Corporate), `TPA` (Third Party Administrator). |
| | `Insurance_Company` & `Insurance_Company_Branch` | Insurance payer entities (e.g., Daman, AXA, Bupa, Tawuniya, Metlife). |
| | `Insurance_Associate_Company` | TPA intermediaries (e.g., NextCare, NAS, Mednet, Neuron, FMC, Enaya). |
| | `Insurance_Associate_Company_Insurance_Company` | Associative bridging between TPAs and Insurance Companies. |
| | `Patient_Income_Network` | Coverage tier networks: Comprehensive, Silk, Gold, Silver, Green, Basic. |
| | `Insurance_Company_Patient_Income_Network` | Network contract mapping per insurance company branch. |
| | `Insurance_Plans` | Plan definitions: `Insurance_Plan_Name`, `Plan_Policy_Expiry_Date`, `Plan_Effective_Date`, `TOB_Files_Path`. |
| | `Insurance_Plan_Department_Cover` | Universal Code Group / department coverage, copays, coinsurance, deductibles, and pre-auth thresholds. |
| | `Insurance_Plan_Excluded_Prior_Approval_Services` | Service-level exclusions (`'E'`) and prior authorization (`'P'`) rules. |
| | `Insurance_Plan_Copay_Category_Link` | Modular category copay linking: Consultation, Pharmacy, Lab, Radiology, Dental, Optical. |
| | `Service_Rate_For_Insurance` | Negotiated gross tariff and price schedules for insurance billing. |
| | `Branch_Free_Paid_Followup_Services` | Branch & speciality mapping for Free Follow-up (`'F'`), Paid Follow-up (`'P'`), and Revisit (`'R'`). |
| | `Patient_Visit_Insurance_Card_Details` | Active visit insurance snapshot: Card number, expiry, policy number, eligibility reference. |
| | `Patient_Visit_Insurance_Plan_Department_Cover` | Point-in-time snapshot of department coverage rules frozen at registration. |
| | `Patient_Visit_Insurance_Plan_Excluded_Prior_Approval_Services` | Point-in-time snapshot of service exclusions and pre-auth requirements. |
| **Prior Authorization (PA)**| `PA_Patient_Visit_Basic_Details` | Master pre-authorization tracking visit. |
| | `PA_Patient_Visit_Services` | Services submitted for insurance authorization. |
| | `PA_Patient_Visit_Insurance_Service_Cover_Details` | Pre-auth status tracking: `Insurance_Prior_Approval_Status` (`A`=Approved, `D`=Denied, `M`=More Info, `S`=Submitted). |
| | `Denial_Code` | Payer denial codes and rejection justifications. |

---

## 3. Demographics, Card Reader & Mandatory Validations

### 3.1 Card Reader XML Parsing
- Handled via `RegistrationPartOneController.php@getxmlfilefullcontent` & `getxmlmoveuploadfile`.
- Automatically extracts data from the official chip reader:
  - Demographic fields: `Full_Name_EN`, `Full_Name_AR`, `ID_Number`, `Date_Of_Birth`, `Gender`, `Nationality`.
  - Photo attachment: Uploads photo file directly to FTP / server path.
  - Card Validity: Compares `Card_Expiry_Date` against current date.

### 3.2 Duplicate ID Validation
- Methods: `RegistrationPartTwoController@CheckdefaultemiratesID` & `RegistrationController@checkSponserNameForRegEmirates`.
- Queries `Patient_Identification_Details` and `Patient_Basic_Details` across the active branch.
- If an existing patient already owns that Identification Number, system triggers an alert modal displaying the matched patient's MRN and Name, offering a direct redirect or Patient Merge.

### 3.3 Mandatory Field Rules (`config/applicationsetting.php`)
- Evaluated against `mandatory_status`:
  ```php
  'mandatory_status' => [
      'NM' => 'Not mandatory at all',
      'MA' => 'Mandatory during appointment',
      'MV' => 'Mandatory during visit',
      'MB' => 'Mandatory at both'
  ]
  ```
- If a field is set to `'MV'` or `'MB'`, registration cannot proceed until data is provided.

---

## 4. Resource & Service Selection Engine

### 4.1 Provider Role Allocations (`Patient_Visit_Resources`)
When assigning providers during registration:
- **`AD` (Attending Doctor)**: Mandated for every Consultation Visit. Controls EMR Caseload ownership.
- **`CD` (Consulting Doctor)**: Added when patient requires secondary cross-speciality opinion.
- **`RD` (Referring Doctor)**: Logs the internal or external referrer for incentive calculations and referral letters.

### 4.2 Auto-Loading Doctor Default Service
- Method: `RegistrationPartOneController.php@loadSelectedResourceDefaultServices`
- SQL Execution:
  ```sql
  SELECT TOP 1 rs.Resource_Service_Time_Slot, ser.Service_Serial_No, ser.Service_Description,
               sussdb.Service_USSDB_Serial_No, ucv.Universal_Code_Value
  FROM Resource res
  JOIN Resource_Service rs ON rs.Resource_Serial_No = res.Resource_Serial_No AND rs.Active_Status = 'A'
  JOIN Service ser ON ser.Service_Serial_No = rs.Service_Serial_No AND ser.Active_Status = 'A'
  JOIN Service_USSDB sussdb ON sussdb.Service_Serial_No = ser.Service_Serial_No AND sussdb.Active_Status = 'A'
  JOIN Universal_Code_Values ucv ON ucv.Universal_Code_Values_Serial_No = sussdb.Universal_Code_Values_Serial_No
  WHERE res.Resource_Serial_No = :resourceSno
    AND rs.IsDefault = 'Y'
  ```
- Automatically injects the doctor's default consultation code into the active visit services grid.

### 4.3 Consultation vs. Non-Consultation Visits
- **Consultation Visit (`Visit_Is_Non_Consultation = 'N'`)**:
  - Doctor is assigned as `AD`.
  - Service has `service_indicator = 'C'`.
  - Generates EMR clinical encounter and doctor queue token.
- **Non-Consultation Visit (`Visit_Is_Non_Consultation = 'Y'`)**:
  - Direct services for Laboratory, Radiology, Pharmacy, or Nursing dressing.
  - Consultation fee is suppressed (`Service_Base_Rate = 0.00` or consultation line omitted).
  - Automatically routes service requests directly to LIS/RIS worklists without doctor sign-off.

---

## 5. Insurance, TPA, Copay, Deductible & Coverage Engine

Managed primarily in `app/Http/Controllers/RegistrationInsuranceController.php` and `PlanMasterController.php`.

### 5.1 Plan Master Configuration Architecture (`Insurance_Plan_Department_Cover`)
Copays and deductibles are configured at the Universal Code Group / Department level:
- **`Percentage_Consulting_Service` (`copaypresentage`)**: Patient coinsurance percentage for consultation (e.g., 20%).
- **`Amount_Consulting_Service` (`copaye`)**: Fixed consultation copay amount (e.g., AED 25).
- **`Percentage_Non_Consulting_Service` (`deductpresentage`)**: Patient coinsurance percentage for investigations/procedures.
- **`Amount_Non_Consulting_Service` (`deductae`)**: Fixed investigation deductible.
- **`Limit_Value` (`limit`)**: Overall monetary spending ceiling under this group.
- **`PA_Limit_Value` (`Ipdc_PA_Limit_Value`)**: Pre-authorization threshold (e.g., any service exceeding AED 1,000 triggers mandatory pre-auth).
- **`Patient_Share_Limit` (`Ipdc_Pat_Share_Limit`)**: Maximum deductible cap per visit (e.g., patient never pays more than AED 50 copay per visit).
- **`Prior_Approval_Required` (`Ipdc_PA_Req`)**: 'Y' if this entire department/group requires pre-authorization.

### 5.2 Category Copays (`Insurance_Plan_Copay_Category_Link`)
Granular copays managed per clinical category:
- `InvCopayLimitPerc` & `InvCopayLimitAmt`: Investigation / Lab / Radiology copay % and max cap.
- `PharCopayLimitPerc` & `PharCopayLimitAmt`: Pharmacy medicine copay % and max cap.
- `PatVisLimit`: Patient out-of-pocket maximum limit across the entire visit.

### 5.3 Point-in-Time Visit Snapshot
When insurance is saved at registration (`patientInsuranceCreate`):
1. Plan rules from `Insurance_Plan_Department_Cover` are **cloned into `Patient_Visit_Insurance_Plan_Department_Cover`**.
2. Service exclusions are cloned into `Patient_Visit_Insurance_Plan_Excluded_Prior_Approval_Services`.
3. **Rationale**: Freezes the financial contract as of the visit date. Future changes to the plan master will not corrupt historical billing or claims.

### 5.4 Excluded Services Logic
- Master: `Insurance_Plan_Excluded_Prior_Approval_Services` (`Excluded_Or_Prior_Approval_Flag = 'E'`).
- Manual Overrides: Front desk can check `cptckChkboxExc[]` to exclude specific services for this visit.
- Adjudication Effect:
  $$\text{Insurance Cover Amount} = 0.00, \quad \text{Patient Share Amount} = 100\% \text{ of Gross Price}$$

### 5.5 Prior Approval Trigger & Thresholds
A service is flagged as requiring pre-authorization (`Prior_Approval_Required_Flag = 'Y'`) if:
1. Marked with `'P'` in `Insurance_Plan_Excluded_Prior_Approval_Services`.
2. OR Department has `Prior_Approval_Is_Required = 'Y'` in `Insurance_Plan_Department_Cover`.
3. OR Service gross rate exceeds `PA_Limit_Value` and `Limit_Based_Approval_Applicable = 'Y'`.
4. OR Front desk manually flags `cptckChkboxReq[]`.

---

## 6. Patient Merging Workflow (Duplicate MRN Reconciliation)

### 6.1 Architectural Workflow
1. **Initiation**: Front desk detects duplicate patient profiles and opens Merge Modal (`RegistrationPartTwoController@checkDetailsForpatientMerge`).
2. **Identification**:
   - `frompbdsno`: Duplicate patient to be merged and retired.
   - `topbdsno`: Target patient to retain permanent identity.
3. **Audit Log Persistence**:
   - Inserts record into `Patient_Basic_Details_Link_Merging`:
     ```sql
     INSERT INTO Patient_Basic_Details_Link_Merging (
         From_Patient_Basic_Details_Serial_No,
         To_Patient_Basic_Details_Serial_No,
         Patient_Type,
         To_Family_Relationship_Code,
         Patient_Is_Duplicate,
         Default_MRN_No_To_Search,
         Active_Status
     ) VALUES (:frompbdsno, :topbdsno, 'I', 'SELF', 'Y', 'Y', 'A')
     ```
4. **Relational Cascading**:
   - Re-points all foreign keys from `frompbdsno` to `topbdsno`:
     - `Patient_Visit_Basic_Details.Patient_Basic_Details_Serial_No`
     - `Patient_Appointment.Patient_Basic_Details_Serial_No`
     - `Patient_Billing.Patient_Basic_Details_Serial_No`
     - `EMR_Patient_Visit_Summary.Patient_Basic_Details_Serial_No`
     - `Patient_Visit_LIS_Services` & Lab test history
     - `Patient_Visit_RIS_Services` & Radiology imaging history
5. **Retirement**:
   - Updates `Patient_Basic_Details.Active_Status = 'D'` for the source patient, ensuring it no longer appears in routine search results.

---

## 7. Replication & Carry-Forward Scenarios

### 7.1 Previous Visit Insurance Carry-Forward (`loadPreviousVisitPayment`)
- Controller: `DRP/QuickRegistrationController.php@loadPreviousVisitPayment`
- Carries forward:
  - `Insurance_Company_Serial_No`, `Associate_Company_Insurance_Company_Serial_No` (TPA)
  - `Insurance_Plan_Serial_No`, `Patient_Income_Network_Serial_No`
  - `Insurance_Card_No`, `Card_Expiry_Date`, `Policy_Number`
  - Copay percentages and deductible caps
  - Secondary insurance company and network details

### 7.2 Prior Visit Approval Carry-Forward (`loadPreviousPriorVisitPaymentDetails`)
- If appointment or current visit is linked to an approved Prior Authorization:
  - System extracts `Authorization_Reference_No`, approved service codes, and authorized quantities.
  - Automatically sets `Insurance_Prior_Approval_Status = 'A'` on current visit services.
  - **Suppression Mechanism**: Restricts the system from re-transmitting pre-authorization claims to insurance payer, eliminating duplicate claim denials.

### 7.3 Chronic Diagnosis Carry-Forward (ICD-10)
- Method: `addICDFromHimesVisitSummaryService`
- Fetches active primary and secondary ICD-10 diagnosis codes from previous encounter and replicates them into current `Patient_Visit_Diagnosis`.

### 7.4 Treatment Plan Conversion
- Method: `AddRegPendingServicetoTreatmentPlan`
- Pulls planned dental/physio/surgical items from `Patient_Treatment_Plan` into active `Patient_Visit_Services`.

---

## 8. Visit Types & Follow-Up Transition Rules

### 8.1 Visit Types:
- **`N` (New Visit)**: Initial consult encounter.
- **`F` (Free Follow-up)**: Zero-charge consult within validity window.
- **`P` (Paid Follow-up)**: Discounted consult beyond free follow-up window.
- **`R` (Repeat Visit)**: Chronic medication refill or routine review.

### 8.2 Transition Validation Algorithm (`loadServicesBasedOnVisitType`):
When user changes visit type:
1. Calculates days elapsed since initial consultation:
   $$\Delta \text{Days} = \text{Current Visit Date} - \text{Last New Visit Date}$$
2. Checks completed follow-ups:
   $$\text{Followup Count} = \text{Count of completed visits with } \text{Followup\_Status} = 'F' \text{ against that New Visit}$$
3. Evaluates eligibility against `Branch`:
   - If $\Delta \text{Days} \le \text{Free\_Follow\_Up\_Days}$ AND $\text{Followup Count} < \text{No\_Of\_Free\_Follow\_Up\_Visits}$:
     - **Allowed**: Follow-up type set to `'F'`. Queries `Branch_Free_Paid_Followup_Services` to load mapped free service code.
   - Else:
     - **Blocked**: System rejects Free Follow-up, alerting user that validity has expired, and forces selection of Paid Follow-up (`'P'`) or New Visit (`'N'`).

---

## 9. Check-In, Visit Creation & Prior Approval Flow

```
┌─────────────────────────────────┐
│     Front Desk Registration     │
│   (createVisitForAppointment    │
│    or postQuickRegistration)    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│       Visit Created ('Y')       │
│  Patient_Visit_Basic_Details    │
│    Token Number Generated       │
└────────────────┬────────────────┘
                 │
         Check Service Types
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐   ┌──────────────────────────────┐
│ Prior Auth   │   │ Already Approved or          │
│ Required?    │   │ Routine Consultation?        │
└───────┬──────┘   └──────────────┬───────────────┘
   YES  │                         │ NO
        ▼                         ▼
┌──────────────────────┐   ┌──────────────────────┐
│ Create Prior Visit   │   │ Route Directly to    │
│ (PA_Patient_Visit_   │   │ Doctor EMR Caseload  │
│  Basic_Details)      │   │ & Service Worklists  │
└──────────────────────┘   └──────────────────────┘
```

### 9.1 Service Deletion Restriction Rules
A service in `Patient_Visit_Services` **CANNOT** be cancelled or deleted if:
1. **Invoiced / Billed**: `Is_Service_Billed = 'Y'` (`removeAddedService`).
2. **Laboratory Processing Started** (`getlisparameterstatuscancelservice`):
   - Status in `['SK', 'TP', 'RE', 'RT', 'TA', 'PR', 'TD', 'TT']` (Sample collected, Test in progress, Results entered, or Reports printed).
3. **Radiology Exam Initiated**: Study completed or accession number locked in RIS worklist.
4. **Prior Authorization Active**: Pre-auth claim submitted to payer and in pending review or approved state.
5. **Visit Checked Out**: `Visit_Is_Checkedout = 'Y'`.

---

## 10. Privileges, Conditions & Edit Lockouts

The registration interface enforces rigid read-only lockouts under any of the following operational conditions:

| Lockout Scenario | Database Trigger / Field Condition | Operational & Compliance Rationale |
| :--- | :--- | :--- |
| **1. Visit Checked Out** | `Patient_Visit_Basic_Details.Visit_Is_Checkedout == 'Y'` (`checkPrevVstCheckout`) | Encounter concluded; clinical liability closed. Re-opening requires administrative override. |
| **2. Patient Discharged** | `Patient_Visit_Basic_Details.Discharge_Date_Time IS NOT NULL` | Inpatient discharged; bed vacated; gate pass generated. |
| **3. Invoice Generated** | `Patient_Billing` invoice finalized | Financial audit lockout; modifications must occur via Credit/Debit Notes. |
| **4. E-Claim XML Batched** | `XML_File_Creation` claim batch submitted | Insurance claim batched for DHA/Waseel submission. Modifying visit invalidates claim hash. |
| **5. Cancelled Visit** | `Patient_Visit_Basic_Details.Visit_Cancellation_Flag == 'Y'` | Visit officially voided. |
| **6. User Privilege Denied** | Function ID permission revoked (`functions.patientregistration.id`) | Role-based access control prevents unauthorized staff from modifying registration data. |

---

## 11. Core Code Locations Reference

| Component | File Path |
| :--- | :--- |
| **Quick Registration Controller** | `app/Http/Controllers/DRP/QuickRegistrationController.php` |
| **Quick Registration Service** | `app/Services/QuickRegistrationService.php` |
| **Detailed Registration Tab Controller** | `app/Http/Controllers/RegistrationTabController.php` |
| **Core Demographics Controller** | `app/Http/Controllers/RegistrationController.php` |
| **Registration Part One Controller** | `app/Http/Controllers/RegistrationAppointmentPartOneController.php` |
| **Registration Part Two Controller** | `app/Http/Controllers/RegistrationPartTwoController.php` |
| **Insurance Engine Controller** | `app/Http/Controllers/RegistrationInsuranceController.php` |
| **Plan Master Controller** | `app/Http/Controllers/PlanMasterController.php` |
| **Insurance Plans Master Controller** | `app/Http/Controllers/InsuranceplansController.php` |
| **Follow-up Services Master** | `app/Http/Controllers/BranchFreePaidFollowupServicesController.php` |
| **Patient Merging Controller** | `app/Http/Controllers/PatientMergedMRNNOController.php` |
| **Routes** | `routes/controllers/Registration.php` & `RegistrationInsurance.php` |
| **Configuration Schema** | `config/registration.php`, `config/application.php`, `config/aps.php` |

---

## 12. Operational Mandate: Architecture/SOP Inquiries vs. Live Transaction Database Execution

An AI agent working with the Patient Registration Module MUST strictly distinguish between **Conceptual Workflow Queries** and **Operational Transaction Queries**:

### 12.1 Conceptual Workflow & SOP Queries (Served by Valkey & ChromaDB)
- **Examples**:
  - *"How does patient registration work in HIMES?"*
  - *"What is the difference between Simple Registration and Detailed Registration?"*
  - *"How are copay and deductible calculated for insurance plans?"*
  - *"What are the service deletion restriction rules?"*
  - *"When does a visit screen get locked or read-only?"*
- **Execution Flow**:
  - Retrieve authoritative rules instantly from **Valkey** (`himes:flow:registration_workflow`) and **ChromaDB** (`agent_knowledge_base`).
  - **In User Mode (Default View)**: Explain the clinical and front-desk journey in simple, clean, intuitive hospital business language. NEVER output raw SQL table names (`Patient_Basic_Details`, `Patient_Visit_Basic_Details`, `Insurance_Plan_Department_Cover`), column primary keys, or raw code.
  - **In Developer Mode**: Present full technical diagnostics including exact table relationships, controller methods, routes, and JSON schema.

### 12.2 Operational & Transactional Queries (Mandatory Live MSSQL Execution)
- **Examples**:
  - *"How many patients registered today?"* / *"Inaikki evlo patients register aagirukaanga?"*
  - *"Check registration and insurance details for MRN 3004383."*
  - *"Is patient Prakash registered yesterday?"*
  - *"Show me all emergency (ER) visits registered today."*
  - *"Find duplicate patient profiles for Emirates ID 784-1988-1234567-1."*
- **Mandatory 5-Step Live Data Execution Flow**:
  1. **Understand Workflow**: Identify the relevant tables (`Patient_Basic_Details`, `Patient_Basic_Encript_Details`, `Patient_Visit_Basic_Details`, `Patient_Visit_Insurance_Card_Details`, `Patient_Visit_Resources`, `Patient_Identification_Details`).
  2. **Review Code / Controller**: Check controller queries (`QuickRegistrationController.php`, `RegistrationController.php`) to confirm exact status flags (`Active_Status = 'A'`, `Visit_Cancellation_Flag = 'N'`).
  3. **Prepare Exact SQL Query**: Formulate a safe, read-only MSSQL `SELECT` query with `WITH(NOLOCK)` using exact equality for dates, MRNs, and IDs.
  4. **Fetch Live Database Records**: Execute via `execute_select_sql` against the live MSSQL database.
  5. **Analyze & Present**: Analyze the returned rows and output clean, structured, factual details (MRN Number, Patient Name, Visit No, Registration Time, Insurance Plan, Doctor) in the user's exact query language. NEVER output generic workflow text when live operational data is requested!
