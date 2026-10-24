---
name: appointment-workflow
description: >-
  Comprehensive guide and reference for the HIMES Appointment Scheduling & Patient Journey Workflow.
  Covers all entry points (ASM Scheduler, Global View, Front Desk, EMR Caseload, Prior Visit, OT Scheduler, APIs),
  Resource & Speciality master configurations, Doctor Operating Hours & Non-Availability (leaves/breaks),
  Free vs Paid Followup calculation rules (Branch_Free_Paid_Followup_Services), SMS & Email template delivery engines,
  Recurring appointment patterns, Status lifecycle & Color code mappings, Prior Visit conversion,
  Visit Registration flows, Validation rules, and Patient Search mechanics.
---

# HIMES Appointment Workflow & Architecture Specification

This skill documents the complete, end-to-end **Appointment Management and Scheduling System** in HIMES (Hospital Information Management Enterprise System). It serves as the authoritative, definitive reference for developers, support engineers, healthcare workflow architects, and AI agents.

---

## 1. System Overview & Architecture

The Appointment Scheduling Module (ASM) in HIMES manages outpatient scheduling, provider time allocation, multi-resource linking, recurring bookings, and conversion to live hospital visits (OP/IP).

### Key Architectural Layers:
- **Presentation Layer (Blade & FullCalendar)**:
  - `resources/views/ASM/appointmentSchedular.blade.php`: Visual drag-and-drop calendar (Day, Week, Month, Resource view).
  - `resources/views/ASM/patientAppointment/appointment.blade.php`: Modal appointment booking & modification form.
  - `resources/views/aps/apsmanagement/global_view_of_all_appointment.blade.php`: Tabular multi-resource enterprise queue.
  - `resources/views/registration/regBookedAppointment.blade.php`: Front desk receptionist visit conversion screen.
- **Controller Layer (Business Logic)**:
  - `app/Http/Controllers/ASM/appointmentSchedularController.php`: Core scheduler events, doctor time-slots, patient search.
  - `app/Http/Controllers/ASM/patientAppointmentController.php`: Booking persistence, SMS/Email triggers, recurring logic, status transitions.
  - `app/Http/Controllers/GlobalViewAppointmentController.php`: Global view management, status updates, visit redirection.
  - `app/Http/Controllers/RegistrationAppointmentPostController.php`: Converting appointment into active patient visits (`Patient_Visit_Appointments`).
  - `app/Http/Controllers/BranchFreePaidFollowupServicesController.php`: Follow-up services master management.
- **Database Tables**:
  - Primary: `Patient_Appointment`, `Patient_Visit_Appointments`, `Appointment_Merge_Counter`, `Recurring_Patient_Appointment_Details`.
  - Master & Config: `Resource`, `Resource_Parent`, `Resource_Service`, `Resource_Service_Operating_Hours`, `Resource_Parent_Operating_Hours`, `Resource_Non_Availability`, `Speciality`, `Speciality_Sub_Department_Branch`, `Branch_Free_Paid_Followup_Services`, `Appointment_Status_Type`, `Branch_Based_SMS_Template`, `Branch_Based_Email`.

---

## 2. Appointment Booking Entry Points (Where All Appointments Can Be Booked)

HIMES supports 8 distinct entry points for creating and managing appointments:

| Entry Point | Route / URL | Controller Method | Description |
| :--- | :--- | :--- | :--- |
| **1. ASM Calendar Scheduler** | `/appointmentScheduler` | `appointmentSchedularController@viewAppointmentSchedular` | Interactive FullCalendar grid. Staff selects vacant slot, drags/drops, resizes, and books. |
| **2. Patient Appointment Screen** | `/patientAppointment` | `PatientAppointmentController@viewPatientAppointmentDetails` | Standard form-based single patient appointment screen. |
| **3. Global View of Appointments** | `/viewGlobalAppointment` | `GlobalViewAppointmentController@getViewGlobal` | Enterprise multi-resource list with status filtering, bulk confirmations, and register shortcuts. |
| **4. Front Desk Registration** | `/quickRegistration` & `/regBookedAppointment` | `QuickRegistrationController` & `RegistrationAppointmentController` | Receptionist pulls up booked appointments and registers patient into a live OP Visit on arrival. |
| **5. Doctor Consultation / EMR Caseload** | `/doctorConsultation` / EMR Caseload | `EMRCaseloadListController` / `PatientAppointmentController` | Doctors create follow-up appointments during consultation or from Treatment Plan. |
| **6. OT Scheduler** | `/OTScheduler` | `OTSchedularController@viewOTSchedular` | Specialized surgical scheduling organized by Building -> Floor -> Unit -> Room -> Bed / OT Table. |
| **7. Prior Visit Module** | `/viewPriorVisit` / `/globalViewForPriorVisitNew` | `PriorVisitController` / `GlobalViewPriorVisitNewController` | Converts approved insurance prior authorization orders directly into booked appointments. |
| **8. Patient Portal & Mobile APIs** | `/api/patientPortal/...` & `/Okadoc/...` | `PatientPortalAppointmentWebServiceController` / `OkadocApis` | External patient booking via Web Portal, Mobile App, WhatsApp bot, or third-party platforms (Okadoc). |

---

## 3. Master Configurations: Resource, Speciality & Operating Hours

The appointment scheduling engine relies on a hierarchical master data model to determine doctor schedules and slot availability.

### 3.1 Organization & Speciality Hierarchy
```
Company (Company)
   └── Branch (Branch)
         └── Department (Department -> Department_Branch)
               └── Sub-Department (Sub_Department)
                     └── Speciality (Speciality -> Speciality_Sub_Department_Branch)
                           └── Resource (Resource -> Resource_Parent)
```
- **`Speciality`**: Holds medical specialities (e.g., Cardiology, Dental, Orthopedics). Linked to Sub-Department and Branch via `Speciality_Sub_Department_Branch` (`ssdb`).
- **`Resource_Parent`**: Represents the physical doctor / practitioner or room (e.g., Dr. John Smith).
- **`Resource`**: Individual service delivery node. Each `Resource` points to a `Resource_Parent_Serial_No` and a `Speciality_Sub_Department_Branch_Serial_No`.
- **`Appointment_Default_Speciality`**: (`ASM/AppointmentDefaultSpecialityController`) allows configuring default specialities per branch or user login so doctors immediately see their own calendar upon login.

### 3.2 Doctor Operating Hours & Availability Calculation
Doctor operating hours and slot times are derived hierarchically in `appointmentSchedularController.php@getAllEventsData`:

1. **Specific Doctor Working Hours (`Resource_Parent_Operating_Hours` & `_WeekDay`)**:
   - `Resource_Availability_Start_Date` to `Resource_Availability_End_Date`.
   - `Resource_Availability_Start_Time` and `Resource_Availability_END_Time`.
   - Mapped by `WeekDay` (1 = Sunday, 2 = Monday, etc.).
2. **Resource Service Operating Hours (`Resource_Service_Operating_Hours` on `Resource_Service`)**:
   - `Resource_Service_Day_of_Week`: Specific day of week.
   - `Resource_Service_Operating_Hour_Start_Time` / `Resource_Service_Operating_Hour_End_Time`.
   - `Resource_Service_Time_Slot`: Slot interval in minutes (e.g., 15 mins, 20 mins, 30 mins).
3. **Branch Operational Fallback (`Branch` table)**:
   - If doctor operating hours are not explicitly defined, the calendar bounds fall back to `Branch.Branch_Operational_Start_Time` and `Branch.Branch_Operational_End_Time`.
4. **Doctor Non-Availability / Leaves / Breaks (`Resource_Non_Availability`)**:
   - Defines periods when the doctor is unavailable:
     - `Resource_Non_Availability_Start_Date_Time`
     - `Resource_Non_Availability_End_Date_Time`
     - `Reason_Code` (Leave, Emergency, Surgery, Break).
   - In `patientDetailsController.php`:
     ```php
     $isTimeOutsideBreak = ($AppEndTime > $ResStartTime && $AppStartTime < $ResEndTime);
     ```
     If an appointment overlaps with a non-availability record, slot booking is blocked.

---

## 4. Free Follow-Up vs Paid Follow-Up Master Configurations

In HIMES, follow-up appointments and services are determined by two separate layers: **Eligibility Limits** and **Service Mapping**.

### 4.1 Follow-Up Eligibility Rules & Limits
Configured in `Branch`, `Installation_Parameters`, and `Insurance_Company_Followup`:

| Master Parameter | Field Name | Description |
| :--- | :--- | :--- |
| **Cash Free Follow-Up Days** | `Free_Follow_Up_Days_For_Cash_Patients` | Number of calendar days from initial consultation within which cash patients receive free follow-up (e.g., 7 or 14 days). |
| **Cash Free Follow-Up Visits** | `No_Of_Free_Follow_Up_Visits_For_Cash_Patients` | Maximum number of free follow-up visits allowed within the validity window (typically 1 visit). |
| **Insurance Free Follow-Up Days** | `Free_Follow_Up_Days_For_Insured_Patients` | Number of days valid for insurance patients (per payer rules, e.g., 7 days). |
| **Insurance Free Follow-Up Visits** | `No_Of_Free_Follow_Up_Visits_For_Insured_Patients` | Max free visits allowed for insured patients. |
| **Paid Follow-Up Limits** | `Paid_Follow_Up_Days_For_...` & `No_Of_Paid_Follow_Up_Visits_For_...` | Grace period and visit count for discounted paid follow-up visits before reverting to New Visit consultation rates. |

### 4.2 Branch Free & Paid Follow-Up Services Master (`Branch_Free_Paid_Followup_Services`)
Managed via `BranchFreePaidFollowupServicesController` (`/viewBranchFreePaidFollowupServices`):
- **Table**: `Branch_Free_Paid_Followup_Services`
- **Fields**:
  - `Branch_Code`
  - `Speciality_Code`
  - `Service_USSDB_Serial_No` (The specific consultation service)
  - `Paid_Free_Service_Status`:
    - `'F'` = FREE FOLLOWUP
    - `'P'` = PAID FOLLOWUP
    - `'R'` = REVISIT
  - `Visit_Encounter_Type_Serial_No`
  - `Active_Status`

### 4.3 Service Allocation Logic During Booking:
In `appointmentSchedularController.php@getDefaultServiceForAppointmentResource`:
- When booking a **NEW VISIT** (`type == 'new'`):
  - Fetches default service from `Resource_Service` where `rs.IsDefault = 'Y'`.
- When booking a **FREE FOLLOWUP** (`ApptType == 'F'`) or **PAID FOLLOWUP** (`ApptType == 'P'`):
  - Queries `Branch_Free_Paid_Followup_Services`:
    ```sql
    select Top 1 ucv.Universal_Code_Value, ser.Service_Description, sussdb.Service_USSDB_Serial_No
    from Branch_Free_Paid_Followup_Services BFPFS
    where BFPFS.Branch_Code = :branch
      and BFPFS.Speciality_Code = :speciality
      and BFPFS.Paid_Free_Service_Status = :apptType
      and BFPFS.Active_Status = 'A'
    ```
  - Automatically loads the configured follow-up service and price schedule.

---

## 5. SMS & Email Notification Workflows & Templates

HIMES triggers automated communications upon appointment booking, rescheduling, cancellation, or reminders.

### 5.1 SMS Processing Flow
- **Controller**: `ASM/patientAppointmentController.php@sendSMSonCheck`
- **Execution Engine**: `$this->appointmentSMSService->PatientPortalAPPointmentsendSMSonCheck(...)`
- **Master Tables**:
  - `Branch_Based_SMS`: Holds branch level SMS gateway credentials, active languages (`Language_Code`: `'EN'`, `'AR'`).
  - `Branch_Based_SMS_Template`: Template content mapped by `Module_Id = 'APS'` and `Appointment_Status_Type_Code` (`CF`, `PD`, `WF`, `CX`).
  - `Patient_Basic_Notification` & `Patient_Basic_Notification_Modules_Link`: Tracks patient DND (Do Not Disturb) and communication channel preferences.
- **Dynamic Tokens Replaced in Template**:
  - `{{Patient_Name}}`, `{{Doctor_Name}}`, `{{Appointment_Date}}`, `{{Appointment_Time}}`, `{{Branch_Name}}`, `{{Branch_Phone}}`, `{{Token_Number}}`.

### 5.2 Email Processing Flow
- **Controller**: `ASM/patientAppointmentController.php@sendEmailonCheck`
- **Master Table**: `Branch_Based_Email`
- **Fields**: `Branch_Based_Email_Serial_No`, `Email_Subject`, `Email_Content`, `Branch_Code`.
- **Placeholder Replacement**:
  - Uses `preg_match_all("/{{(.*?)}}/", $content, $m)` and calls `$this->getPatientDBValue($varname, $patient_ser_no, $Patient_Appointment_Serial_No, $userBaseBranch)` to replace tokens dynamically with patient MRN, doctor, and date/time.

---

## 6. Recurring Appointment Workflow

HIMES supports booking recurring treatment cycles (e.g., Physiotherapy rehabilitation, Dental orthodontics, Dialysis, Chemotherapy).

### 6.1 Recurrence Options & Patterns
Handled in `ASM/patientAppointmentController.php` (lines 7080–7220) and `ASM/patientDetailsController.php`:
1. **Every Day / Days of Week (`Recurringapptype == 'ED'`)**:
   - User picks a Start Date and End Date.
   - User selects specific weekdays: `1=Sat`, `2=Sun`, `3=Mon`, `4=Tue`, `5=Wed`, `6=Thu`, `7=Fri`.
   - System loops from `recurringstartdate` to `recurringenddate` matching selected weekdays.
2. **Custom Multiple Dates Selection**:
   - User provides a comma-separated list of discrete calendar dates (`multiplerecurringappointmentDate`).

### 6.2 Conflict Detection & Database Linking
- For every date generated in the recurring series:
  - System checks `Resource_Non_Availability` (doctor leaves/breaks). Dates with conflicts are flagged or skipped.
  - System increments `Order_Sequence` from `Recurring_Patient_Appointment_Details`.
  - Master entry inserted in `Recurring_Patient_Appointment_Details`.
  - Individual appointment rows inserted into `Patient_Appointment` with `Recurring_Order_Sequence` linking back to the recurrence group.

---

## 7. Status Lifecycle & Color Coding Master

On the appointment scheduling views, every card is visually color-coded based on status, resource type, and patient type.

### 7.1 Status Types, Color Codes & Meanings
Defined in `config/applicationsetting.php` (`new_color` & `Appointment_Status`) and `getAllEventData.blade.php`:

| Status Code | Status Name | Hex Color | Visual Meaning | Trigger / Transition Point |
| :---: | :--- | :---: | :--- | :--- |
| **`CF`** | **CONFIRMED** | `#2BD790` | Mint Green | Appointment is confirmed. Doctor and slot are locked for the patient. |
| **`PD`** | **PENDING** | `#92BDF9` | Soft Sky Blue | Initial tentative booking from portal/web/phone awaiting confirmation or payment. |
| **`WF`** | **WAITING LIST** | `#E1C8E1` | Lavender / Light Purple | Slot quota exceeded. Patient placed in queue for cancellations. |
| **`NS`** | **NO SHOW** | `#EDB917` | Golden Amber | Patient did not arrive within grace period (e.g., 15–30 mins past start time). |
| **`CX`** | **CANCELLED** | `#F6DCAB` | Muted Sand / Wheat | Appointment cancelled by patient or staff. Reason logged in `Cancelled_Reason`. |
| **`REG`** | **REGISTERED** | `#948e79` | Grey / Olive Drab | Patient arrived and front desk converted appointment into an active Visit (`Patient_Visit_Appointments`). |
| **`REF`** | **REFERENCE RESOURCE** | `#C8EB02` | Lime Green | Appointment has a secondary/assisting resource linked (`Reference_Resource_Serial_No`). |

### 7.2 Patient Type Highlights
- **`NP` (New Patient)**: No permanent MRN yet. Displayed with Temporary MRN (`TMP10234`) and CSS class `NPHighlight`.
- **`EP` (Existing Patient)**: Has Permanent MRN (`PMP10234`) and CSS class `EPHighlight`.

### 7.3 How Status Changes from Pending (`PD`) to Confirmed (`CF`):
1. **Manual Staff Confirmation**: Staff clicks "Confirm" or selects `CF` in appointment modal dropdown.
2. **API Endpoint**: `ASM/patientAppointmentController.php@getStatusChangePendingtoConfirm` executes:
   - Updates `Appointment_Status_Type_Code = 'CF'` in `Patient_Appointment`.
   - If resource is a `BED`, calls `ReserveBedForPatient(...)` to reserve inpatient bed.
   - If reference/linked resources exist, cascades `CF` to all secondary resource appointments.
3. **Automatic Waiting List Promotion**: In `autoCompleteController.php` (lines 2143 & 2253), when an existing confirmed appointment is cancelled (`CX`), the earliest waiting list appointment (`WF`) for that doctor slot is **automatically promoted to `CF`**!

---

## 8. Prior Visit <-> Appointment Workflow

In GCC insurance healthcare systems (UAE DHA/DoH/Thiqa, KSA CCHI/Waseel), specialized procedures, dental treatments, and surgeries require Prior Authorization (PA) before treatment.

```
┌─────────────────────────────────┐
│     Patient Needs Surgery/      │
│      Specialized Procedure      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐       Insurance Approval       ┌─────────────────────────────────┐
│    Create Prior Visit (PA)      │ ─────────────────────────────> │       PA Approved ('A')         │
│  (PA_Patient_Visit_Basic_Details│                                └────────────────┬────────────────┘
│   & Insurance Pre-Auth Claims)  │                                                 │
└─────────────────────────────────┘                                                 ▼
                 ▲                                                 ┌─────────────────────────────────┐
                 │                                                 │   Book Appointment Against PA   │
                 │ Cancel / Revert                                 │ (PriorVisitAppointmentDetails   │
                 │                                                 │  & addPriorVisitServicetoAppt)  │
┌────────────────┴────────────────┐                                └────────────────┬────────────────┘
│   Appointment Cancelled / Void  │ <───────────────────────────────────────────────┘
│  (callPriorVisitCancellation)   │
└─────────────────────────────────┘
```

1. **Appointment to Prior Visit**:
   - If a procedure requires insurance approval, staff creates a Prior Visit record (`PA_Patient_Visit_Basic_Details` and `PA_Patient_Visit_Services`). Pre-authorization claims are submitted to payer.
2. **Prior Visit to Appointment**:
   - Once insurance returns approval (`Insurance_Prior_Approval_Status` = 'A'):
   - Front desk opens `/viewPriorVisit` and triggers `PriorVisitAppointmentDetails` (`PatientAppointmentController.php@PriorVisitAppointmentDetails`).
   - Approved services, pre-auth codes, copay details, and patient demographics are loaded into the Appointment Scheduler to lock in provider surgical time.
3. **Prior Visit Cancellation Guard**:
   - If an appointment tied to an approved PA is cancelled, `checkPriorVisitApprovalStatus` verifies whether authorization was already granted (`['D', 'M', 'A']`). If so, `callPriorVisitCancellation` updates or reverts the insurance authorization lifecycle.

---

## 9. Appointment to Visit Registration Flow

When a patient arrives at the hospital, the booked appointment is converted into a live Registered Visit (`Patient_Visit_Basic_Details`).

### Step-by-Step Transition:
1. **Reception Trigger**:
   - In Global View or ASM Calendar, receptionist clicks "Register" (`/registerAppointment/{app_id}`).
   - Handled in `GlobalViewAppointmentController.php@getRegsiterForAppointment`:
     - Populates session with appointment data: `registration.Patient_Basic_Details_Serial_No`, `registration.Patient_Appointment_Serial_No`, `registration.Patient_Resource_Serial_No`, `registration.Patient_Appointment_Date`, `registration.Patient_Appointment_Start_Time`.
     - Redirects user to `/patientRegistration`.
2. **Visit Creation & Linking**:
   - In `RegistrationAppointmentPostController.php@createVisitForAppointment`:
     - Creates/Updates `Patient_Visit_Basic_Details` (`Is_Patient_Visit_Registered = 'Y'`).
     - Generates token number (`generateToken`) if queue token system is enabled.
     - Adds consulting service to `Patient_Visit_Services` and allocates provider in `Patient_Visit_Resources`.
     - Inserts linking row into **`Patient_Visit_Appointments`**:
       ```sql
       INSERT INTO Patient_Visit_Appointments
       (Patient_Visit_Basic_Details_Serial_No, Patient_Appointment_Serial_No, ...)
       VALUES (:vis_basic_sno, :pat_app_sno, ...)
       ```
3. **Visual Status Update**:
   - In the appointment scheduler, the appointment now has an active visit linked (`Patient_Visit_Appointments_Serial_No IS NOT NULL`).
   - Color shifts to **`#948e79`** with label **`REGISTERED`**.

---

## 10. Validations Engine

Before saving any appointment, HIMES enforces strict clinical and administrative validations:

1. **Single Slot Collision Check (`checkAppointmentAvailability` & `confirmAppointmentSlotAvailability`)**:
   - Configured via `Branch_Based_Settings.Appointment_Required_Single_Slot` ('Y'/'N').
   - When 'Y': Verifies that no other appointment in status `CF`, `PD`, or `WF` overlaps with requested `Appointment_Start_Time` and `Appointment_End_Time` for that `Resource_Parent_Serial_No`.
   - If overlap exists: returns `"SingleNotAvail"` and prevents double booking.
2. **Quota & Capacity Check (`Max_Appointments_Per_Day`)**:
   - Compares total booked count against `Appointment_Status_Type.Max_Appointments_Per_Day`.
   - If slot is saturated, prompts user to place patient on Waiting List (`WF`) or blocks booking.
3. **Doctor Leave / Non-Availability Guard (`Resource_Non_Availability`)**:
   - Blocks appointments during doctor leaves, breaks, or hospital meetings.
4. **Duplicate Same-Day Appointment Guard (`getExistingPatientDuplicateSameDaySameRes`)**:
   - Prevents booking the same patient with the same doctor more than once on the same calendar day unless explicitly overridden.
5. **Operating Hours Boundary Validation**:
   - Rejects appointments scheduled outside provider working hours or branch operational hours.
6. **Mandatory Patient Demographics**:
   - Validates First Name, Mobile Phone (validated against country dial codes), Gender, and Branch.
7. **Follow-Up Expiry Guard**:
   - Verifies whether patient's previous visit is still within the configured `Free_Follow_Up_Days`. If expired, rejects Free Follow-up and mandates Paid Follow-up or New Visit.

---

## 11. Patient Search Flows

HIMES supports both rapid auto-suggest and advanced demographic searches:

1. **Quick Auto-Suggest Search**:
   - Triggered as user types 3+ characters in the scheduler search box (`getAllAppointmentPatientSearch`).
   - Searches across: Permanent MRN (`PMP...`), Temporary MRN (`TMP...`), Patient First/Last Name, and Mobile Number.
2. **Advanced Demographic Search (`advPatientSearchDetailsAppointment`)**:
   - Available via search modal when patient is not immediately found.
   - Filter criteria:
     - Full Name (First, Middle, Last)
     - Mobile / Phone Number
     - Emirates ID / National ID (`Emirates_Id`)
     - Date of Birth (`Patient_DOB`)
     - Passport Number
   - Returns paginated list showing Photo, MRN, Age/Gender, and Contact info.
3. **Unregistered / Prospective Patients**:
   - If patient is new, staff inputs basic details directly into appointment form.
   - System registers prospective patient in `Patient_Basic_Details` with Temporary MRN (`TMP...`), allowing booking to proceed without full front-desk registration.

---

## 12. Quick Reference: Key Code Locations

| Component | File Path |
| :--- | :--- |
| **Scheduler Controller** | `app/Http/Controllers/ASM/appointmentSchedularController.php` |
| **Booking & Event Controller** | `app/Http/Controllers/ASM/patientAppointmentController.php` |
| **Auto-Complete & Status Logic**| `app/Http/Controllers/ASM/autoCompleteController.php` |
| **Patient Demography Controller**| `app/Http/Controllers/ASM/patientDetailsController.php` |
| **Global View Controller** | `app/Http/Controllers/GlobalViewAppointmentController.php` |
| **Visit Conversion Controller** | `app/Http/Controllers/RegistrationAppointmentPostController.php` |
| **Follow-Up Services Master** | `app/Http/Controllers/BranchFreePaidFollowupServicesController.php` |
| **Status Type Master Controller**| `app/Http/Controllers/AppointmentStatusTypeController.php` |
| **Scheduler Routes** | `routes/ASM/appointmentSchedular.php` |
| **Calendar Blade Template** | `resources/views/ASM/appointmentSchedular.blade.php` |
| **Modal Booking Form Blade** | `resources/views/ASM/patientAppointment/appointment.blade.php` |
| **Scheduler Event Rendering** | `resources/views/ASM/getAllEventData.blade.php` |
| **Color & Status Settings** | `config/applicationsetting.php` (`new_color`, `appointment_type`, `Appointment_Status`) |
| **APS Schema Config** | `config/aps.php` |

---

## 13. Operational Mandate: Architecture/SOP vs. Live Transaction Database Execution

An AI agent working with the Appointment Scheduling Module (ASM) MUST strictly distinguish between **Conceptual Workflow Queries** and **Operational Transaction Queries**:

### 13.1 Conceptual Workflow & SOP Queries (Served by Valkey & ChromaDB)
- **Examples**:
  - *"How does the appointment workflow work in this application?"*
  - *"What are the appointment status colors and codes?"*
  - *"Explain the free vs paid follow-up calculation rules."*
  - *"What happens when a confirmed appointment is cancelled?"*
- **Execution Flow**:
  - Retrieve authoritative workflow rules instantly from **Valkey** (`himes:flow:appointment_workflow`) and **ChromaDB** (`agent_knowledge_base`).
  - Explain the architecture, master tables, and business logic clearly without running redundant database queries.

### 13.2 Operational & Transactional Queries (Mandatory Live MSSQL Execution)
- **Examples**:
  - *"Is Dr. John available today?"* / *"Doctor John-ku inaikki appointment irukka?"*
  - *"How many appointments are booked for today?"*
  - *"Check the appointment status for MRN 3004383."*
  - *"Which doctors are on leave or break today?"*
  - *"Show me today's cancelled or waiting list appointments."*
- **Mandatory 5-Step Live Data Execution Flow**:
  1. **Understand Workflow**: Identify the relevant tables from the ASM schema (`Patient_Appointment`, `Resource_Parent`, `Resource_Non_Availability`, `Patient_Basic_Details`, `Patient_Basic_Encript_Details`, `Patient_Visit_Appointments`).
  2. **Review Code / Controller**: Check the corresponding controller logic (e.g. `appointmentSchedularController.php`, `GlobalViewAppointmentController.php`) to confirm exact status flags and filters (`Active_Status = 'A'`).
  3. **Prepare Exact SQL Query**: Formulate a safe, read-only MSSQL `SELECT` query with `WITH(NOLOCK)` using exact equality for dates, MRNs, and doctor IDs.
  4. **Fetch Live Database Records**: Execute via `execute_select_sql` against the live hospital MSSQL database.
  5. **Analyze & Present**: Analyze the actual returned rows and output clean, structured, factual details (Doctor Name, MRN, Appointment Time, Status, Token/Visit) in the user's exact query language. NEVER output generic workflow text when live data is requested!

