# 🏥 HIMES Application - Complete Dynamic Architectural Knowledge Base
> **Generated Date**: 2026-10-17 | **Discovery Mode**: 100% Dynamic Engine (Zero Hardcoded Modules)
> **Database**: Microsoft SQL Server (MSSQL) | **Application**: Laravel 12.x / PHP 8.2 | **ChromaDB Target**: Persistent Vector Store

## 📊 Architectural Executive Summary
- **Discovered Active Modules**: 44 modules from database `Module` table
- **Mapped Application Menus & Functions**: 1006 functions
- **Discovered Database Tables**: 2,550 base tables mapped across dynamic prefixes
- **Total Eloquent Models**: 453 models with primary keys, fillables & relationships
- **Total Controllers**: 1164 controllers with action methods & validation rules
- **Total Routes**: 12485 web & API routes mapped with middlewares
- **Total Services & Integrations**: 261 service & helper classes
- **Active Workflows**: 3 Events, 1 Listeners, 4 Background Jobs
- **Active Middlewares**: 23 Middlewares

---

## 📌 Module: Analytics Report (ID: ANR)

### 1. Module Overview & Navigation Structure
- **Module ID**: `ANR`
- **Module Name**: `Analytics Report`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (0 total):
*(Core background or reporting module - navigation managed dynamically via service or API)*

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Report_` (11 tables), `Reporting_` (1 tables)
- **Associated Tables Count**: 58 tables identified
- **Key Tables**: `Branch_Based_EMR_Panel_Report`, `Branch_Based_EMR_Panel_Report_Sub_Details`, `DHA_Report_Code`, `HP_Report_Template`, `Himes_Job_Reports`, `Himes_Reports_Schedule_Details`, `Himes_Reports_Schedule_Details_Logs`, `LIS_Custom_Report_Template`, `LIS_Custom_Report_Template_Branch_Mapping`, `LIS_Custom_Report_Template_Section`, `LIS_Report_Branch_Dept_Header_Footer`, `LIS_Report_Dispatch_Details`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `HimesReportsScheduleDetailsLogs` (`app/Models/HimesReportsScheduleDetailsLogs.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details_Logs` | **Primary Key**: `Himes_Reports_Schedule_Details_Logs_Serial_No`
- **Model**: `ReportBasedBranch` (`app/Models/ReportBasedBranch.php`)
  - **Database Table**: `Report_Based_Branch_Details` | **Primary Key**: `Report_Based_Branch_User_Details_Serial_No`
- **Model**: `HimesReportsScheduleDetails` (`app/Models/HimesReportsScheduleDetails.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details` | **Primary Key**: `Himes_Reports_Schedule_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(ReportFunctionURL)` [Key/Pivot: `Report_Function_URL_Serial_No`]
- **Model**: `ReportFunctionURL` (`app/Models/ReportFunctionURL.php`)
  - **Database Table**: `Report_Function_URL` | **Primary Key**: `Report_Function_URL_Serial_No`
- **Model**: `Himes_Job_Reports` (`app/Models/Himes_Job_Reports.php`)
  - **Database Table**: `Himes_Job_Reports` | **Primary Key**: `Himes_Job_Reports_Serial_No`

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `UserTestResultReportingConroller` (`app/Http/Controllers/UserTestResultReportingConroller.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getviewusertestresultreprting()`, `getaddusertestresultreprting()`
- **Controller**: `UserTestResultReportingController` (`app/Http/Controllers/UserTestResultReportingController.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getViewUserTestResultReportingprivilages()`, `getAddUserTestResultReporting()`, `getservicevalues()`, `gettemplatedetails()`
- **Controller**: `EmrRadiologyReportController` (`app/Http/Controllers/EmrRadiologyReportController.php`)
  - **Action Methods**: `emrRadiologyReportgeneration()`, `getEmrRadiologyReportReviewed()`
- **Controller**: `NewReportTemplateController` (`app/Http/Controllers/NewReportTemplateController.php`)
  - **Action Methods**: `NewaddReportTemplate()`, `Ristemlateeditor()`, `getriseditorval()`, `PatientvisitpayemtdetailsPanel()`, `viewPatientHeader()`, `patientpaymentdetailpanel()`, `newpatientpaymentdetailpanel()`, `MultipletemplateEdit()`
- **Controller**: `reportJRSController1` (`app/Http/Controllers/reportJRSController1.php`)
  - **Action Methods**: `reportJRS()`, `reportdownJRS1()`, `reportdownJRS2()`
- **Controller**: `EmrLabReportController` (`app/Http/Controllers/EmrLabReportController.php`)
  - **Action Methods**: `getemrlabreportparameter()`, `labReviewDetailsupdate()`, `viewHeaderforemrlisReport()`
- *(+69 more controllers handling Analytics Report)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/testReport` | `TestReportController` | `gettestReportDetails` | `web/api` |
| `GET` | `/Reportpdfgeneration` | `TestReportController` | `getreportpdfgeneration` | `web/api` |
| `GET` | `/generatePDFreport` | `TestReportController` | `viewgeneratipdf` | `web/api` |
| `GET` | `/reportpdfgenetationtest` | `TestReportController` | `postreportpdfgeneration` | `web/api` |
| `GET` | `/viewReportSchedule/{id?}` | `ReportScheduleController` | `getListReportSchedule` | `web/api` |
| `GET` | `/editReportSchedule/{id?}` | `ReportScheduleController` | `getEditReportSchedule` | `web/api` |
| `GET` | `/runScheduleJob/{id?}` | `ReportScheduleController` | `runScheduleJob` | `web/api` |
| `GET` | `/editStatusReportSchedule/{id?}` | `ReportScheduleController` | `getEditStatusReportSchedule` | `web/api` |
| `GET` | `/deleteReportSchedule/{id?}` | `ReportScheduleController` | `getDeleteReportSchedule` | `web/api` |
| `GET` | `/reportSchedule/{id?}` | `ReportScheduleController` | `getViewReportSchedule` | `web/api` |
| *...* | *+754 more routes mapped to Analytics Report* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `JasperReportDownloadForftp` (`app/Services/JasperReportDownloadForftp.php`)
  - Methods: `ReportDownloadForftp()`
- **Service**: `ReportGeneratorService` (`app/Services/ReportGeneratorService.php`)
  - Methods: `generateAndSend()`
- **Service**: `HimesReportService` (`app/Services/HimesReportService.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: APPLICATION (ID: APP)

### 1. Module Overview & Navigation Structure
- **Module ID**: `APP`
- **Module Name**: `APPLICATION`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Application Error Log, Application Masters, Appointment Default Speciality, Appointment Visit Questionnaire, Appointment Visit Questionnaire Type, Appointment-Status-Type, BED SERVICES, BULK PLAN LIMIT, Blood-Group, Blood-Pressure-Matrix
- **Discovered Sub-functions & Action Page Links** (130 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `APPERRLOG` | APPLICATION ERROR LOG | `viewApplicationErrorLog` | Application Error Log | - |
| `AMSTR` | Application Masters | `dashboard` | Application Masters | Manage Functional Configurations |
| `APPDEFSPEC` | Appointment Default Speciality | `viewAppointmentDefaultSpeciality` | Appointment Default Speciality | - |
| `APPSTATTYP` | APPOINTMENT STATUS TYPE | `appointmentStatusType` | Appointment-Status-Type | - |
| `VISITQUE` | APPOINTMENT VISIT QUESTIONAIRE | `viewAppointmentQuestionnaire` | Appointment Visit Questionnaire | - |
| `APPQUETYP` | APPOINTMENT VISIT QUESTIONNAIRE TYPE | `appointmentQstnType` | Appointment Visit Questionnaire Type | - |
| `BEDSERVICE` | Bed Service | `viewBedServices` | BED SERVICES | - |
| `BLOODGRP` | BLOOD GROUP | `bloodGroup` | Blood-Group | - |
| `PREMAT` | BLOOD PREASSURE MATRIX | `bloodPressureMatrix` | Blood-Pressure-Matrix | - |
| `SUGMAT` | BLOOD SUGAR MATRIX | `bloodSugarMatrix` | Blood-Sugar-Matrix | - |
| `INDMAT` | BODY MASS PONDERAL INDEX MATRIX | `bodyMassPonderalIndexMatrix` | Body-Mass -Ponderal-Index-Matrix | - |
| `TEMPMAT` | BODY TEMPERATURE MATRIX | `bodyTemperatureMatrix` | Body-Temperature-Matrix | - |
| `BSSDEPMAP` | BODYSITE SUBSITE SUBDEPARTMENT MAPPING | `previous_value` | BodySite SubSite Subdepartment Mapping | BODYSITE SUBSITE SUBDEPARTMENT MAPPING MASTER |
| `BRCFRPAFUS` | Branch Free Paid Followup Services | `viewBranchFreePaidFollowupServices` | Branch Free Paid Followup Services | - |
| `BLKPRCLSMG` | BULK PRICE LIST MANAGEMENT | `BulkPriceListManagement` | Bulk Price List Management | - |
| *...* | *+115 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Application_` (4 tables), `Drug_` (18 tables), `Drugs_` (1 tables), `Reason_` (1 tables)
- **Associated Tables Count**: 569 tables identified
- **Key Tables**: `AAA_Item_Drug_map`, `API_Request_Response_Log_Details`, `Adm_Drug_18032019`, `Adm_Drug_21032019`, `Adm_Drug_Covered`, `Alcohol_Attribute_Values`, `All_Master_Logs`, `Allergy_Attribute_Values`, `Allergy_Group`, `Allergy_Machine_Test_Code`, `Allergy_Type`, `Allergy_Type_Allergy_Name_Link`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `API_Request_Response_Log_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `API_Request_Response_Log_Details_Serial_No` | `bigint` | - | NO | - |
| `Url` | `varchar` | 250 | NO | - |
| `Method` | `varchar` | 6 | NO | - |
| `Page_type` | `varchar` | 100 | NO | - |
| `Request_headers` | `varchar` | -1 | NO | - |
| `Request_body` | `varchar` | -1 | NO | - |
| `Response_headers` | `varchar` | -1 | NO | - |
| `Response_body` | `varchar` | -1 | NO | - |
| `Status_code` | `nvarchar` | 100 | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| *...* | *+2 more columns* | | | |

### 3. Eloquent Models & Data Architecture
- **Model**: `UserBasedGlobalFilterDetail` (`app/Models/UserBasedGlobalFilterDetail.php`)
  - **Database Table**: `User_Based_Global_Filter_Details` | **Primary Key**: `User_Based_Global_Filter_Details_Serial_No`
  - **Fillable Attributes**: `User_Based_Global_Filter_Serial_No`, `Speciality_Code`, `Resource_Parent_Serial_No`, `Type`, `Created_By_User_ID`, `Created_Date_Time`, `Modified_By_User_ID`, `Modified_Date_Time`...
  - **Eloquent Relationships**: `belongsTo(UserBasedGlobalFilter)` [Key/Pivot: `User_Based_Global_Filter_Serial_No`], `belongsTo(Speciality)` [Key/Pivot: `Speciality_Code`], `belongsTo(ResourceParent)` [Key/Pivot: `Resource_Parent_Serial_No`], `belongsTo(DepartmentBranch)` [Key/Pivot: `Department_Branch_Serial_No`], `belongsTo(WorkflowServices)` [Key/Pivot: `Workflow_Services_Serial_No`]
- **Model**: `HimesAboutus` (`app/Models/HimesAboutus.php`)
  - **Database Table**: `Himes_Aboutus` | **Primary Key**: `Branch_Code`
- **Model**: `RIS_Screening_Lock_Patient` (`app/Models/RIS_Screening_Lock_Patient.php`)
  - **Database Table**: `RIS_Screening_Lock_Patient` | **Primary Key**: `RIS_Screening_Lock_Patient_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No `, `Locked_Start_Date_Time`, `Locked_End_Date_Time`, `Locked_By_User_ID`, `Locked_By_Date_Time`, `Order_Sequence`, `Active_Status`...
- **Model**: `Physio_Order_Details` (`app/Models/Physio_Order_Details.php`)
  - **Database Table**: `Physio_Order_Details` | **Primary Key**: `Physio_Order_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Basic_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `No_Of_Remaining_Sessions`, `Total_No_Of_Session`, `Branch_Code`, `Physio_Order_Deleted`, `Ordered_Notes`, `Remarks`...
- **Model**: `PriorStatus` (`app/Models/PriorStatus.php`)
  - **Database Table**: `Prior_Status` | **Primary Key**: `id`
- **Model**: `User` (`app/Models/User.php`)
  - **Database Table**: `Users` | **Primary Key**: `User_Id`
  - **Constants / Status Flags**: `ADMIN_USER_USER_ID = "Admin"`
  - **Eloquent Relationships**: `hasMany(UserBasedGlobalFilter)` [Key/Pivot: `User_Id`], `hasMany(BranchBasedCacheSettings)` [Key/Pivot: `Created_By_User_Id`], `hasMany(BranchBasedCacheSettings)` [Key/Pivot: `Modified_By_User_Id`], `hasMany(UserDocumentationTab)` [Key/Pivot: `User_Id`]
- *(+447 additional Eloquent models associated with APPLICATION)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `MessageTaskInboxController` (`app/Http/Controllers/MessageTaskInboxController.php`)
  - **Action Methods**: `getViewInboxMail()`, `fetchInboxContent()`, `deleteSelectedMessage()`, `newdeleteSelectedMessage()`, `newdeletesingleInboxItemMultiMessage()`, `deleteSingleSelectedMessage()`, `newdeleteSingleSelectedMessage()`, `showToReadSelectedMessage()`
- **Controller**: `PolicyInsuranceCompanyAndPlanController` (`app/Http/Controllers/PolicyInsuranceCompanyAndPlanController.php`)
  - **Action Methods**: `viewPolicyInsuranceCompanyAndPlan()`, `getAddPolicyInsuranceCompanyAndPlan()`, `getPolicyDescription()`, `getpaymentType()`, `getInsuranceCompanyName()`, `getpatientIncomenetworkName()`, `getInsurancePlanNames()`, `PostAddPolicyInsCmpyAndPlan()`
- **Controller**: `PatientBillingBackendController` (`app/Http/Controllers/PatientBillingBackendController.php`)
  - **Action Methods**: `modifyInvoiceDate()`, `UPDInvoiceDate()`, `modifyInvoiceReceipt()`, `UPDInvoiceReceipt()`, `UPDInvoiceReceiptAmt()`, `getInvoiceVisitRegisteredDateTime()`
- **Controller**: `AnesthesiaTemplateController` (`app/Http/Controllers/AnesthesiaTemplateController.php`)
  - **Action Methods**: `postAnesthesia()`, `editAnesthesia()`, `updatedtAnesthesia()`, `viewAnesthesiaDetail()`, `changeAnesthesiaTemplateStatus()`, `viewAnesthesia()`, `addAnesthesiaTemplate()`, `getDepartmentBranchAutoComplete()`
- **Controller**: `PatientAssitanceTypesController` (`app/Http/Controllers/PatientAssitanceTypesController.php`)
  - **Action Methods**: `getViewPatientAssitanceTypes()`, `getAddPatientAssitanceTypes()`, `alreadyExists()`, `postAddPatientAssitanceTypes()`, `getPatientAssitanceTypesstatus()`, `getEditPatientAssitanceTypes()`, `postEditPatientAssitanceTypes()`, `getDeletePatientAssitanceTypes()`
- **Controller**: `PurchaseTaxTypeController` (`app/Http/Controllers/PurchaseTaxTypeController.php`)
  - **Action Methods**: `viewPurchaseTaxType()`, `addPurchaseTaxType()`, `postAddPurchaseTaxType()`, `editPurchaseTaxType()`, `postEditPurchaseTaxType()`, `changeStatusPurchaseTaxType()`, `downloadPurchaseTaxType()`, `deletePurchaseTaxType()`
- *(+1158 more controllers handling APPLICATION)*

### 5. Form Requests & Input Validation Rules
- **Form Request**: `StoreEMRCommonMastersTypeRequest` (`app/Http/Requests/StoreEMRCommonMastersTypeRequest.php`)
  - **Validation Rules**:
    - `//         EMR_Common_Type_Description => required|string|max:200`
    - `//         Order_Sequence => required|integer`
    - `//         Branch_Code => required|string|max:20|unique:EMR_Common_Masters_Type,Branch_Code`
    - `//         selectedData.*.EMR_Common_Description => required|string|max:200`
    - `//         selectedData.*.Textbox_Required => required|string|in:Y,N`
    - `//         selectedData.*.Score_Is_Applicable => required|string|in:Y,N`
- **Form Request**: `StoreUserRequest` (`app/Http/Requests/StoreUserRequest.php`)
  - **Validation Rules**:
    - `User_Id => required|unique:users,User_Id|max:40|regex:/^[0-9A-Za-z@.]+$/`
    - `User_First_Name => required|max:30|string|regex:/^[A-Za-z\s]+$/`
    - `User_Middle_Name => sometimes|max:30|string|regex:/^[A-Za-z\s]+$/`
    - `User_Last_Name => required|max:30|string|regex:/^[A-Za-z\s]+$/`
    - `User_Password => max:200|regex:/[a-z]/|regex:/[A-Z]/|regex:/[0-9]/|regex:/[@$!%*#?&]/`
    - `Nationality_Code => required|max:20`
- **Form Request**: `DeleteUserRequest` (`app/Http/Requests/DeleteUserRequest.php`)
  - **Validation Rules**:
    - `User_Id => exists:users,User_Id`
- **Form Request**: `Request` (`app/Http/Requests/Request.php`)
- **Form Request**: `UpdateUserRequest` (`app/Http/Requests/UpdateUserRequest.php`)
  - **Validation Rules**:
    - `User_Id => required|unique:users,User_Id,.$User_id.,User_Id|max:40|regex:/^[0-9A-Za-z@.]+$/`
    - `User_First_Name => required|max:30|string|regex:/^[A-Za-z\s]+$/`
    - `User_Middle_Name => sometimes|max:30|string|regex:/^[A-Za-z\s]+$/`
    - `User_Last_Name => required|max:30|string|regex:/^[A-Za-z\s]+$/`
    - `User_Password => max:200|regex:/[a-z]/|regex:/[A-Z]/|regex:/[0-9]/|regex:/[@$!%*#?&]/`
    - `Nationality_Code => required|max:20`
- **Form Request**: `DoctorAvailabilityRequest` (`app/Http/Requests/Resource/DoctorAvailabilityRequest.php`)
  - **Validation Rules**:
    - `location_id => required|string|exists:Branch,Branch_Code`
    - `api_key => required|string|exists:Branch,WebService_Key`
    - `doctor_id => required|integer|exists:Resource_Parent,Resource_Parent_Serial_No`
    - `start_datetime => required|date_format:Y-m-d H:i|date|after:now`
    - `end_datetime => required|date_format:Y-m-d H:i|after:start_datetime`
    - `speciality_code => required|string|exists:Speciality,Speciality_Code`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/loadICDCodes` | `ICDSearchController` | `loadICDCodes` | `web/api` |
| `GET` | `/nationalityIDTypeMapping/{id?}` | `IdentificationTypeController` | `getnationalityIDTypeMapping` | `web/api` |
| `GET` | `/addIDNationalityMapping` | `IdentificationTypeController` | `addIDNationalityMapping` | `web/api` |
| `POST` | `/addIDentNatMapping` | `IdentificationTypeController` | `addIDentNatMapping` | `web/api` |
| `GET` | `/changeNatIdentTypeStatusToChange/{code}/{status}` | `IdentificationTypeController` | `getNationalIdentificationTypeStatusToChange` | `web/api` |
| `GET` | `/editNatIdentificationType/{code}` | `IdentificationTypeController` | `getNatIdentificationTypeToEdit` | `web/api` |
| `POST` | `/editNatIdentificationType` | `IdentificationTypeController` | `postEditedNatIdentificationType` | `web/api` |
| `GET` | `/deleteNatIdentificationType/{code}` | `IdentificationTypeController` | `getdeleteNatIdentificationType` | `web/api` |
| `GET` | `/downloadNatIdentificationType` | `IdentificationTypeController` | `downloadNatIdentificationTypeDetails` | `web/api` |
| `GET` | `/viewNatIdentificationType/{code}/{page?}` | `IdentificationTypeController` | `viewNatIdentificationType` | `web/api` |
| *...* | *+1449 more routes mapped to APPLICATION* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `CommonService` (`app/Services/CommonService.php`)
  - Methods: `getRemittanceStatus()`, `getEncounterEndStatus()`, `getexistEncTypedata()`, `checkAcknowledgmentStatus()`, `checkRISServiceCompletedStatus()`
- **Service**: `ClaimMandatoryObservationTypeService` (`app/Services/ClaimMandatoryObservationTypeService.php`)
  - Methods: `saveClaimMandatoryObservationType()`, `getClaimMandatoryObservationTypedata()`, `changestatus()`, `ClaimMandatoryObservationTypeDownload()`, `getBranchBasedModule()`
- **Service**: `BranchConfigurationService` (`app/Services/BranchConfigurationService.php`)
- **Service**: `MuscleStrengthService` (`app/Services/MuscleStrengthService.php`)
  - Methods: `addMuscleStrength()`, `getMuscleStrengthdata()`, `changestatus()`, `MuscleStrengthDownload()`, `updateMuscleStrength()`
- **Service**: `LISQueryService` (`app/Services/LISQueryService.php`)
  - Methods: `ResultEntryQuery()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: APPOINTMENT (ID: APS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `APS`
- **Module Name**: `APPOINTMENT`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Appointment Bookings, Appointment Source Master, Appointments, Global View Of Appointments, OR SCHEDULER
- **Discovered Sub-functions & Action Page Links** (15 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `APPMAIN` | Appointment Main | `#` | Appointments | Appointments Management |
| `APONTMT` | APPOINTMENT SCHEDULER | `dashboard` | - | - |
| `APSMGMT` | APPOINTMENT SCHEDULER MANAGEMENT | `appointmentScheduler` | Appointment Bookings | Appointments Management |
| `APPSRCMAST` | Appointment Source Master | `AppointmentSource` | Appointment Source Master | - |
| `APPT` | APPOINTMENT TAB | `appointment` | - | - |
| `ChgSpclty` | Change Speciality | `changeSpecialityView` | - | - |
| `GLOBE` | GLOBAL APPOINTMENT | `viewGlobalAppointment` | Global View Of Appointments | View & Manage Appointments |
| `OTSCH` | OT SCHEDULER | `OTScheduler` | OR SCHEDULER | OR SCHEDULER |
| `PATDET` | PATIENT BASIC DETAILS | `patientBasicDetails` | - | - |
| `PATNOTEAPP` | PATIENTNOTE TAB | `patnotes` | - | - |
| `QUESTIONAP` | QUESTIONAIRE TAB | `questiontab` | - | - |
| `APPDOCVIEW` | View Doctor Appointment | `#` | - | - |
| `APPVIEWEMR` | VIEW EMR | `apptViewEMR` | - | - |
| `POSTPONE` | VIEW POSTPONE | `apptViewPostpone` | - | - |
| `WHTCBT` | Whats App Message | `previous_value` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Appointment_` (7 tables), `appointment_` (1 tables)
- **Associated Tables Count**: 108 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Appointment_Default_Speciality`, `Appointment_Merge_Counter`, `Appointment_Status_Type`, `Appointment_Visit_Questionnaire`, `Appointment_Visit_Questionnaire_Possible_Answers`, `Appointment_Visit_Questionnaire_Types`, `Appointment_Visit_Questionnaire_Types_Services`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Appointment` (`app/Models/Appointment.php`)
  - **Database Table**: `Default` | **Primary Key**: `id`
  - **Eloquent Relationships**: `belongsTo(PatientInfo)` [Key/Pivot: `Patient_Basic_Details_Serial_No`], `belongsTo(Resource)` [Key/Pivot: `Resource_Serial_No`]
- **Model**: `PatientAppointmentWhatsappNotification` (`app/Models/PatientAppointmentWhatsappNotification.php`)
  - **Database Table**: `Patient_Appointment_Whatsapp_Notification` | **Primary Key**: `id`
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- **Model**: `PatientVisitLISServicesParameterStatusValues` (`app/Models/PatientVisitLISServicesParameterStatusValues.php`)
  - **Database Table**: `Patient_Visit_LIS_Services_Parameter_Status_Values` | **Primary Key**: `Patient_Visit_LIS_Services_Parameter_Status_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_LIS_Services_Parameter_Serial_No`, `Visit_Service_Level_Status_Type_Code`, `Updated_By_User_Id`, `Updated_Date_Time`, `Reason_Code`, `Remarks`, `Created_By_User_Id`, `Created_Date_Time`...
- **Model**: `PatientBasicDetails` (`app/Models/PatientBasicDetails.php`)
  - **Database Table**: `Patient_Basic_Details` | **Primary Key**: `Patient_Basic_Details_Serial_No`
  - **Eloquent Relationships**: `hasOne(PatientBasicEncriptDetail)` [Key/Pivot: `Patient_Basic_Details_Serial_No`]
- *(+12 additional Eloquent models associated with APPOINTMENT)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `PatientMultiAppointmentController` (`app/Http/Controllers/PatientMultiAppointmentController.php`)
  - **Action Methods**: `loadMultiAppointmentGrid()`
- **Controller**: `RegistrationAppointmentController` (`app/Http/Controllers/RegistrationAppointmentController.php`)
  - **Action Methods**: `patientVisitRequiredAppt()`, `patientVisitNotRequiredAppt()`, `checkWaitListExceedCount()`, `patientAppointmentNotRequiredWalkinAppointment()`, `loadEncounterTypeDetail()`, `loadPartnerGroup()`, `getRISInstallationparameterBasedOnLabNo()`, `branchBasedFollowUp()`
- **Controller**: `GlobalViewAppointmentController` (`app/Http/Controllers/GlobalViewAppointmentController.php`)
  - **Action Methods**: `Appointment()`, `generateprint()`, `generatePDF()`, `getViewGlobal()`, `statuscountchange()`, `getspeciality()`, `getresource()`, `getname()`
- **Controller**: `AppointmentQstnTypeController` (`app/Http/Controllers/AppointmentQstnTypeController.php`)
  - **Action Methods**: `getAddAppointmentQstnType()`, `postAddAppointmentQstnType()`, `alreadyExists()`, `getViewApptQstnType()`, `getEditStatusApptQstnType()`, `getDeleteApptQstnType()`, `getEditApptQstnType()`, `postEditApptQstnType()`
- **Controller**: `AppointmentDefaultSpecialityController` (`app/Http/Controllers/AppointmentDefaultSpecialityController.php`)
  - **Action Methods**: `addAppointmentDefaultSpeciality()`, `postaddAppointmentDefaultSpeciality()`, `viewAppointmentDefaultSpeciality()`, `geteditStatusAppointmentDefaultSpeciality()`, `getdeleteAppointmentDefaultSpeciality()`, `editAppointmentDefaultSpeciality()`, `posteditAppointmentDefaultSpeciality()`, `downloadAppointmentDefaultSpeciality()`
- *(+26 more controllers handling APPOINTMENT)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/checkMobileAndUsername` | `OnlineAppointmentSchedulerController` | `checkMobileAndUsername` | `web/api` |
| `GET` | `/checkMobileAndUsernameEdit` | `OnlineAppointmentSchedulerController` | `checkMobileAndUsernameEdit` | `web/api` |
| `GET` | `/getAptSpeciality` | `OnlineAppointmentSchedulerController` | `getAptSpeciality` | `web/api` |
| `GET` | `/getAptSpecialityResource` | `OnlineAppointmentSchedulerController` | `getAptSpecialityResource` | `web/api` |
| `GET` | `/apsOnlineFetchResources` | `OnlineAppointmentSchedulerController` | `fetchResourceLists` | `web/api` |
| `GET` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `getEditOnlinePatient` | `web/api` |
| `POST` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `postEditOnlinePatient` | `web/api` |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/universalCodeGroupsValues/{id?}` | `UniversalCodeGroupsValuesController` | `getIndex` | `web/api` |
| `GET` | `/loadUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `loadUniversalCodeGroupValues` | `web/api` |
| *...* | *+562 more routes mapped to APPOINTMENT* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `AppointmentSMS` (`app/Services/AppointmentSMS.php`)
  - Methods: `getAppointmentDetails()`
- **Service**: `AppointmentService` (`app/Services/AppointmentService.php`)
  - Methods: `getPatientAppointmentDetails()`
- **Service**: `RecurringAppointmentService` (`app/Services/AppointmentService/RecurringAppointmentService.php`)
- **Service**: `ResourceService` (`app/Services/AppointmentService/ResourceService.php`)
  - Methods: `getExistingPatientDuplicateSameDaySameResSameSer()`
- **Service**: `PatientPortalAppointmentSMS` (`app/Services/AppointmentSMS/PatientPortalAppointmentSMS.php`)
  - Methods: `PatientPortalAPPointmentsendSMSonCheck()`, `getAPIResponse()`, `getDBValue()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: Audit Log (ID: AUL)

### 1. Module Overview & Navigation Structure
- **Module ID**: `AUL`
- **Module Name**: `Audit Log`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Audit Log, Audit-Log
- **Discovered Sub-functions & Action Page Links** (2 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `AUL` | Audit Log | `viewSampleAuditLog` | Audit-Log | - |
| `AUDL` | Audit_Log | `viewSampleAuditLog` | Audit Log | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Associated Tables Count**: 31 tables identified
- **Key Tables**: `API_Request_Response_Log_Details`, `Application_Request_Log`, `Billing_Deleted_Log_Details`, `Copay_Favorite_Maternity_Group_Log`, `Okadoc_Reschedule_Cancel_Log`, `PA_Patient_Visit_ICD_Submission_Log`, `PA_Patient_Visit_ICD_Submission_Log_Details`, `PA_Patient_Visit_Insurance_Service_Cancellation_Log`, `Patient_Eligibility_Check_Log_Details`, `Patient_Visit_Discharge_Summary_Approval_Log_Details`, `Patient_Visit_Discharge_Summary_Details_Log`, `Patient_Visit_Discount_Log_Details`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `API_Request_Response_Log_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `API_Request_Response_Log_Details_Serial_No` | `bigint` | - | NO | - |
| `Url` | `varchar` | 250 | NO | - |
| `Method` | `varchar` | 6 | NO | - |
| `Page_type` | `varchar` | 100 | NO | - |
| `Request_headers` | `varchar` | -1 | NO | - |
| `Request_body` | `varchar` | -1 | NO | - |
| `Response_headers` | `varchar` | -1 | NO | - |
| `Response_body` | `varchar` | -1 | NO | - |
| `Status_code` | `nvarchar` | 100 | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| *...* | *+2 more columns* | | | |

*Table: `Application_Request_Log`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Application_Request_Log_Serial_No` | `bigint` | - | NO | - |
| `Session_ID` | `nvarchar` | 200 | YES | - |
| `Branch_Code` | `nvarchar` | 20 | YES | - |
| `Request_IP` | `nvarchar` | 100 | YES | - |
| `Application_URL` | `nvarchar` | -1 | YES | - |
| `Request_Method` | `nvarchar` | 10 | YES | - |
| `Is_AJAX` | `nvarchar` | 1 | YES | - |
| `Controller_Name` | `nvarchar` | 200 | YES | - |
| `Functions_Name` | `nvarchar` | 200 | YES | - |
| `JSON_Format_Details` | `nvarchar` | -1 | YES | - |
| `Request_Execution_Time` | `nvarchar` | 50 | YES | - |
| `Created_By_User_Id` | `nvarchar` | 40 | YES | - |
| *...* | *+8 more columns* | | | |

*Table: `Billing_Deleted_Log_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Billing_Deleted_Log_Details_Serial_No` | `bigint` | - | NO | - |
| `Bill_Header_Serial_No` | `bigint` | - | NO | - |
| `Bill_Header_Json_Data` | `varchar` | -1 | YES | - |
| `Bill_Detail_Json_Data` | `varchar` | -1 | YES | - |
| `Bill_Amount_Received_Data` | `varchar` | -1 | YES | - |
| `Bill_Deposit_Json_data` | `varchar` | -1 | YES | - |
| `Page_Type` | `varchar` | 10 | YES | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `varchar` | 1 | NO | - |

*Table: `Copay_Favorite_Maternity_Group_Log`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Copay_Favorite_Maternity_Group_Log_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Basic_Details_Serial_No` | `bigint` | - | YES | - |
| `Copay_Favorite_Maternity_Group_Details_Serial_No` | `bigint` | - | YES | - |
| `Copay_Favorite_Default_Groups` | `varchar` | 200 | YES | - |
| `Copay_Favorite_Patient_Share` | `decimal` | - | YES | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

### 3. Eloquent Models & Data Architecture
- **Model**: `PatientVisitDrugScheduleIVAdministrationLog` (`app/Models/PatientVisitDrugScheduleIVAdministrationLog.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_IV_Administration_Log` | **Primary Key**: `Patient_Visit_Drug_Schedule_IV_Administration_Log_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`, `IV_Start_Resume_Time`, `IV_End_Pause_Time`, `Rate`, `Type`, `Started_By_User_Id`, `Paused_By_User_Id`, `Resume_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(PatientVisitDrugScheduleIVAdminstration)` [Key/Pivot: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`]
- **Model**: `WebServiceLogDetail` (`app/Models/WebServiceLogDetail.php`)
  - **Database Table**: `Web_Service_Log_Details` | **Primary Key**: `Web_Service_Log_Details_Serial_No`
  - **Fillable Attributes**: `Branch_Code`, `Web_Service_Type`, `Web_Service_Method`, `Web_Service_Content`, `Web_Service_Error`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
  - **Eloquent Relationships**: `hasMany(Branch)` [Key/Pivot: `Branch_Code`]
- **Model**: `LogActivityModel` (`app/Models/LogActivityModel.php`)
  - **Database Table**: `Application_Request_Log` | **Primary Key**: `Application_Request_Log_Serial_No`
  - **Fillable Attributes**: `Session_ID`, `Branch_Code`, `Request_IP`, `Application_URL`, `Request_Method`, `Is_AJAX`, `Controller_Name`, `Functions_Name`...
- **Model**: `PatientEligibilityLogDetails` (`app/Models/PatientEligibilityLogDetails.php`)
  - **Database Table**: `Patient_Eligibility_Check_Log_Details` | **Primary Key**: `Patient_Eligibility_Check_Log_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Eligibility_Check_Serial_No`, `Eligibility_Request`, `Eligibility_Response`, `Eligibility_Status`, `Eligibility_Type`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(PatientEligibilityCheck)` [Key/Pivot: `Patient_Eligibility_Check_Serial_No`]
- **Model**: `UserLogModel` (`app/Models/UserLogModel.php`)
  - **Database Table**: `User_Log_Details_By_Branch` | **Primary Key**: `User_Log_Details_By_Branch_Serial_No`
  - **Fillable Attributes**: `Total_No_Of_Instance`...
- **Model**: `PAPatientVisitICDSubmissionLogDetails` (`app/Models/PAPatientVisitICDSubmissionLogDetails.php`)
  - **Database Table**: `PA_Patient_Visit_ICD_Submission_Log_Details` | **Primary Key**: `PA_Patient_Visit_ICD_Submission_Log_Details_Serial_No`
  - **Fillable Attributes**: `PA_Patient_Visit_ICD_Submission_Log_Serial_No`, `PA_Patient_Visit_ICD_Codes_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
  - **Eloquent Relationships**: `belongsTo(PAPatientVisitICDSubmissionLog)` [Key/Pivot: `PA_Patient_Visit_ICD_Submission_Log_Serial_No`], `belongsTo(PAPatientVisitICDCodes)` [Key/Pivot: `PA_Patient_Visit_ICD_Codes_Serial_No`]
- *(+22 additional Eloquent models associated with Audit Log)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `SampleAuditLogController` (`app/Http/Controllers/SampleAuditLogController.php`)
  - **Action Methods**: `viewSampleAuditLog()`, `getPatientVisitDetailsByPatientSampleAuditLog()`, `expandPatientHandOverDetail()`, `getAuditLogDetails()`, `getPerioDentalAuditLogDetails()`, `getPerioDentalToothMeta()`, `printAuditPatientLog()`, `sanitizeValue()`
- **Controller**: `ClaimEMAuditController` (`app/Http/Controllers/INS/ClaimEMAuditController.php`)
  - **Action Methods**: `loadEMAuditViewGrid()`, `getEMClaimDetailsLoad()`, `getDeleteClaimService()`, `getDeleteClaimICD()`, `getUpdateClaimServiceICD()`, `getWaitListTabEM()`
- **Controller**: `ClaimInvoiceAuditLogController` (`app/Http/Controllers/INS/ClaimInvoiceAuditLogController.php`)
  - **Action Methods**: `saveAuditLogDetails()`, `insertClaimAuditLog()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/ambient/save-ai-log` | `AmbientController` | `saveAmbientAILog` | `web/api` |
| `GET` | `/viewSampleAuditLog/{id?}` | `SampleAuditLogController` | `viewSampleAuditLog` | `web/api` |
| `GET` | `/getPatientVisitDetailsByPatientSampleAuditLog` | `SampleAuditLogController` | `getPatientVisitDetailsByPatientSampleAuditLog` | `web/api` |
| `GET` | `/getAuditLogDetails` | `SampleAuditLogController` | `getAuditLogDetails` | `web/api` |
| `GET` | `/getPerioDentalAuditLogDetails` | `SampleAuditLogController` | `getPerioDentalAuditLogDetails` | `web/api` |
| `GET` | `/getPerioDentalToothMeta` | `SampleAuditLogController` | `getPerioDentalToothMeta` | `web/api` |
| `GET` | `/expandPatientHandOverDetail` | `SampleAuditLogController` | `expandPatientHandOverDetail` | `web/api` |
| `GET` | `/printAuditPatientLog/{pSno}` | `SampleAuditLogController` | `printAuditPatientLog` | `web/api` |
| `POST` | `/userLogDetailsinView` | `SampleAuditLogController` | `userLogDetailsinView` | `web/api` |
| `POST` | `/checkIfUserDataExistsForDownload` | `SampleAuditLogController` | `checkIfUserDataExists` | `web/api` |
| *...* | *+19 more routes mapped to Audit Log* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `InsertAuditLogService` (`app/Services/InsertAuditLogService.php`)
  - Methods: `insertAuditLog()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: BED MANAGEMENT (ID: IPD)

### 1. Module Overview & Navigation Structure
- **Module ID**: `IPD`
- **Module Name**: `BED MANAGEMENT`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Bed Management
- **Discovered Sub-functions & Action Page Links** (3 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `IPDBedMan` | IPD Bed Manager | `patientDetailsIPD` | - | - |
| `IPDView` | IPD Bed View | `viewIPD` | Bed Management | Manage Admissions & Bed Status |
| `RETODISNOT` | Ready To Discharge Notification | `#` | - | Ready To Discharge Notification |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `IPD_` (7 tables)
- **Associated Tables Count**: 4 tables identified
- **Key Tables**: `Patient_Visit_Admission_Data`, `Patient_Visit_Admission_Data_Values`, `Patient_Visit_Admission_Form_Details`, `Patient_Visit_Resources_Bed_Log_Details`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `Patient_Visit_Admission_Form_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Patient_Visit_Admission_Form_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Accompanied_Name` | `varchar` | 200 | NO | - |
| `Family_Relationship_Code` | `nvarchar` | 40 | YES | - |
| `Contact_No` | `varchar` | 20 | YES | - |
| `Arrival_Mode_Registration_Common_Masters_Serial_No` | `bigint` | - | YES | - |
| `Admission_Type_Registration_Common_Masters_Serial_No` | `bigint` | - | YES | - |
| `Admission_Reason` | `varchar` | -1 | YES | - |
| `Estimated_Stay_In_Days` | `smallint` | - | YES | - |
| `Admission_Mode_Registration_Common_Masters_Serial_No` | `bigint` | - | YES | - |
| `Re_Admission` | `varchar` | 1 | NO | ('N') |
| *...* | *+8 more columns* | | | |

*Table: `Patient_Visit_Resources_Bed_Log_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Patient_Visit_Resources_Bed_Log_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Resources_Serial_No` | `bigint` | - | NO | - |
| `Bed_Start_Time` | `datetime` | - | NO | - |
| `Bed_End_Time` | `datetime` | - | NO | - |
| `Reason_Code` | `nvarchar` | 30 | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | - |
| `Resource_Status_Update_Log_Details` | `varchar` | -1 | YES | - |

### 3. Eloquent Models & Data Architecture
- **Model**: `PatientVisitResourcesBedLog` (`app/Models/Patient/PatientVisitResourcesBedLog.php`)
  - **Database Table**: `Patient_Visit_Resources_Bed_Log_Details` | **Primary Key**: `Patient_Visit_Resources_Bed_Log_Details_Serial_No`
- **Model**: `PatientVisitAdmissionFormDetails` (`app/Models/Registration/PatientVisitAdmissionFormDetails.php`)
  - **Database Table**: `Patient_Visit_Admission_Form_Details` | **Primary Key**: `Patient_Visit_Admission_Form_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Admission_Form_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Accompanied_Name`, `Family_Relationship_Code`, `Contact_No`, `Arrival_Mode_Registration_Common_Masters_Serial_No`, `Admission_Type_Registration_Common_Masters_Serial_No`...

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `ERAdmissionModuleController` (`app/Http/Controllers/ERAdmissionModuleController.php`)
  - **Action Methods**: `viewERWaitingList()`, `ERWaitListFilterRecords()`, `EmergencyPatStatusUpdate()`, `loadTriagedByUserErPat()`, `loadExaminedByUserErPat()`, `getERCTALevel()`, `getEmergencyTriageDT()`, `getUserGroupListforNotify()`
- **Controller**: `ERIPAdmissionModuleController` (`app/Http/Controllers/ERIPAdmissionModuleController.php`)
  - **Action Methods**: `viewERIPAdmission()`, `getReasonForERIPAdmission()`, `getRefBranchForERIPAdmission()`, `getRefUserForERIPAdmission()`, `postERIPAdmission()`, `viewIPAdmissionWaitingList()`, `IPWaitListFilterRecords()`, `IPWaitListFilterRecords_bk()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/viewIPDPackageCategory/{id?}` | `IPDPackageCategoryController` | `getViewIPDPackageCategory` | `web/api` |
| `GET` | `/getReasonForERIPAdmission` | `ERIPAdmissionModuleController` | `getReasonForERIPAdmission` | `web/api` |
| `GET` | `/getRefBranchForERIPAdmission` | `ERIPAdmissionModuleController` | `getRefBranchForERIPAdmission` | `web/api` |
| `GET` | `/getRefUserForERIPAdmission` | `ERIPAdmissionModuleController` | `getRefUserForERIPAdmission` | `web/api` |
| `GET` | `/postERIPAdmission` | `ERIPAdmissionModuleController` | `postERIPAdmission` | `web/api` |
| `GET` | `/viewIPAdmissionWaitingList/{id?}` | `ERIPAdmissionModuleController` | `viewIPAdmissionWaitingList` | `web/api` |
| `POST` | `/IPWaitListFilterRecords` | `ERIPAdmissionModuleController` | `IPWaitListFilterRecords` | `web/api` |
| `GET` | `/registerERIPPatient/{pat_id?}/{vst_id?}/{ref_By_Vst?}/{type?}/{stat?}` | `ERIPAdmissionModuleController` | `registerERIPPatient` | `web/api` |
| `GET` | `/IPReadytodischargeupdat` | `ERIPAdmissionModuleController` | `IPReadytodischargeupdat` | `web/api` |
| `GET` | `/IPdischargeStat` | `ERIPAdmissionModuleController` | `IPdischargeStat` | `web/api` |
| *...* | *+40 more routes mapped to BED MANAGEMENT* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: BI REPORTS (ID: BAR)

### 1. Module Overview & Navigation Structure
- **Module ID**: `BAR`
- **Module Name**: `BI REPORTS`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (167 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ABNRMLRPT` | Abnormal Results Report | `byABNRMLRPT` | - | - |
| `AGINGRPT` | Aging Report | `byAGINGRPT` | - | - |
| `BILLCNTRPT` | Bill Count Report | `byBILLCNTRPT` | - | - |
| `BILLREG` | Bill Register Report - New | `byBILLREG` | - | - |
| `BILRGSRRPT` | BILL REGISTER WISE REPORT | `byBillRegisterReport` | - | - |
| `BILLINGRPT` | Billing Wise Collection Report | `byBillWiseCollRpt` | - | - |
| `DOCINRPT` | bydoctorincome | `bydoctorincome` | - | - |
| `CWTRPT` | Category Wise Test Count | `bycategorywise` | - | - |
| `CLIMISRPT` | CLINICS MONTHLY INCOME REPORT | `byClinicsMIRpt` | - | - |
| `CMPPENDINV` | Company Pending Invoice | `byCmpPendInv` | - | - |
| `BILLCMPSUM` | COMPANY SUMMARY REPORT | `byCompanySummary` | - | - |
| `COMWSEICME` | Company wise income | `byCmyWiseIcome` | - | - |
| `CONSULTAT` | CONSULTATION TAT | `byCONSULTAT` | - | - |
| `COPAYRPT` | Copay Report | `byCopayReport` | - | - |
| `COSQTYRPT` | Cost of Sales Report - QuantityWise | `byCOSQTYRPT` | - | N |
| *...* | *+152 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Bar_` (1 tables)
- **Associated Tables Count**: 82 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`, `Children_MH_Attribute_Values`, `DSR_All_Attribute_Values`, `Demographic_Attribute_Age_Values`, `Demographic_Attribute_DOB_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `HimesReportsScheduleDetailsLogs` (`app/Models/HimesReportsScheduleDetailsLogs.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details_Logs` | **Primary Key**: `Himes_Reports_Schedule_Details_Logs_Serial_No`
- **Model**: `HimesReportsScheduleDetails` (`app/Models/HimesReportsScheduleDetails.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details` | **Primary Key**: `Himes_Reports_Schedule_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(ReportFunctionURL)` [Key/Pivot: `Report_Function_URL_Serial_No`]
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- **Model**: `PatientVisitLISServicesParameterStatusValues` (`app/Models/PatientVisitLISServicesParameterStatusValues.php`)
  - **Database Table**: `Patient_Visit_LIS_Services_Parameter_Status_Values` | **Primary Key**: `Patient_Visit_LIS_Services_Parameter_Status_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_LIS_Services_Parameter_Serial_No`, `Visit_Service_Level_Status_Type_Code`, `Updated_By_User_Id`, `Updated_Date_Time`, `Reason_Code`, `Remarks`, `Created_By_User_Id`, `Created_Date_Time`...
- **Model**: `Himes_Job_Reports` (`app/Models/Himes_Job_Reports.php`)
  - **Database Table**: `Himes_Job_Reports` | **Primary Key**: `Himes_Job_Reports_Serial_No`
- *(+9 additional Eloquent models associated with BI REPORTS)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `specialityDepartmentVisitServiceStatusValuesController` (`app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`)
  - **Action Methods**: `getspecialityDepartmentVisitServiceStatusValues()`, `alreadyExists()`, `getDownloadspecialityDepartmentVisitServiceStatusValues()`
- **Controller**: `GlobalViewOfUniversalCodeGroupsValuesController` (`app/Http/Controllers/GlobalViewOfUniversalCodeGroupsValuesController.php`)
  - **Action Methods**: `ViewGlobalViewOfUniversalCodeGroupsValues()`, `LoadOptionForUniversalCodeGroupsValuesField()`
- **Controller**: `ReportScheduleController` (`app/Http/Controllers/ReportScheduleController.php`)
  - **Action Methods**: `getListReportSchedule()`, `getViewReportSchedule()`, `getReportList()`, `getAddReportSchedule()`, `downloadReportSchedule()`, `postAddReportSchedule()`, `getEditReportSchedule()`, `postEditReportSchedule()`
  - **Form Validation Rules**: reportFunctionName => required; fileName => string|max:255; frequency => required|integer|between:1; durationWeek => nullable|integer|between:1
  - **Dispatched Workflows**: Job: `ProcessSchedulerJob`
- **Controller**: `UniversalCodeGroupsValuesController` (`app/Http/Controllers/UniversalCodeGroupsValuesController.php`)
  - **Action Methods**: `getIndex()`, `loadUniversalCodeGroupValues()`, `getAddUniversalCodeGroupValues()`, `CheckSpecialityDepartmentData()`, `EditCheckSpecialityDepartmentData()`, `postAddUniversalCodeGroupValues()`, `getChangeUniversalCodeGroupValuestatus()`, `getDeletUniversalCodeGroupValue()`
- **Controller**: `UniversalCodeValuesController` (`app/Http/Controllers/UniversalCodeValuesController.php`)
  - **Action Methods**: `addUniversalcodeType()`, `postUniversalcodeTypeValues()`, `getUniversalcodeValues()`, `getchangeUniversalcodetypevaluestatus()`, `getDeleteUniversalcodevalues()`, `getEditUniversalCodeValue()`, `downloadUniversalCodeValuesDetails()`, `postEditUniversalcodeValue()`
- *(+2 more controllers handling BI REPORTS)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/viewReportSchedule/{id?}` | `ReportScheduleController` | `getListReportSchedule` | `web/api` |
| `GET` | `/editReportSchedule/{id?}` | `ReportScheduleController` | `getEditReportSchedule` | `web/api` |
| `GET` | `/runScheduleJob/{id?}` | `ReportScheduleController` | `runScheduleJob` | `web/api` |
| `GET` | `/editStatusReportSchedule/{id?}` | `ReportScheduleController` | `getEditStatusReportSchedule` | `web/api` |
| `GET` | `/deleteReportSchedule/{id?}` | `ReportScheduleController` | `getDeleteReportSchedule` | `web/api` |
| `GET` | `/reportSchedule/{id?}` | `ReportScheduleController` | `getViewReportSchedule` | `web/api` |
| `POST` | `/reportSchedule` | `ReportScheduleController` | `getViewReportSchedule` | `web/api` |
| `GET` | `/addReportSchedule` | `ReportScheduleController` | `getAddReportSchedule` | `web/api` |
| `GET` | `/downloadReportSchedule` | `ReportScheduleController` | `downloadReportSchedule` | `web/api` |
| `POST` | `/addReportSchedule` | `ReportScheduleController` | `postAddReportSchedule` | `web/api` |
| *...* | *+767 more routes mapped to BI REPORTS* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `HimesReportService` (`app/Services/HimesReportService.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: BILLING (ID: BIL)

### 1. Module Overview & Navigation Structure
- **Module ID**: `BIL`
- **Module Name**: `BILLING`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: BRANCH BASED CREDIT NOTE, Bill Counter, Bill Counter User, Billing, Billing Master, CREDIT NOTE, CREDIT NOTE GLOBAL VIEW, DN & CN, Deposit, Discount Codes Master
- **Discovered Sub-functions & Action Page Links** (29 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `BILLCOUNTE` | BILL COUNTER | `billcounter` | Bill Counter | - |
| `BILLCOUNTU` | BILL COUNTER USER | `billcounteruser` | Bill Counter User | - |
| `BILLHD` | BILL HEADER | `patientBilling` | Invoice List | List Of Generated Invoices |
| `BILINDQTY` | BILL INDIVIDUAL QUANTITY | `#` | - | - |
| `BILLMSTR` | BILLING MASTER | `#` | Billing Master | Billing Configurations |
| `BRCRDTNOTE` | Branch Based Credit Note | `previous_value` | BRANCH BASED CREDIT NOTE | - |
| `CASHINV` | Cash Invoice | `#` | - | - |
| `CREDNOTE` | Credit Note | `previous_value` | CREDIT NOTE | - |
| `CREDGV` | Credit Note Global View | `viewGlobalCreditNote` | CREDIT NOTE GLOBAL VIEW | - |
| `DEPHISTORY` | Deposit History | `#` | - | - |
| `DISCODE` | Discount Codes | `viewDiscountCodes` | Discount Codes Master | - |
| `DPACKVIEW` | Dynamic Package Management | `DynamicPackageManagement` | - | - |
| `GLBLBLING` | GLOBAL BILLING | `viewGlobalBilling` | Global View Of Billing | View & Manage Patient Billing |
| `GLBREFUND` | GLOBAL REFUND BILLING | `viewGlobalRefundBilling` | Global View Of Refund Billing | View & Manage Refunds |
| `GLBBILDISC` | GLOBAL VIEW OF DISCOUNT | `viewGlobalDiscount` | Global View of Discount | View & Manage Discount Reqeusts |
| *...* | *+14 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Bill_` (3 tables), `Billing_` (2 tables), `Invoice_` (1 tables), `Occupation_` (1 tables), `Receipts_` (1 tables)
- **Associated Tables Count**: 132 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bill_Auto_Eclaim_Post_Close`, `Bill_Counter`, `Bill_Counter_User`, `Billing_Deleted_Log_Details`, `Billing_Shipment_Details`, `Branch_Based_Purchase_Invoice`, `Branch_Wise_Invoice_Generation`, `Branch_Wise_Proforma_Invoice_Generation`, `Bulk_Previous_Day_Visit_SMS`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `PatientVisitInventoryBilling` (`app/Models/PatientVisitInventoryBilling.php`)
  - **Database Table**: `Patient_Visit_Inventory_Billing` | **Primary Key**: `Patient_Visit_Inventory_Billing_Serial_No`
  - **Fillable Attributes**: `Inventory_Billing_Type`, `Patient_Basic_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No`, `Package_Service_Serial_No`, `Patient_Visit_Drugs_Prescribed_Serial_No`, `Running_Serial_No`, `Item_Drug_Link_Serial_No`...
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- **Model**: `PatientVisitLISServicesParameterStatusValues` (`app/Models/PatientVisitLISServicesParameterStatusValues.php`)
  - **Database Table**: `Patient_Visit_LIS_Services_Parameter_Status_Values` | **Primary Key**: `Patient_Visit_LIS_Services_Parameter_Status_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_LIS_Services_Parameter_Serial_No`, `Visit_Service_Level_Status_Type_Code`, `Updated_By_User_Id`, `Updated_Date_Time`, `Reason_Code`, `Remarks`, `Created_By_User_Id`, `Created_Date_Time`...
- **Model**: `PatientVisitServicesUniversalGroupsCodeValues` (`app/Models/UniversalGroup/PatientVisitServicesUniversalGroupsCodeValues.php`)
  - **Database Table**: `Patient_Visit_Services_Universal_Groups_Code_Values` | **Primary Key**: `Patient_Visit_Services_Universal_Groups_Code_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Services_Serial_No`, `Universal_Code_Groups_Values_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- **Model**: `EMRCCHPIPreviousTreatmentUsersLink` (`app/Models/CCHPITypes/EMRCCHPIPreviousTreatmentUsersLink.php`)
  - **Database Table**: `EMR_CC_HPI_Previous_Treatment_Users_Link` | **Primary Key**: `EMR_CC_HPI_Previous_Treatment_Users_Link_Serial_No`
  - **Fillable Attributes**: `User_Id`, `EMR_CC_HPI_Previous_Treatment_Serial_No`, `Usage_Frequency`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- *(+10 additional Eloquent models associated with BILLING)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PatientBillingBackendController` (`app/Http/Controllers/PatientBillingBackendController.php`)
  - **Action Methods**: `modifyInvoiceDate()`, `UPDInvoiceDate()`, `modifyInvoiceReceipt()`, `UPDInvoiceReceipt()`, `UPDInvoiceReceiptAmt()`, `getInvoiceVisitRegisteredDateTime()`
- **Controller**: `BranchBasedPurchaseInvoiceController` (`app/Http/Controllers/BranchBasedPurchaseInvoiceController.php`)
  - **Action Methods**: `viewBrnchBsePrchaseInv()`, `getdownloadPurchaseInv()`, `changeStatus()`, `getViewBrnchBsePrchaseInv()`, `getAddBrBsePurchaseInv()`, `GetCompany()`, `GetBranch()`, `postAddBrBsePurchaseInv()`
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `GlobalViewRefundBillingController` (`app/Http/Controllers/GlobalViewRefundBillingController.php`)
  - **Action Methods**: `getViewGlobalAppointment()`, `getViewGlobal()`, `getspeciality()`, `getresource()`, `getPatientInvoice()`, `getbilbaranchdetls()`, `getname()`, `getnamesort()`
- **Controller**: `PackageInvoiceController` (`app/Http/Controllers/PackageInvoiceController.php`)
  - **Action Methods**: `printPackageInvoicePdf()`
- **Controller**: `PatientBillingGetController` (`app/Http/Controllers/PatientBillingGetController.php`)
  - **Action Methods**: `getPatientBilling()`, `getPhyPrescribePatientAllergies()`, `getpatientbillinginvoicehistroy()`, `viewPatientBilling()`, `viewPatientBillingSearch()`, `getbillAddRowMore()`, `getBillCounter()`, `getAjaxAddReceivedPayment()`
- *(+70 more controllers handling BILLING)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/invoice/download` | `InvoiceController` | `download` | `web/api` |
| `GET` | `/printer` | `PrintReceiptController` | `printer` | `web/api` |
| `GET` | `/showprinter` | `PrintReceiptController` | `showprinter` | `web/api` |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/universalCodeGroupsValues/{id?}` | `UniversalCodeGroupsValuesController` | `getIndex` | `web/api` |
| `GET` | `/loadUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `loadUniversalCodeGroupValues` | `web/api` |
| `GET` | `/CheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `CheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/EditCheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `EditCheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `getAddUniversalCodeGroupValues` | `web/api` |
| `POST` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `postAddUniversalCodeGroupValues` | `web/api` |
| *...* | *+887 more routes mapped to BILLING* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `InvoiceService` (`app/Services/InvoiceService.php`)
  - Methods: `getPatientVisitIds()`, `getHospitalAddress()`, `getPatientBillHeaderDetails()`, `getPaymentsReceivedByInvoice()`, `getInvoiceHeaderDetails()`
- **Service**: `PatientBillingServices` (`app/Services/PatientBillingServices.php`)
  - Methods: `validateInventoryItemAgainstPatient()`
- **Service**: `GlobalViewBillingService` (`app/Services/GlobalViewBillingService.php`)
- **Service**: `GenerateInvoiceClosedPostedStatus` (`app/Services/GenerateInvoiceClosedPostedStatus.php`)
  - Methods: `getGenInvoiceClosedPostedStatus()`, `insertPatientvisitExcludedPlan()`, `checkseletedItemExcluded()`, `checkInventoryCoverageApplicable()`, `checkPatientPaymentTypes()`
- **Service**: `ClaimInvoiceService` (`app/Services/ClaimInvoiceService.php`)
  - Methods: `ClaimInvoiceDetails()`, `loadInvoiceGridNew()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: BULK MASTER (ID: BMT)

### 1. Module Overview & Navigation Structure
- **Module ID**: `BMT`
- **Module Name**: `BULK MASTER`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: BULK PLAN LIMIT, Bulk Service List Management, Inventory Price List Copy, Report Function URL, Stock Items Copy
- **Discovered Sub-functions & Action Page Links** (5 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `BULKPLANLT` | BULK PLAN LIMIT | `BulkPlanLimit` | BULK PLAN LIMIT | Description of Bulk Plan Limit |
| `BULKPLANLT` | BULK PLAN LIMIT | `BulkPlanLimit` | Report Function URL | Description of Bulk Plan Limit |
| `BLKSERLSMG` | BULK SERVICE LIST MANAGEMENT | `BulkServiceListManagement` | Bulk Service List Management | - |
| `INVPRICCPY` | INVENTORY PRICE LIST COPY | `ViewInventoryPriceListCopy` | Inventory Price List Copy | - |
| `STCKITMCPY` | STOCK ITEMS COPY | `ViewStockItemsCopy` | Stock Items Copy | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Bulk_` (2 tables), `Master_` (5 tables)
- **Associated Tables Count**: 63 tables identified
- **Key Tables**: `AAA_New_Service_Master`, `AAA_given_item_master_QMC`, `All_Master_Logs`, `Bulk_LIS_Result_Update_SMS`, `Bulk_Previous_Day_Visit_SMS`, `Claim_Mandatory_Observation_Type`, `Customer_Master`, `DDWC_Skill_Master`, `Drug_Mapping_Master`, `EMR_Common_Masters`, `EMR_Common_Masters_Type`, `EMR_Lines_Drains_Category`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `All_Master_Logs`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `All_Master_Logs_Serial_No` | `bigint` | - | NO | - |
| `Branch_Code` | `nvarchar` | 20 | NO | - |
| `Function_ID` | `nvarchar` | 10 | NO | - |
| `Module_ID` | `nvarchar` | 3 | NO | - |
| `Page_URL` | `nvarchar` | 200 | NO | - |
| `Before_Revision` | `nvarchar` | -1 | YES | - |
| `After_Revision` | `nvarchar` | -1 | YES | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

### 3. Eloquent Models & Data Architecture
- **Model**: `ItemMaster` (`app/Models/ItemMaster.php`)
  - **Database Table**: `Item_Master` | **Primary Key**: `Item_Master_Serial_No`
- **Model**: `SupplierMaster` (`app/Models/SupplierMaster.php`)
  - **Database Table**: `Supplier_Master` | **Primary Key**: `Supplier_Master_Serial_No`
- **Model**: `AllMasterLogs` (`app/Models/AllMasterLogs.php`)
  - **Database Table**: `All_Master_Logs` | **Primary Key**: `All_Master_Logs_Serial_No`
  - **Fillable Attributes**: `Branch_Code`, `Function_ID`, `Module_ID`, `Page_URL`, `Before_Revision`, `After_Revision`, `Created_By_User_Id`, `Created_Date_Time`...
- **Model**: `Registration_Common_Masters` (`app/Models/Registration_Common_Masters.php`)
  - **Database Table**: `Registration_Common_Masters` | **Primary Key**: `Registration_Common_Masters_Serial_No`
- **Model**: `Master_Flexibility` (`app/Models/Flexibility/Master_Flexibility.php`)
  - **Database Table**: `Master_Flexibility` | **Primary Key**: `Flexibility_Serial_No`
  - **Fillable Attributes**: `Gender_Code`, `Age_Start_UOM`, `Age_Start_Value`, `Age_End_UOM`, `Age_End_Value`, `Branch_Code`, `Flexibility_Level_Serial_No`...
- **Model**: `PatientVisitDocumentType` (`app/Models/Master/PatientVisitDocumentType.php`)
  - **Database Table**: `Patient_Visit_Document_Types` | **Primary Key**: `Patient_Visit_Document_Types_Serial_No`
  - **Constants / Status Flags**: `ROW_PER_PAGE_FOR_PAGINATION = 15`
- *(+38 additional Eloquent models associated with BULK MASTER)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PlanMasterController` (`app/Http/Controllers/PlanMasterController.php`)
  - **Action Methods**: `getIndex()`, `getPlanMasterData()`, `getPlanMasterFetchGroup()`, `getPlanMasterFetchCompany()`, `getPlanMasterFetchBranch()`, `getPlanMasterInsuranceCompany()`, `getinsuranceType()`, `getplanMasterComtonetwrk()`
- **Controller**: `ICUVentilationMasterController` (`app/Http/Controllers/ICUVentilationMasterController.php`)
  - **Action Methods**: `index()`, `postICUVentilationHeaderAndDetailInformation()`, `postReomveElementICUVentilationElement()`, `postICUVentilation()`, `getHeaderDetailsData()`, `insertOrUpdateMasterDetailDataType()`, `deleteMasterDetailDataTypeDropDownItem()`, `updateHeaderAndDetailsTxt()`
- **Controller**: `EmrAllergiesMasterController` (`app/Http/Controllers/EmrAllergiesMasterController.php`)
  - **Action Methods**: `getveiwEmrAllergies()`, `getaddEmrAllergies()`, `postaddEmrAllergies()`, `EMRallergloadMoreItems()`, `getEditEmrAllergies()`, `PosteditEmrAllergies()`, `getEditStatusEmrAllergy()`, `getDeleteEmrAllergies()`
- **Controller**: `ItemMasterController` (`app/Http/Controllers/ItemMasterController.php`)
  - **Action Methods**: `GetAddItemMaster()`, `PostAddItemMaster()`, `PostAddItemMasterDrugItem()`, `alreadyexitsArea()`, `alreadyExistsPostal()`, `getViewItemMaster()`, `EditStatusItemMaster()`, `DeleteItemMaster()`
- **Controller**: `RegistrationCommonMasterController` (`app/Http/Controllers/RegistrationCommonMasterController.php`)
  - **Action Methods**: `index()`, `create()`, `store()`, `edit()`, `update()`, `show()`, `ChangeStatus()`, `Download()`
- **Controller**: `AllMasterLogsController` (`app/Http/Controllers/AllMasterLogsController.php`)
  - **Action Methods**: `insertAllMasterLogs()`, `mapValue()`, `getTypeParameter()`, `getUserMasterSummery()`, `getUserSpeciality()`, `retainUserRevisionBeforeAftertxt()`
- *(+18 more controllers handling BULK MASTER)*

### 5. Form Requests & Input Validation Rules
- **Form Request**: `StoreEMRCommonMastersTypeRequest` (`app/Http/Requests/StoreEMRCommonMastersTypeRequest.php`)
  - **Validation Rules**:
    - `//         EMR_Common_Type_Description => required|string|max:200`
    - `//         Order_Sequence => required|integer`
    - `//         Branch_Code => required|string|max:20|unique:EMR_Common_Masters_Type,Branch_Code`
    - `//         selectedData.*.EMR_Common_Description => required|string|max:200`
    - `//         selectedData.*.Textbox_Required => required|string|in:Y,N`
    - `//         selectedData.*.Score_Is_Applicable => required|string|in:Y,N`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/hrBranchVehicleStatusChange` | `HRMasterController` | `posthrBranchVehicleStatusChange` | `web/api` |
| `POST` | `/hrDeleteBranchVehicle` | `HRMasterController` | `posthrDeleteBranchVehicle` | `web/api` |
| `GET` | `/hrDownloadBranchVehicle` | `HRMasterController` | `getHrDownloadBranchVehicle` | `web/api` |
| `GET` | `/hrEditBranchVehicle` | `HRMasterController` | `gethrEditBranchVehicle` | `web/api` |
| `GET` | `/hrVehicleEditCompanyBranchLoad` | `HRMasterController` | `gethrVehicleEditCompanyBranchLoad` | `web/api` |
| `POST` | `/hrVehicleDataEdit` | `HRMasterController` | `posthrVehicleDataEdit` | `web/api` |
| `GET` | `/viewVehicleDetailsPageLoad` | `HRMasterController` | `viewVehicleDetailsPageLoad` | `web/api` |
| `GET` | `/viewDesgnQualfctn` | `HRMasterController` | `viewDesgnQualfctn` | `web/api` |
| `GET` | `/viewDesgnQualifDetAdd` | `HRMasterController` | `viewDesgnQualifDetAdd` | `web/api` |
| `GET` | `/hrBranchQualiExperianceAutoComplete` | `HRMasterController` | `gethrBranchQualiExperianceAutoComplete` | `web/api` |
| *...* | *+326 more routes mapped to BULK MASTER* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `AllMasterLogsServices` (`app/Services/AllMasterLogsServices.php`)
  - Methods: `insertForAllMasterLogs()`, `nationality()`, `allMAsterLogDataCollection()`, `masterlogBeforeUpdateForVisitEncounter()`, `masterlogAfterUpdateForVisitEncounter()`
- **Service**: `CommonMasterService` (`app/Services/CommonMasterService.php`)
  - Methods: `getBranchLogoFormat()`
- **Service**: `EMRCommonMasterService` (`app/Services/EMRCommonMasterService.php`)
  - Methods: `getDownload()`, `downloadEMRCM()`, `downloadEMRCTD()`, `changestatus()`, `checkEMRTypeDesc()`
- **Service**: `RegistrationCommonMasterService` (`app/Services/RegistrationCommonMasterService.php`)
  - Methods: `addRegistrationCommonMaster()`, `updateRegistrationCommonMaster()`, `getRegistrationCommonMasterdata()`, `getFamilyRelationshipdata()`, `getReferalClinicData()`
- **Service**: `BulkInsertService` (`app/Services/BulkInsertService.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: CERTIFICATE (ID: CTF)

### 1. Module Overview & Navigation Structure
- **Module ID**: `CTF`
- **Module Name**: `CERTIFICATE`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (0 total):
*(Core background or reporting module - navigation managed dynamically via service or API)*

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Certificate_` (3 tables)
- **Associated Tables Count**: 6 tables identified
- **Key Tables**: `Branch_Wise_Certificate_Generation`, `Certificate`, `Certificate_Approved_User`, `Certificate_Header_Footer`, `Certificate_Header_Footer_Link`, `Patient_visit_Certificate`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `CertificateController` (`app/Http/Controllers/CertificateController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewCertificate()`, `viewCertificateAdd()`, `postAddCertificate()`, `getEditCertificate()`, `postUpdateCertificate()`, `changeCertificateStatus()`, `downloadCertificate()`
- **Controller**: `patientCertificateGlobalViewController` (`app/Http/Controllers/patientCertificateGlobalViewController.php`)
  - **Action Methods**: `getCertificateGlobalView()`, `ViewPatVisitCertificateDetail()`, `approvePatCertificate()`, `getGlobalFilterCertificateDet()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/viewCertificate/{id?}` | `CertificateController` | `viewCertificate` | `web/api` |
| `GET` | `/addCertificate` | `CertificateController` | `viewCertificateAdd` | `web/api` |
| `POST` | `/postAddCertificate` | `CertificateController` | `postAddCertificate` | `web/api` |
| `GET` | `/editCertificate/{id?}` | `CertificateController` | `getEditCertificate` | `web/api` |
| `POST` | `/editCertificate` | `CertificateController` | `postUpdateCertificate` | `web/api` |
| `GET` | `/changeCertificateStatus/{sNo}/{status}` | `CertificateController` | `changeCertificateStatus` | `web/api` |
| `GET` | `/downloadCertificate` | `CertificateController` | `downloadCertificate` | `web/api` |
| `GET` | `/ViewCertificateDetail/{id?}` | `CertificateController` | `ViewCertificateDetail` | `web/api` |
| `GET` | `/viewEmbedFieldCertificate` | `CertificateController` | `getEmbedFieldCertificate` | `web/api` |
| `GET` | `/serviceAutoComplete` | `CertificateController` | `serviceAutoComplete` | `web/api` |
| *...* | *+14 more routes mapped to CERTIFICATE* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: CERTIFICATE TEMPLATE (ID: CER)

### 1. Module Overview & Navigation Structure
- **Module ID**: `CER`
- **Module Name**: `CERTIFICATE TEMPLATE`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (0 total):
*(Core background or reporting module - navigation managed dynamically via service or API)*

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Certificate_` (3 tables)
- **Associated Tables Count**: 65 tables identified
- **Key Tables**: `AAA_Given_Additional_Stock_template_qmc`, `AAA_Given_Stock_Template_QMC`, `AAA_given_Pharmacy_Stock_template`, `Anesthesia_Templates`, `Branch_Based_SMS_Template`, `Branch_Based_SMS_Template_Configuration`, `Branch_Wise_Certificate_Generation`, `Certificate`, `Certificate_Approved_User`, `Certificate_Header_Footer`, `Certificate_Header_Footer_Link`, `Consent_Form_Template`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `BranchBasedSMSTemplateConfiguration` (`app/Models/BranchBasedSMSTemplateConfiguration.php`)
  - **Database Table**: `Branch_Based_SMS_Template_Configuration` | **Primary Key**: `Branch_Based_SMS_Template_Configuration_Serial_No`
  - **Fillable Attributes**: `Branch_Based_SMS_Serial_No`, `Template_Format`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
  - **Eloquent Relationships**: `belongsTo(BranchBasedSMS)` [Key/Pivot: `Branch_Based_SMS_Serial_No`], `belongsTo(User)` [Key/Pivot: `Created_By_User_Id`], `belongsTo(User)` [Key/Pivot: `Modified_By_User_Id`]
- **Model**: `DischargeSummaryTemplate` (`app/Models/DischargeSummaryTemplate.php`)
  - **Database Table**: `Discharge_Summary_Template` | **Primary Key**: `Discharge_Summary_Template_Serial_No`
- **Model**: `PatientBasedOrderTemplate` (`app/Models/PhysioTherapy/PatientBasedOrderTemplate.php`)
  - **Database Table**: `Patient_Based_Order_Template` | **Primary Key**: `Patient_Based_Order_Template_Serial_No`
  - **Fillable Attributes**: `Order_Based_Template_Serial_No`, `Physio_Order_Details_Serial_No`, `Template_Description`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
  - **Eloquent Relationships**: `belongsTo(PhysioOrderDetails)` [Key/Pivot: `Physio_Order_Details_Serial_No`]
- **Model**: `ServiceExternalReferralTemplate` (`app/Models/Master/ServiceExternalReferralTemplate.php`)
  - **Database Table**: `Service_External_Referral_Template` | **Primary Key**: `Service_External_Referral_Template_Serial_No`
- **Model**: `UserEMRTemplate` (`app/Models/EMR/UserEMRTemplate.php`)
  - **Database Table**: `User_EMR_Templates` | **Primary Key**: `User_EMR_Templates_Serial_No`
  - **Fillable Attributes**: `User_Id`, `Template_Name`, `Is_Template_Deleted`, `CC_HPI_Group_Form_Encouter_Assignment_Serial_No`, `CC_HPI_Details`, `Services_Group_Form_Encouter_Assignment_Serial_No`, `Service_Details`, `ICD_Group_Form_Encouter_Assignment_Serial_No`...
- **Model**: `UserEMRTemplateLog` (`app/Models/EMR/UserEMRTemplateLog.php`)
  - **Database Table**: `User_EMR_Templates_Log` | **Primary Key**: `User_EMR_Templates_Log_Serial_No`
  - **Fillable Attributes**: `User_EMR_Templates_Serial_No`, `CC_HPI_Group_Form_Encouter_Assignment_Serial_No`, `CC_HPI_Details`, `Services_Group_Form_Encouter_Assignment_Serial_No`, `Service_Details`, `ICD_Group_Form_Encouter_Assignment_Serial_No`, `ICD_Details`, `Prescriptions_Group_Form_Encouter_Assignment_Serial_No`...

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `AnesthesiaTemplateController` (`app/Http/Controllers/AnesthesiaTemplateController.php`)
  - **Action Methods**: `postAnesthesia()`, `editAnesthesia()`, `updatedtAnesthesia()`, `viewAnesthesiaDetail()`, `changeAnesthesiaTemplateStatus()`, `viewAnesthesia()`, `addAnesthesiaTemplate()`, `getDepartmentBranchAutoComplete()`
- **Controller**: `NewReportTemplateController` (`app/Http/Controllers/NewReportTemplateController.php`)
  - **Action Methods**: `NewaddReportTemplate()`, `Ristemlateeditor()`, `getriseditorval()`, `PatientvisitpayemtdetailsPanel()`, `viewPatientHeader()`, `patientpaymentdetailpanel()`, `newpatientpaymentdetailpanel()`, `MultipletemplateEdit()`
- **Controller**: `DischargeSummaryTemplateController` (`app/Http/Controllers/DischargeSummaryTemplateController.php`)
  - **Action Methods**: `viewDischargeSummaryTemplate()`, `addDischargeSummaryTemplate()`, `postaddDischargeSummaryTemplate()`, `getDischargeBranch()`, `editDischargeSummaryTemplate()`, `postEditDischargeSummaryTemplate()`, `deleteDischargeSummaryTemplate()`, `statusDischargeSummaryTemplate()`
- **Controller**: `CertificateController` (`app/Http/Controllers/CertificateController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewCertificate()`, `viewCertificateAdd()`, `postAddCertificate()`, `getEditCertificate()`, `postUpdateCertificate()`, `changeCertificateStatus()`, `downloadCertificate()`
- **Controller**: `ConsentFormTemplateController` (`app/Http/Controllers/ConsentFormTemplateController.php`)
  - **Action Methods**: `getViewConsentFormTemplate()`, `addReportTemplate()`, `getdownloadconsentformTemplate()`, `postSaveReportData()`, `postSaveTempFile()`, `getEditReportTemplate()`, `geteditorval()`, `postEditReportData()`
- **Controller**: `EMROpenTemplateController` (`app/Http/Controllers/EMROpenTemplateController.php`)
  - **Action Methods**: `AddOpenFormatTemplate()`, `postAddOpenFormatTemplate()`, `postAddOpenFormatTemplate()`, `editEMROpenFormatTemp()`, `getEditOpenFormatTemplate()`, `getEditOpenFormatTemplate()`, `postUpdateOpenFormatTemplate()`, `postUpdateOpenFormatTemplate()`
- *(+18 more controllers handling CERTIFICATE TEMPLATE)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/createTemplate` | `TemplateController` | `getviewtemplate` | `web/api` |
| `GET` | `/addReportTemplate` | `ReportTemplateController` | `addReportTemplate` | `web/api` |
| `GET` | `/viewReportTemplate/{id?}` | `ReportTemplateController` | `viewReportTemplate` | `web/api` |
| `GET` | `/changereportemplateStatus/{id}/{status}` | `ReportTemplateController` | `changereportemplatestatus` | `web/api` |
| `GET` | `/deletereportemplate/{id}` | `ReportTemplateController` | `deletereportemplate` | `web/api` |
| `POST` | `/savetempfile` | `TemplateController` | `postSaveTempFile` | `web/api` |
| `POST` | `/savereportdata` | `ReportTemplateController` | `postSaveReportData` | `web/api` |
| `POST` | `/geteditorval` | `ReportTemplateController` | `geteditorval` | `web/api` |
| `GET` | `/editReportTemplate/{id?}` | `ReportTemplateController` | `getEditReportTemplate` | `web/api` |
| `GET` | `/detailedviewReporttemplate/{id?}` | `ReportTemplateController` | `getDetailedViewReportTemplate` | `web/api` |
| *...* | *+293 more routes mapped to CERTIFICATE TEMPLATE* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `ProcessHtmlTemplateEmbeddedFieldService` (`app/Services/ProcessHtmlTemplateEmbeddedFieldService.php`)
  - Methods: `init()`, `postProcessHTMLContentForPDF()`
- **Service**: `PageTemplateService` (`app/Services/PageTemplateService.php`)
  - Methods: `getUserBasedReferralDoctorList()`, `getUserBasedReferralReceptionList()`, `getReferralDoctorList()`, `OPIntRefNotification()`, `getDocumentCountAlert()`
- **Service**: `PanelTemplateService` (`app/Services/EMR/PanelTemplateService.php`)
  - Methods: `checkPanelTemplateApplicable()`, `TemplateSearchQuery()`, `checkselectedPanels()`, `PanelSearchQuery()`, `checkAlreadyExistTemplate()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: CHARTS (ID: CRT)

### 1. Module Overview & Navigation Structure
- **Module ID**: `CRT`
- **Module Name**: `CHARTS`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Appointment Charts, Billing Charts, Charts, Registration Charts
- **Discovered Sub-functions & Action Page Links** (4 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `APTCHARTS` | APPOINTMENT CHARTS | `getAppiontmentCharts` | Appointment Charts | - |
| `APTCHARTS` | APPOINTMENT CHARTS | `getAppiontmentCharts` | Charts | - |
| `BILCHARTS` | BILLING CHARTS | `getBillingCharts` | Billing Charts | - |
| `REGCHARTS` | REGISTRATION CHARTS | `getRegistrationCharts` | Registration Charts | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Associated Tables Count**: 6 tables identified
- **Key Tables**: `Patient_Perio_Dental_Chart`, `Patient_Perio_Dental_Chart_Value`, `Patient_Visit_Progress_Chart`, `Patient_Visit_Progress_Chart_Details`, `Patient_Visit_Progress_Chart_Images`, `User_Based_Dental_Advanced_Chart`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `Patient_Visit_Progress_Chart`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Patient_Visit_Progress_Chart_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Plan_Name` | `nvarchar` | 300 | NO | - |
| `Plan_Color_Code` | `nvarchar` | 10 | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

*Table: `Patient_Visit_Progress_Chart_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Patient_Visit_Progress_Chart_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Progress_Chart_Serial_No` | `bigint` | - | NO | - |
| `Date` | `date` | - | NO | - |
| `Plan_Value` | `smallint` | - | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

### 3. Eloquent Models & Data Architecture
- **Model**: `PatientVisitProgressChartDetails` (`app/Models/Patient/PatientVisitProgressChartDetails.php`)
  - **Database Table**: `Patient_Visit_Progress_Chart_Details` | **Primary Key**: `Patient_Visit_Progress_Chart_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Progress_Chart_Serial_No`, `Date`, `Plan_Value`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- **Model**: `PatientVisitProgressChartImages` (`app/Models/Patient/PatientVisitProgressChartImages.php`)
  - **Database Table**: `Patient_Visit_Progress_Chart_Images` | **Primary Key**: `Patient_Visit_Progress_Chart_Image_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Chart_Base64`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- **Model**: `PatientVisitProgressChart` (`app/Models/Patient/PatientVisitProgressChart.php`)
  - **Database Table**: `Patient_Visit_Progress_Chart` | **Primary Key**: `Patient_Visit_Progress_Chart_Serial_No`
  - **Constants / Status Flags**: `PROGRESS_CHART_PRE_DEFINE_CATEGORY = "144"`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Plan_Name`, `Plan_Color_Code`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`...
  - **Eloquent Relationships**: `hasMany(PatientVisitProgressChartDetails)` [Key/Pivot: `Patient_Visit_Progress_Chart_Serial_No`]

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `VitalsChartController` (`app/Http/Controllers/VitalsChartController.php`)
  - **Action Methods**: `getVitalDetails()`, `getVisitBasedDetails()`, `loadAllVitalRemarks()`, `loadAllEncounter()`
- **Controller**: `GrowthChartController` (`app/Http/Controllers/GrowthChartController.php`)
  - **Action Methods**: `viewGrowthChart()`, `getPatientGrowthChart()`, `getGrowthChartDetail()`, `splitDataForGraph()`, `convertToXYPair()`, `addXYKey()`, `parse_csv_file()`, `loadVisitBasedData()`
- **Controller**: `ProgressChartEmrPanelController` (`app/Http/Controllers/ProgressChartEmrPanelController.php`)
  - **Action Methods**: `viewProgressChartPanel()`, `saveProgressChartData()`, `initAuditLog()`, `getPatientProgressChartData()`, `patientDocumentAndVisitSummaryContent()`, `medicalReport()`, `progressChartEmbeddedFieldContent()`
- **Controller**: `AppointmentChartController` (`app/Http/Controllers/AppointmentChartController.php`)
  - **Action Methods**: `getAppiontmentCharts()`, `getAppointmentChartByType()`, `getAptCountByStatus()`, `getApptStatusNameByCode()`, `getAptCountByResource()`, `getAptCountBySpeciality()`, `printAppointmentChart()`
- **Controller**: `BillingChartController` (`app/Http/Controllers/BillingChartController.php`)
  - **Action Methods**: `getBillingCharts()`, `getBillingChartByType()`, `getCountByPaymentType()`, `getPaymentTypeNameByCode()`, `getAmountByPayment()`, `getAmountByResource()`
- **Controller**: `RegistrationChartController` (`app/Http/Controllers/RegistrationChartController.php`)
  - **Action Methods**: `getRegistrationCharts()`, `getRegistrationChartByType()`, `getPaymentTypeChart()`, `getPaymentTypeNameByCode()`, `getResourceChart()`, `getMonthChartForResource()`, `getRefResourceChart()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/getGlobalBillingChart` | `GlobalViewBillingController` | `getGlobalBillingChart` | `web/api` |
| `GET` | `/getBillingDetailForChart` | `GlobalViewBillingController` | `getBillingDetailForChart` | `web/api` |
| `GET` | `/lisWorkListpichartreg` | `LISServiceWorkListController` | `getlisWorkListpichartreg` | `web/api` |
| `GET` | `/getLISWorklistPieChart` | `LISServiceWorkListController` | `getLISWorklistPieChart` | `web/api` |
| `GET` | `/pichartDispatchLisWork` | `LISServiceWorkListController` | `getpichartDispatchLisWork` | `web/api` |
| `GET` | `/getLISDispatchPieChart` | `LISServiceWorkListController` | `getLISDispatchPieChart` | `web/api` |
| `GET` | `/getAppiontmentCharts/{id?}` | `AppointmentChartController` | `getAppiontmentCharts` | `web/api` |
| `POST` | `/getAppointmentChartByType` | `AppointmentChartController` | `getAppointmentChartByType` | `web/api` |
| `GET` | `/getRegistrationCharts/{id?}` | `RegistrationChartController` | `getRegistrationCharts` | `web/api` |
| `POST` | `/getRegistrationChartByType` | `RegistrationChartController` | `getRegistrationChartByType` | `web/api` |
| *...* | *+51 more routes mapped to CHARTS* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `DentalChartService` (`app/Services/EmbeddedFields/DentalChartService.php`)
  - Methods: `getDentalServiceDetails()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: COMMON (ID: COM)

### 1. Module Overview & Navigation Structure
- **Module ID**: `COM`
- **Module Name**: `COMMON`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Area, BRANCH BASED API, BRANCH BASED SMS TEMPLATE CONFIGURATION, BRANCH WISE PRINT CONFIGURATION, BULK MASTERS, Branch, Branch Based Email, Branch Based SMS, Branch Based Settings 1, Branch Based Settings 2
- **Discovered Sub-functions & Action Page Links** (81 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `AREA` | AREA | `area` | Area | - |
| `BRANCH` | BRANCH | `branch` | Branch | - |
| `BRANCHAPI` | BRANCH BASED API | `BranchBasedAPI` | BRANCH BASED API | Branch Based API |
| `BRBASEMAIL` | Branch Based Email | `viewBranchBasedEmail` | Branch Based Email | Description of Branch Based Email |
| `BRANCHSET` | BRANCH BASED SETTINGS | `viewBranchBasedSettings` | Branch Based Settings 1 | - |
| `BRANSTLIST` | BRANCH BASED SETTINGS LIST | `viewBranchBasedSettingsList` | Branch Based Settings 2 | - |
| `BRBASESMS` | Branch Based SMS | `viewBranchBasedSMS` | Branch Based SMS | - |
| `SMSTMPLATE` | BRANCH BASED SMS TEMPLATE CONFIGURATION | `sms-template/View` | BRANCH BASED SMS TEMPLATE CONFIGURATION | BRANCH BASED SMS TEMPLATE CONFIGURATION |
| `BRAECLAIM` | BRANCH ECLAIM | `branchEClaim` | Branch-Eclaim | - |
| `BRNENCPNL` | Branch Encounter Panel | `viewBranchBasedEncPanelAccess` | Branch Encounter Panel | - |
| `BrIPDCLIM` | Branch Wise IPD Claim Form | `getIPDClaimFormDet` | - | - |
| `BRANLIC` | Branch Wise License | `branchWiseLicenseDetails` | Branch Wise TRN | - |
| `BRWSEPRNT` | BRANCH WISE PRINT CONFIGURATION | `BrWisePrint/View` | BRANCH WISE PRINT CONFIGURATION | BRANCH WISE PRINT CONFIGURATION MASTER |
| `BREED` | BREED | `viewBreed` | Breed | - |
| `BLKMTRS` | BULK MASTER | `dashboard` | BULK MASTERS | Description of Bulk Master |
| *...* | *+66 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Branch_` (70 tables), `'Branch_` (1 tables), `Common_` (1 tables), `Company_` (5 tables), `Country_` (3 tables), `Department_` (4 tables)
- **Associated Tables Count**: 514 tables identified
- **Key Tables**: `'Branch_Based_PO_Settings'`, `AAA_Given_Additional_Stock_template_qmc`, `AAA_Given_Gender`, `AAA_Given_Speciality`, `AAA_Given_Stock_Template_QMC`, `AAA_Given_country`, `AAA_Given_nationality`, `AAA_given_Pharmacy_Stock_template`, `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Group`, `Allergy_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `User` (`app/Models/User.php`)
  - **Database Table**: `Users` | **Primary Key**: `User_Id`
  - **Constants / Status Flags**: `ADMIN_USER_USER_ID = "Admin"`
  - **Eloquent Relationships**: `hasMany(UserBasedGlobalFilter)` [Key/Pivot: `User_Id`], `hasMany(BranchBasedCacheSettings)` [Key/Pivot: `Created_By_User_Id`], `hasMany(BranchBasedCacheSettings)` [Key/Pivot: `Modified_By_User_Id`], `hasMany(UserDocumentationTab)` [Key/Pivot: `User_Id`]
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `BranchWiseDischargeGeneration` (`app/Models/BranchWiseDischargeGeneration.php`)
  - **Database Table**: `Branch_Wise_Discharge_Generation` | **Primary Key**: `Branch_Wise_Discharge_Generation_Serial_No`
  - **Fillable Attributes**: `Group_Code`, `Company_Code`, `Branch_Code`, `Current_Discharge_No`, `Discharge_No_Range_Start`, `Discharge_No_Rage_End`, `Discharge_Prefix`, `Created_By_User_Id`...
- **Model**: `GroupCompanyBranchLogo` (`app/Models/GroupCompanyBranchLogo.php`)
  - **Database Table**: `Group_Company_Branch_Logo` | **Primary Key**: `Group_Company_Branch_Logo_Serial_No`
- **Model**: `BranchBasedSettings` (`app/Models/BranchBasedSettings.php`)
  - **Database Table**: `Branch_Based_Settings` | **Primary Key**: `id`
- **Model**: `OriginBranchStockLocation` (`app/Models/OriginBranchStockLocation.php`)
  - **Database Table**: `Origin_Branch_Stock_Location` | **Primary Key**: `Origin_Branch_Stock_Location_Serial_No`
- *(+93 additional Eloquent models associated with COMMON)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PolicyInsuranceCompanyAndPlanController` (`app/Http/Controllers/PolicyInsuranceCompanyAndPlanController.php`)
  - **Action Methods**: `viewPolicyInsuranceCompanyAndPlan()`, `getAddPolicyInsuranceCompanyAndPlan()`, `getPolicyDescription()`, `getpaymentType()`, `getInsuranceCompanyName()`, `getpatientIncomenetworkName()`, `getInsurancePlanNames()`, `PostAddPolicyInsCmpyAndPlan()`
- **Controller**: `AnesthesiaTemplateController` (`app/Http/Controllers/AnesthesiaTemplateController.php`)
  - **Action Methods**: `postAnesthesia()`, `editAnesthesia()`, `updatedtAnesthesia()`, `viewAnesthesiaDetail()`, `changeAnesthesiaTemplateStatus()`, `viewAnesthesia()`, `addAnesthesiaTemplate()`, `getDepartmentBranchAutoComplete()`
- **Controller**: `InsuranceassociatecompanyController` (`app/Http/Controllers/InsuranceassociatecompanyController.php`)
  - **Action Methods**: `getIndex()`, `getAdd()`, `postAddinsuranceAssociate()`, `getInsuranceAssociatestatus()`, `getDeleteInsuranceAssociate()`, `getEditinsuranceAssociate()`, `postEditInsuranceAssociateCompany()`, `downloadInsuranceAssociateCompanyDetails()`
- **Controller**: `BranchBasedPurchaseInvoiceController` (`app/Http/Controllers/BranchBasedPurchaseInvoiceController.php`)
  - **Action Methods**: `viewBrnchBsePrchaseInv()`, `getdownloadPurchaseInv()`, `changeStatus()`, `getViewBrnchBsePrchaseInv()`, `getAddBrBsePurchaseInv()`, `GetCompany()`, `GetBranch()`, `postAddBrBsePurchaseInv()`
- **Controller**: `BranchWiseLicenseController` (`app/Http/Controllers/BranchWiseLicenseController.php`)
  - **Action Methods**: `getBranchWiseLicense()`, `addBranWiseLic()`, `postAddBranWiseLic()`, `editBranWiseLic()`, `postEditBranWiseLic()`, `getBranLicStatus()`, `downloadBranchLic()`
- **Controller**: `CompanyBasedInventoryInsuranceController` (`app/Http/Controllers/CompanyBasedInventoryInsuranceController.php`)
  - **Action Methods**: `viewCompanyBasedInventoryInsurance()`, `addCompanyBasedInventoryInsurance()`, `postAddCompanyBasedInventoryInsurance()`, `editCompanyBasedInventoryInsurance()`, `posteditCompanyBasedInventoryInsurance()`, `changeStatusCompanyBasedInventoryInsurance()`, `downloadCompanyBasedInventoryInsurance()`, `addItemBasedInventoryInsurance()`
- *(+178 more controllers handling COMMON)*

### 5. Form Requests & Input Validation Rules
- **Form Request**: `StoreEMRCommonMastersTypeRequest` (`app/Http/Requests/StoreEMRCommonMastersTypeRequest.php`)
  - **Validation Rules**:
    - `//         EMR_Common_Type_Description => required|string|max:200`
    - `//         Order_Sequence => required|integer`
    - `//         Branch_Code => required|string|max:20|unique:EMR_Common_Masters_Type,Branch_Code`
    - `//         selectedData.*.EMR_Common_Description => required|string|max:200`
    - `//         selectedData.*.Textbox_Required => required|string|in:Y,N`
    - `//         selectedData.*.Score_Is_Applicable => required|string|in:Y,N`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/ldap/api/user-search` | `LDAPDiagnosticsController` | `searchUsers` | `web/api` |
| `GET` | `/userBaseBranch` | `ConnectionsController` | `changeUserBranch` | `web/api` |
| `GET` | `/viewInsParam/{id?}` | `InstallationParameterController` | `getInsParam` | `web/api` |
| `POST` | `/idntyTypebranExistsInDB` | `InstalledModulesController` | `postInstalledBranchExists` | `web/api` |
| `GET` | `/addCountry` | `CountryController` | `getAddCountry` | `web/api` |
| `POST` | `/addCountry` | `CountryController` | `postAddCountry` | `web/api` |
| `GET` | `/country/{id?}` | `CountryController` | `getAllCountries` | `web/api` |
| `POST` | `/country` | `CountryController` | `getAllCountries` | `web/api` |
| `GET` | `/editCountry/{code}` | `CountryController` | `getCountryToEdit` | `web/api` |
| `GET` | `/viewCountry/{code}` | `CountryController` | `getCountryToView` | `web/api` |
| *...* | *+2716 more routes mapped to COMMON* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `CommonService` (`app/Services/CommonService.php`)
  - Methods: `getRemittanceStatus()`, `getEncounterEndStatus()`, `getexistEncTypedata()`, `checkAcknowledgmentStatus()`, `checkRISServiceCompletedStatus()`
- **Service**: `BranchConfigurationService` (`app/Services/BranchConfigurationService.php`)
- **Service**: `BranchWiseLicenseService` (`app/Services/BranchWiseLicenseService.php`)
  - Methods: `get()`
- **Service**: `BranchBasedCacheService` (`app/Services/BranchBasedCacheService.php`)
  - Methods: `InsertUpdateBranchBasedSettings()`, `changestatus()`
- **Service**: `CreateOtherBranchOpReferralVisitService` (`app/Services/CreateOtherBranchOpReferralVisitService.php`)
  - Methods: `addPriorVisitFromOtherBranchToCurrentVisit()`, `addProirServicetoCurrentHimesVisit()`, `getPAServiceDetails()`, `getotherBranchServicetoCurrentBranchVisit()`, `getPAInsCardDetTOCurrBranchHAVisit()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: CONSENT FORM (ID: CON)

### 1. Module Overview & Navigation Structure
- **Module ID**: `CON`
- **Module Name**: `CONSENT FORM`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Consent Forms, Consent Service link, Consent Template, Patients Consent
- **Discovered Sub-functions & Action Page Links** (5 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `PNTCONFORM` | Common Patient Consent Form | `CommonPatientConsentForm` | - | - |
| `CONTEMP` | CONSENT FORM TEMPLATE | `viewConsentFormTemplate` | Consent Template | Configure Consent form templates |
| `CONTEMSER` | CONSENT FORMS TEMPLATE SERVICES | `viewConsentFormTemplateService` | Consent Service link | Link Consent Template to Service |
| `SERCONFORM` | PATIENT VISIT SERVICE CONSENT FORM | `viewConsentFormsPatientVisit` | Patients Consent | Manage Medical Consents |
| `SERCONFORM` | PATIENT VISIT SERVICE CONSENT FORM | `viewConsentFormsPatientVisit` | Consent Forms | Manage Medical Consents |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Consent_` (4 tables), `Form_` (2 tables), `Proforma_` (2 tables)
- **Associated Tables Count**: 69 tables identified
- **Key Tables**: `Allowances_Calculation_Formula`, `Benefits_Calculation_Formula`, `Body_Mass_Ponderal_Index_Formula`, `Body_Temperature_Conversion_Formula`, `Branch_Wise_IPD_Claim_Forms`, `Branch_Wise_Proforma_Invoice_Generation`, `Consent_Form_Category`, `Consent_Form_Template`, `Consent_Form_Template_Services`, `Consent_Form_Template_Signature`, `DDWC_Api_Information`, `Deductions_Calculation_Formula`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_Physician_Assessment_Form` (`app/Models/Patient_Visit_Physician_Assessment_Form.php`)
  - **Database Table**: `Patient_Visit_Physician_Assessment_Form` | **Primary Key**: `Patient_Visit_Physician_Assessment_Form_Serial_No`
  - **Constants / Status Flags**: `SAVE_COMPLETE_OPTION_NO = "N"`, `SAVE_COMPLETE_OPTION_COMPLETED = "C"`
- **Model**: `Patient_Visit_PAC_Assessment_Information_Details` (`app/Models/Patient_Visit_PAC_Assessment_Information_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Assessment_Information_Details` | **Primary Key**: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Assessment_Anaesthesia_Type`], `hasMany(Patient_Visit_PAC_Previous_Anaesthesia_History_Details)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Plan_Of_Care)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Airway_Definition)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Drugs_List)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`]
- **Model**: `GroupFormEncounterAssignment` (`app/Models/GroupFormEncounterAssignment.php`)
  - **Database Table**: `Group_Form_Encouter_Assignment` | **Primary Key**: `Group_Form_Encouter_Assignment_Serial_No`
  - **Fillable Attributes**: `User_Role_Speciality_Sub_Department_Branch_Serial_No`, `Panel_Group_Serial_No`, `Panel_Serial_No`, `Visit_Encounter_Type_Serial_No`, `Assigned_By_User_Id`, `Assigned_Date_Time`, `Unassigned_By_User_Id`, `Unassigned_Date_Time`...
- **Model**: `PatientVisitOptometristFormSlitLampExamination` (`app/Models/PatientVisitOptometristFormSlitLampExamination.php`)
  - **Database Table**: `Patient_Visit_Optometrist_Form_Slit_Lamp_Examination` | **Primary Key**: `Patient_Visit_Optometrist_Form_Slit_Lamp_Examination_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Patient_Visit_ICD_Notes`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- **Model**: `PatientVisitOptometristFormSlitLampExaminationDetails` (`app/Models/PatientVisitOptometristFormSlitLampExaminationDetails.php`)
  - **Database Table**: `Patient_Visit_Optometrist_Form_Slit_Lamp_Examination_Details` | **Primary Key**: `Patient_Visit_Optometrist_Form_Slit_Lamp_Examination_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Optometrist_Form_Slit_Lamp_Examination_Serial_No`, `EMR_Common_Masters_Serial_No`, `Result_Value`, `Eye_Position`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`...
  - **Eloquent Relationships**: `belongsTo(EMRCommonMasters)` [Key/Pivot: `EMR_Common_Masters_Serial_No`]
- **Model**: `PatientVisitBioPsychosocialFormulation` (`app/Models/Patient/PatientVisitBioPsychosocialFormulation.php`)
  - **Database Table**: `Patient_Visit_Bio_Psychosocial_Formulation` | **Primary Key**: `Patient_Visit_Bio_Psychosocial_Formulation_Serial_No`
  - **Constants / Status Flags**: `PANEL_PREDEFINED_CATEGORY_BIOPSYCHOSOCIAL = 145`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- *(+4 additional Eloquent models associated with CONSENT FORM)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `ServicesFormGroupingElementsController` (`app/Http/Controllers/ServicesFormGroupingElementsController.php`)
  - **Action Methods**: `viewServiceFormGroupingElements()`, `getAddServiceFormGroupingElements()`, `postAddServiceFormGroupingElements()`, `getEditServiceFormGroupingElements()`, `postEditServiceFormGroupingElements()`, `editServiceFormGroupingElementsActiveStatus()`, `editServiceFormGroupingElementsDeactiveStatus()`, `deleteServiceFormGroupingElements()`
- **Controller**: `BioPhychoSocialFormulationController` (`app/Http/Controllers/BioPhychoSocialFormulationController.php`)
  - **Action Methods**: `viewBioPhychoSocialFormulationStdPanel()`, `saveBioPsychosocialFormulation()`, `getBioPsychoSocialFormulationLatestData()`, `getBioPsychoSocialFormulationHistoryData()`, `patientDocumentAndVisitSummaryContent()`, `medicalReport()`, `initCommonsave()`, `initAuditLog()`
- **Controller**: `ConsentFormTemplateController` (`app/Http/Controllers/ConsentFormTemplateController.php`)
  - **Action Methods**: `getViewConsentFormTemplate()`, `addReportTemplate()`, `getdownloadconsentformTemplate()`, `postSaveReportData()`, `postSaveTempFile()`, `getEditReportTemplate()`, `geteditorval()`, `postEditReportData()`
- **Controller**: `IPDClaimFormController` (`app/Http/Controllers/IPDClaimFormController.php`)
  - **Action Methods**: `getIPDClaimFormDet()`, `getaddIPDClaimForm()`, `postAddIPDComClaimForm()`, `editIPDClaimForm()`, `posteditIPDClaimForm()`, `editStatusIPDClaimForm()`, `deleteIPDClaimForm()`
- **Controller**: `MedicalRecordFormController` (`app/Http/Controllers/MedicalRecordFormController.php`)
  - **Action Methods**: `GetmedicalRecordForm()`, `postMedicalRecordFormSave()`, `printhtmlcontent()`
- **Controller**: `ConsentFormPatientVisitController` (`app/Http/Controllers/ConsentFormPatientVisitController.php`)
  - **Action Methods**: `getViewPatientVisitConsentForms()`, `downloadPatientVisitConsentForm()`, `getPatientVisitConsentstatus()`, `getViewConsentFormTemplateService()`, `getViewConsentFormTemplate()`, `cancellConsentFormsPatientVisit()`, `getHeaderFooterConsentFormTemplate()`, `headerPAgeConsentFunction()`
- *(+22 more controllers handling CONSENT FORM)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/oldEMRimport` | `OldEMRJSONImportController` | `showForm` | `web/api` |
| `GET` | `/oldEMRimport` | `OldEMRJSONImportController` | `showForm` | `web/api` |
| `POST` | `/fillAnswerFormdata` | `AppointmentQuestionaryController` | `postFillAnswer_appointment_formdata` | `web/api` |
| `POST` | `/canvasSessionFormData` | `AppointmentQuestionaryController` | `postCanvasSessionFormData` | `web/api` |
| `POST` | `/regfillAnswerFormdata` | `RegistrationQuestionaryController` | `postFillAnswer_appointment_formdata` | `web/api` |
| `POST` | `/regcanvasSessionFormData` | `RegistrationQuestionaryController` | `postCanvasSessionFormData` | `web/api` |
| `POST` | `/postSerializedFormData` | `InsuranceCompanyBasedPriceUpdationController` | `postCompanyWisePriceUpdationSerializedFormData` | `web/api` |
| `GET` | `/postExportFormData` | `InsuranceCompanyBasedPriceUpdationController` | `downloadExportFormData` | `web/api` |
| `GET` | `/viewConsentFormTemplate/{id?}` | `ConsentFormTemplateController` | `getViewConsentFormTemplate` | `web/api` |
| `GET` | `/addConsentFormTemplate` | `ConsentFormTemplateController` | `addReportTemplate` | `web/api` |
| *...* | *+436 more routes mapped to CONSENT FORM* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `EMRFormAssemblyService` (`app/Services/EMRFormAssemblyService.php`)
  - Methods: `postEMRFormAssembly()`
- **Service**: `DefaultTimeFormatService` (`app/Services/DefaultTimeFormatService.php`)
  - Methods: `DefaultTimeformat()`
- **Service**: `ConsentFormAlert` (`app/Services/ConsentFormAlert.php`)
  - Methods: `consentFormAlertDetails()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: DECISION SUPPORT MANAGEMENT (ID: DSS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `DSS`
- **Module Name**: `DECISION SUPPORT MANAGEMENT`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (1 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `DECSUPP` | DECISION SUPPORT RULE | `decisionSupportManagement` | - | Business Rules Management System |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Decision_` (1 tables)
- **Associated Tables Count**: 11 tables identified
- **Key Tables**: `Decision_Support_Rule`, `Medical_Decision_Making_Assessment_Risk`, `Medical_Decision_Making_Assessment_Risk_Level`, `Medical_Decision_Making_Problem_Status`, `Medical_Decision_Making_Reviewed_Data`, `Patient_Visit_Medical_Decision_Making`, `Patient_Visit_Medical_Decision_Making_Assessment_Risk`, `Patient_Visit_Medical_Decision_Making_Data_Reviewed`, `Patient_Visit_Medical_Decision_Making_Details`, `Patient_Visit_Medical_Decision_Making_Problem_Status`, `Patient_Visit_Respiratory_Support`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DSSRuleBasedDecisionController` (`app/Http/Controllers/DS/DSSRuleBasedDecisionController.php`)
  - **Action Methods**: `getDSSRuleBasedDecision()`, `getDSSSatisfiedRuleDetails()`, `getAllRuleDataDetails()`, `super_unique()`, `getrulenamedetails()`, `getDSSPatientDemography()`, `getDSSPatientChiefComplaints()`, `ruleBasedResultOnlyShow()`
- **Controller**: `MedicalDecisionMakingStatusController` (`app/Http/Controllers/EM/MedicalDecisionMakingStatusController.php`)
  - **Action Methods**: `getDecisionMakngStatus()`, `getAddDecisionMakPrbStat()`
- **Controller**: `MedicalDecisionMakingReviewedDataController` (`app/Http/Controllers/EM/MedicalDecisionMakingReviewedDataController.php`)
  - **Action Methods**: `getAddDecisionMakRevwedData()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/viewDecisionMakngStatus/{id?}` | `MedicalDecisionMakingStatusController` | `getDecisionMakngStatus` | `web/api` |
| `GET` | `/viewAddDecisionMakPrbStat` | `MedicalDecisionMakingStatusController` | `getAddDecisionMakPrbStat` | `web/api` |
| `POST` | `/viewPostDecsnMakngPrbStatus` | `MedicalDecisionMakingStatusController` | `getPostDecsnMakngPrbStatus` | `web/api` |
| `GET` | `/viewEditDesgnmakngPrbStat/{id}` | `MedicalDecisionMakingStatusController` | `getEditDesgnmakngPrbStat` | `web/api` |
| `POST` | `/viewUpdateDesnmakngPrbStat/{id}` | `MedicalDecisionMakingStatusController` | `getUpdateDesnmakngPrbStat` | `web/api` |
| `GET` | `/viewStatusDecisnMakPrbStat/{id}/{status}` | `MedicalDecisionMakingStatusController` | `getStatusDecisnMakPrbStat` | `web/api` |
| `GET` | `/viewDeleteDecisnMakrbStat/{id}` | `MedicalDecisionMakingStatusController` | `getDeleteDecisnMakrbStat` | `web/api` |
| `GET` | `/viewDownloadMedPrbStatus` | `MedicalDecisionMakingStatusController` | `getDownloadMedPrbStatus` | `web/api` |
| `GET` | `/viewDecisionMakingReviewedData` | `MedicalDecisionMakingReviewedDataController` | `getViewDecisReviwedData` | `web/api` |
| `GET` | `/viewAddDecisionMakRevwedData` | `MedicalDecisionMakingReviewedDataController` | `getAddDecisionMakRevwedData` | `web/api` |
| *...* | *+18 more routes mapped to DECISION SUPPORT MANAGEMENT* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: DENTAL (ID: DEN)

### 1. Module Overview & Navigation Structure
- **Module ID**: `DEN`
- **Module Name**: `DENTAL`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (1 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `DENTALTAB` | DENTAL | `patientRegistration#tabviewDentalTab` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Dental_` (15 tables)
- **Associated Tables Count**: 42 tables identified
- **Key Tables**: `Dental_Bridging_Sub_Category`, `Dental_Category`, `Dental_Category_Details`, `Dental_Category_Details_Service_Mapping`, `Dental_Category_Template`, `Dental_Category_Template_Details`, `Dental_Category_Template_Details_bk_29_05_2026`, `Dental_Category_Template_Details_bkp`, `Dental_Teeth_Details`, `Dental_Teeth_Details_bkp_27_05_2026`, `Dental_Type`, `Dental_Type_Heading`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DentalCategoryDetailController` (`app/Http/Controllers/DentalCategoryDetailController.php`)
  - **Action Methods**: `addDentalCategory()`, `getDentalService()`, `postaddDentalCategory()`, `viewDentalCategory()`, `geteditStatusDentalCategory()`, `getdeleteDentalCategory()`, `editDentalCategory()`, `posteditDentalCategory()`
- **Controller**: `EMRDentalStdPanelController` (`app/Http/Controllers/EMRDentalStdPanelController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewAddPopup()`, `loadDentalSSDBBasedServices()`, `visitServiceListArrayDental()`, `getSelectedResourceinVisitDental()`, `getSSDBVisitDental()`, `getResourceDentalAuto()`, `getResourceServiceBasedSubDeptDental()`
- **Controller**: `PatientRegistrationImportController` (`app/Http/Controllers/PatientRegistrationImportController.php`)
  - **Action Methods**: `uploadPatientRegistration()`, `postPatientExcelUpload()`, `PostPatientRegistrationUpload()`, `insertPatBasicDet()`, `getPaymentAutoCompletePatUpload()`, `updateDefaultPaymentDetails()`, `AddPatientBilling()`, `addRefEntDetails()`
- **Controller**: `DentalController` (`app/Http/Controllers/DentalController.php`)
  - **Action Methods**: `ViewDental()`, `GetDentalCategoryDetails()`, `GetDentalTypeBasedOptions()`, `GetDentalTeethPartPosition()`, `GetDentalChartCommon()`, `GetDentalTeethDetails()`, `GetPerioDentalChartTypeByTab()`, `GetPeriodontalChartValueDetails()`
- **Controller**: `PatientRegistrationController` (`app/Http/Controllers/PatientRegistrationController.php`)
  - **Action Methods**: `getPatientBasicDetails()`, `getAddPatientBasicDetails()`, `postAddPatientBasicDetails()`, `checkForSupportedImageFormat()`, `fetchPatientOriginStateDetails()`, `fetchPatientOriginCityDetails()`, `fetchPatientOriginAreaDetails()`, `fetchCompanyDetailsBasedOnGroup()`
- **Controller**: `PatientRegistrationOpeningBalanceImportController` (`app/Http/Controllers/PatientRegistrationOpeningBalanceImportController.php`)
  - **Action Methods**: `uploadOpeningBalancePatientRegistration()`, `postOpeningBalancePatientExcelUpload()`, `postPatientRegistrationOpeningBalanceUpload()`, `insertPatientBasicDetails()`, `CreateVisit()`, `addServices()`, `AddPatientBilling()`, `addRefEntDetails()`
- *(+1 more controllers handling DENTAL)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/postUpdatePatientRegistration` | `RegistrationQuestionaryController` | `postUpdatePatientRegistration` | `web/api` |
| `GET` | `/viewEMRStdPanel` | `EMRVisitEntryPanelController` | `viewEMRDental` | `web/api` |
| `GET` | `/viewZeoPatientRegistration/{id?}` | `ZeoDemoRegController` | `viewPatientRegistration` | `web/api` |
| `GET` | `/addDentalCategory` | `DentalCategoryDetailController` | `addDentalCategory` | `web/api` |
| `POST` | `/postaddDentalCategory` | `DentalCategoryDetailController` | `postaddDentalCategory` | `web/api` |
| `GET` | `/viewDentalCategory/{id?}` | `DentalCategoryDetailController` | `viewDentalCategory` | `web/api` |
| `GET` | `/editStatusDentalCategory/{id?}` | `DentalCategoryDetailController` | `geteditStatusDentalCategory` | `web/api` |
| `GET` | `/deleteDentalCategory/{id?}` | `DentalCategoryDetailController` | `getdeleteDentalCategory` | `web/api` |
| `GET` | `/editDentalCategory/{id?}` | `DentalCategoryDetailController` | `editDentalCategory` | `web/api` |
| `POST` | `/posteditDentalCategory` | `DentalCategoryDetailController` | `posteditDentalCategory` | `web/api` |
| *...* | *+87 more routes mapped to DENTAL* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `DentalBridgingService` (`app/Services/DentalBridgingService.php`)
  - Methods: `tableExists()`, `getBridgingCategoryCode()`, `saveBridgeDetails()`, `deleteBridgeDetails()`, `copyActiveBridgesToTargetParent()`
- **Service**: `DentalTeethUpdateService` (`app/Services/DentalTeethUpdateService.php`)
  - Methods: `tableExists()`, `saveToothUpdate()`, `getActiveToothUpdate()`, `getToothNameUpdateMapForPatient()`, `getActiveToothUpdatesForPatient()`
- **Service**: `DentalChartService` (`app/Services/EmbeddedFields/DentalChartService.php`)
  - Methods: `getDentalServiceDetails()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: DISPATCH (ID: DIS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `DIS`
- **Module Name**: `DISPATCH`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Dispatch Results, GV Referral Patients
- **Discovered Sub-functions & Action Page Links** (3 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `DISPATCH` | GENERAL DISPATCH DETAILS | `viewDispatch` | Dispatch Results | Investigation Result Dispatch |
| `RIS` | RADIOLOGY INFORMATION SYSTEM | `dashboard` | - | - |
| `REFDASH` | Referrer Dashboard | `ReferrerDashboard` | GV Referral Patients | Global View of Referral patients |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Associated Tables Count**: 5 tables identified
- **Key Tables**: `EMR_User_Dashboard`, `LIS_Report_Dispatch_Details`, `LIS_Report_Dispatch_File_Details`, `Patient_Bill_Dispatch_Details`, `RIS_Report_Dispatch_Details`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `RISDispatchController` (`app/Http/Controllers/RISDispatchController.php`)
  - **Action Methods**: `fetchRISDispatchDetails()`, `getRISServiceDetailsByVisit()`, `getPatientForDispatch()`, `getRISReportPreview()`, `getRISVisitServiceByMail()`, `sendReportEmail()`, `getVisitServiceStatus()`, `RISDispatch()`
- **Controller**: `DashboardController` (`app/Http/Controllers/DashboardController.php`)
  - **Action Methods**: `getIndex()`
- **Controller**: `AutoDispatchController` (`app/Http/Controllers/AutoDispatchController.php`)
  - **Action Methods**: `AutoEmailDispatch()`, `AutoInvoiceDispatch()`, `sendLISRISReportAutoDispatch()`, `sendReportEmailAuto()`, `getcommonHeaderReportDispatch()`, `viewPatientRegistrationHeaderforlis()`, `getprintdeparmetbasedcomments()`, `getpdfparameteriKount()`
- **Controller**: `InventoryDashboardController` (`app/Http/Controllers/InventoryDashboardController.php`)
  - **Action Methods**: `getInventoryDashboard()`, `InventoryDashboardDetails()`
- **Controller**: `GeneralDispatchController` (`app/Http/Controllers/GeneralDispatchController.php`)
  - **Action Methods**: `viewDispatch()`, `fetchLISRISDispatchDetails()`, `printFinalReportView()`, `printLISRISReportView()`, `getVisitServiceStatus()`, `getPatientForDispatch()`, `getReferralClinicId()`, `getLISRISServiceDetailsByVisit()`
- **Controller**: `LISDispatchController` (`app/Http/Controllers/LISDispatchController.php`)
  - **Action Methods**: `fetchLISDispatchDetails()`, `getPatientForDispatch()`, `getLISServiceDetailsByVisit()`, `getVisitServiceStatus()`, `getVisitServiceStatusByManual()`, `getLISVisitServiceByMail()`, `LISServiceDispatchByMail()`, `getLISReportPreview()`
- *(+2 more controllers handling DISPATCH)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/InventoryDashboard/{id?}` | `InventoryDashboardController` | `getInventoryDashboard` | `web/api` |
| `POST` | `/InventoryDashboardDetails` | `InventoryDashboardController` | `InventoryDashboardDetails` | `web/api` |
| `GET` | `/viewDespatchdetails/{id?}` | `DespatchDetailsController` | `getDispatchdetails` | `web/api` |
| `GET` | `/listviewdispatch/{id}` | `DespatchDetailsController` | `getListDespatchDetails` | `web/api` |
| `GET` | `/lisReportDispatch` | `LISController` | `lisReportDispatch` | `web/api` |
| `GET` | `/LisCollectDispatch` | `LISServiceWorkListController` | `getLisCollectDispatch` | `web/api` |
| `GET` | `/searchLisWorkLisDispatch` | `LISServiceWorkListController` | `getsearchLisWorkLisDispatch` | `web/api` |
| `GET` | `/LisDispatchData` | `LISServiceWorkListController` | `getLisDispatchData` | `web/api` |
| `POST` | `/LisAddRisDispatch` | `LISServiceWorkListController` | `postLisAddRisDispatch` | `web/api` |
| *...* | *+73 more routes mapped to DISPATCH* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: DRY DOCKS WORLD CLINIC (ID: DWC)

### 1. Module Overview & Navigation Structure
- **Module ID**: `DWC`
- **Module Name**: `DRY DOCKS WORLD CLINIC`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: DDWC Department, DDWC GLobal View of Alcohol Testing, DDWC Masters, DDWC NonOpernational WorkingDays, DDWC Result Status, DDWC Result Status By Department, DDWC Skill Master, DRY DOCKS WORLD CLINIC
- **Discovered Sub-functions & Action Page Links** (10 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ALSTACHAN` | Alcohol Status Changed | `#` | - | Alcohol Result Status Changed desc |
| `ALCOHTEST` | AlcoholTesting | `#` | - | AlcoholTesting Desc |
| `DDWCDEP` | DDWC Department | `viewDDWCDepartment` | DDWC Department | - |
| `DDWCGLOB` | DDWC GLobal View of Alcohol Testing | `viewDDWCGlobalView` | DDWC GLobal View of Alcohol Testing | Description of DDWC Auto Scheduler |
| `DDWCNOWD` | DDWC NonOpernational WorkingDays | `viewNonOperationalWorkingDays` | DDWC NonOpernational WorkingDays | - |
| `DDWCRSTU` | DDWC Result Status | `viewResultStatus` | DDWC Result Status | - |
| `DDWCRSBD` | DDWC Result Status By Department | `viewResultStatusByDepartment` | DDWC Result Status By Department | - |
| `DDWCSM` | DDWC Skill Master | `viewSkillMasters` | DDWC Skill Master | - |
| `DDWC` | DRY DOCKS WORLD CLINIC | `#` | DRY DOCKS WORLD CLINIC | - |
| `DDWCMSTR` | DRY DOCKS WORLD CLINIC Masters | `#` | DDWC Masters | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Clinical_` (1 tables), `DDWC_` (15 tables)
- **Associated Tables Count**: 26 tables identified
- **Key Tables**: `Clinical_Assessments`, `DDWC_Alcohol_Testing_Notification_Log_Details`, `DDWC_Api_Information`, `DDWC_Auto_Schedule_Details`, `DDWC_Auto_Schedule_Details_Week`, `DDWC_Department`, `DDWC_Non_Opernational_Working_Days`, `DDWC_Non_Opernational_Working_Days_Details`, `DDWC_Patient_Leave_Details`, `DDWC_Patient_Order_Batch`, `DDWC_Patient_Order_Batch_Details`, `DDWC_Patient_Order_Batch_Details_Log`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `PatientVisitClinicalNotes` (`app/Models/PatientVisitClinicalNotes.php`)
  - **Database Table**: `Patient_Visit_Clinical_Notes` | **Primary Key**: `Patient_Visit_Clinical_Notes_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Notes_Description`, `Priority_Type`, `Branch_Code`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
  - **Eloquent Relationships**: `hasMany(PatientVisitBasicDetails)` [Key/Pivot: `Patient_Visit_Basic_Details_Serial_No`]
- **Model**: `Patient_Visit_Clinical_Pharmacist_Intervention` (`app/Models/Patient_Visit_Clinical_Pharmacist_Intervention.php`)
  - **Database Table**: `Patient_Visit_Clinical_Pharmacist_Intervention` | **Primary Key**: `Patient_Visit_Clinical_Pharmacist_Intervention_Serial_No`
  - **Eloquent Relationships**: `hasMany(Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical)` [Key/Pivot: `Patient_Visit_Clinical_Pharmacist_Intervention_Serial_No`]
- **Model**: `Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical` (`app/Models/Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical.php`)
  - **Database Table**: `Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical` | **Primary Key**: `Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRCommonMasters)` [Key/Pivot: `EMR_Common_Masters_Serial_No`]

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DDWCWebServiceController` (`app/Http/Controllers/DDWCWebServiceController.php`)
  - **Action Methods**: `APIExecuteQuery()`, `getPatientAbsencesDetailApi()`, `postEmployeeDetailApi()`, `postLeaveDetailApi()`, `postPatientAbsencesDetailApi()`, `postLeaveAPIinDetail()`, `EmployeeDetailtoPatientBasicDetails()`, `viewDDWCGlobalView()`
- **Controller**: `ClinicalAssController` (`app/Http/Controllers/ClinicalAssController.php`)
  - **Action Methods**: `getClinicalAssessments()`, `addClinicalAssessmentsDetails()`, `getClinicalAssAutoComplete()`, `postdata()`, `downloadClinicalAssType()`, `getEditStatusClinicalAss()`, `getDeleteClinicalAss()`, `getEditClinicalAss()`
- **Controller**: `JRDDWCController` (`app/Http/Controllers/JRDDWCController.php`)
  - **Action Methods**: `viewaptbasedstatus()`, `byAppointmentStatus()`, `viewResourcebasedrevenue()`, `viewResourcebasedrevenuenew()`, `viewDHA0102A02B()`, `viewDHA37()`, `viewDHA38()`, `viewDHA39()`
- **Controller**: `ReferalclinicwisevisitdetailsController` (`app/Http/Controllers/ReferalclinicwisevisitdetailsController.php`)
  - **Action Methods**: `getreports()`, `getviewclinicwisevisitreport()`, `printReferaldoctorvisitDetailReport()`
- **Controller**: `DDWCResultStatusByDepartmentController` (`app/Http/Controllers/DDWC/DDWCResultStatusByDepartmentController.php`)
  - **Action Methods**: `index()`, `add()`, `store()`, `edit()`, `update()`, `status()`, `Delete()`, `Download()`
- **Controller**: `AlcoholTestResultMailController` (`app/Http/Controllers/DDWC/AlcoholTestResultMailController.php`)
  - **Action Methods**: `getEmployeesDetails()`
- *(+6 more controllers handling DRY DOCKS WORLD CLINIC)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/getReferralClinicIdLIS` | `LISDispatchController` | `getReferralClinicId` | `web/api` |
| `GET` | `/getReferralClinicIdRIS` | `RISDispatchController` | `getReferralClinicId` | `web/api` |
| `GET` | `/referalclinicwisevisitdetail/{id?}` | `ReferalclinicwisevisitdetailsController` | `getreports` | `web/api` |
| `GET` | `/refcliwisevisit` | `ReferalclinicwisevisitdetailsController` | `getviewclinicwisevisitreport` | `web/api` |
| `GET` | `/getReferralClinicId` | `GeneralDispatchController` | `getReferralClinicId` | `web/api` |
| `GET` | `/getClinicalAssessments/{id?}` | `ClinicalAssController` | `getClinicalAssessments` | `web/api` |
| `GET` | `/getClinicalAssAutoComplete` | `ClinicalAssController` | `getClinicalAssAutoComplete` | `web/api` |
| `GET` | `/addClinicalAssessments` | `ClinicalAssController` | `addClinicalAssessmentsDetails` | `web/api` |
| `GET` | `/downloadClinicalAssType` | `ClinicalAssController` | `downloadClinicalAssType` | `web/api` |
| `GET` | `/editStatusClinicalAss/{id?}` | `ClinicalAssController` | `getEditStatusClinicalAss` | `web/api` |
| *...* | *+176 more routes mapped to DRY DOCKS WORLD CLINIC* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `OPReferralPAToClinicVisit` (`app/Services/OPReferralPAToClinicVisit.php`)
  - Methods: `loadPreviousApprPriorVisitPaymentDetails()`, `getOPReferralApprovedPAVisit()`
- **Service**: `DDWCAlcoholTestingLogService` (`app/Services/DDWCAlcoholTestingLogService.php`)
  - Methods: `createLogForAlcoholTestingAPIandMail()`, `createApiLog()`, `createMailLog()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: ELECTRONIC MEDICAL RECORDS (ID: EMR)

### 1. Module Overview & Navigation Structure
- **Module ID**: `EMR`
- **Module Name**: `ELECTRONIC MEDICAL RECORDS`
- **Database Active Status**: Active (`A`)
- **Associated Menus**:  EMR ROS Symptoms Abnormalities,  SAMPLE AUDIT LOG, Anesthesia Common Master, Anesthesia Record Master, Anesthesia Templates, Appetite, CRRT Nursing Documentation, Clinical Assessments, Color Identification, Dental Bridging Sub Category
- **Discovered Sub-functions & Action Page Links** (160 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `EMRMFSOCLH` |  EMR MED FAM SOCIAL HISTORY TYPES | `viewSocialHistory` | MED FAM SOCIAL HISTORY | - |
| `EMRROSSYMP` |  EMR ROS SYMPTOMS | `viewROSSymptoms` | EMR ROS Symptoms | - |
| `EMRVACMANF` |  EMR VACCINE MANUFACTURERS | `viewVaccineManufacturers` | EMR Vaccine Manufacturers | - |
| `ALLTASK` | ALL TASK | `viewEmailMessageComposing` | - | - |
| `EAMFMAST` | Anesthesia Common Master | `EMRCommon/getAnesthesiaMenu/1` | Anesthesia Common Master | - |
| `EARFMAST` | Anesthesia Record Master | `EMRCommon/AnesthesiaRecordView` | Anesthesia Record Master | - |
| `ANESTHESIA` | ANESTHESIA TEMPLATE | `viewAnesthesia` | Anesthesia Templates | - |
| `APPETITE` | APPETITE | `viewEmrAppetite` | Appetite | - |
| `APPT` | APPOINTMENT TAB | `appointment` | - | - |
| `BRASKASS` | Braden Skin Assessment | `view-BradenSkinAssessment-list` | - | Braden Skin Assessment |
| `BRNWSDRPM` | BRANCH WISE DRUG PHARMACY | `getViewBranchWisePharm` | Pharmacy Drugs | Pharmacy Drugs config. By branch |
| `CLINICASS` | CLINICAL ASSESSMENTS | `getClinicalAssessments` | Clinical Assessments | - |
| `CRRTNURDOC` | CRRT Nursing Documentation | `viewCRRTNursingMaster` | CRRT Nursing Documentation | CRRT Nursing Documentation |
| `DEBRGSUB` | Dental Bridging Sub Category | `viewDentalBridgingSubCategory` | Dental Bridging Sub Category | - |
| `DECADET` | Dental Category Details | `viewDentalCategory` | Dental Category Details | - |
| *...* | *+145 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Appointment_` (7 tables), `appointment_` (1 tables), `Clinical_` (1 tables), `EMR_` (173 tables), `Medical_` (4 tables), `Vitals_` (1 tables)
- **Associated Tables Count**: 214 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Appointment_Default_Speciality`, `Appointment_Merge_Counter`, `Appointment_Status_Type`, `Appointment_Visit_Questionnaire`, `Appointment_Visit_Questionnaire_Possible_Answers`, `Appointment_Visit_Questionnaire_Types`, `Appointment_Visit_Questionnaire_Types_Services`, `Bulk_Previous_Day_Visit_SMS`, `CONSULTATION$`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `EMRInventoryConsumption` (`app/Models/EMRInventoryConsumption.php`)
  - **Database Table**: `EMR_Inventory_Internal_Consumption` | **Primary Key**: `EMR_Inventory_Internal_Consumption_Serial_No`
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `PatientVisitEMRDischargeSummary` (`app/Models/PatientVisitEMRDischargeSummary.php`)
  - **Database Table**: `Patient_Visit_EMR_Discharge_Summary` | **Primary Key**: `Patient_Visit_EMR_Discharge_Summary_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Discharge_Summary_Description`, `Discharge_Type`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
  - **Eloquent Relationships**: `belongsTo(PatientVisitBasicDetails)` [Key/Pivot: `Patient_Visit_Basic_Details_Serial_No`], `hasOne(PatientVisitDischargeSummaryDetail)` [Key/Pivot: `Patient_Visit_EMR_Discharge_Summary_Details_Serial_No`]
- **Model**: `PatientVisitClinicalNotes` (`app/Models/PatientVisitClinicalNotes.php`)
  - **Database Table**: `Patient_Visit_Clinical_Notes` | **Primary Key**: `Patient_Visit_Clinical_Notes_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Notes_Description`, `Priority_Type`, `Branch_Code`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
  - **Eloquent Relationships**: `hasMany(PatientVisitBasicDetails)` [Key/Pivot: `Patient_Visit_Basic_Details_Serial_No`]
- **Model**: `PatientVisitCaseLoadDischargeDetails` (`app/Models/PatientVisitCaseLoadDischargeDetails.php`)
  - **Database Table**: `Patient_Visit_Case_Load_Discharge_Details` | **Primary Key**: `Patient_Case_Load_Discharge_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Discharged_Status`, `Discharged_By`, `EMR_Case_Load_Color_Identification_Serial_No`, `Reason`, `Remarks`, `Created_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(EmrCaseLoadColorIdentification)` [Key/Pivot: `EMR_Case_Load_Color_Identification_Serial_No`], `belongsTo(PatientVisitBasicDetails)` [Key/Pivot: `Patient_Visit_Basic_Details_Serial_No`], `belongsTo(PatientBasicDetails)` [Key/Pivot: `Patient_Basic_Details_Serial_No`]
- **Model**: `Patient_Visit_Clinical_Pharmacist_Intervention` (`app/Models/Patient_Visit_Clinical_Pharmacist_Intervention.php`)
  - **Database Table**: `Patient_Visit_Clinical_Pharmacist_Intervention` | **Primary Key**: `Patient_Visit_Clinical_Pharmacist_Intervention_Serial_No`
  - **Eloquent Relationships**: `hasMany(Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical)` [Key/Pivot: `Patient_Visit_Clinical_Pharmacist_Intervention_Serial_No`]
- *(+86 additional Eloquent models associated with ELECTRONIC MEDICAL RECORDS)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `EMRPprescriptionController` (`app/Http/Controllers/EMRPprescriptionController.php`)
  - **Action Methods**: `viewEprescription()`, `eprescribeDrugCode()`, `getPatientVisitDiagnosisDetails()`, `getEditPatientVisitDiagnosisDetails()`, `emrpatientDiagnosisdetails()`, `emreditpatientDiagnosisdetails()`, `getdrugviewdetails()`, `ajax_editdrugdetails()`
- **Controller**: `EMRCaseLoadColorIdentificationController` (`app/Http/Controllers/EMRCaseLoadColorIdentificationController.php`)
  - **Action Methods**: `index_old()`, `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy_old()`, `destroy()`
  - **Form Validation Rules**: txtStartDay => required|integer|gt:0; txtEndDay   => required|integer|gt:0|gte:txtStartDay; txtColourCode => required; txtStartDay => required|integer|gt:0
- **Controller**: `EmrVitalSwallowingController` (`app/Http/Controllers/EmrVitalSwallowingController.php`)
  - **Action Methods**: `viewEmrSwallowing()`, `addEmrSwallowing()`, `PostaddemrSwallowing()`, `editEmrSwallowing()`, `PosteditEmrSwallowing()`, `changeStatusEmrSwallowing()`, `downloadEmrSwallowing()`, `deleteEmrSwallowing()`
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `VitalReferenceRangeController` (`app/Http/Controllers/VitalReferenceRangeController.php`)
  - **Action Methods**: `AddVitalReferenceRange()`, `PostAddVitalReferenceRange()`, `VitalReferenceRange()`, `EditVitalReferenceRange()`, `PostEditVitalReferenceRange()`, `DeleteVitalReferenceRange()`, `ActionVitalReferenceRange()`, `DownloadVitalReferenceRange()`
- **Controller**: `GlobalViewOPInternalReferralController` (`app/Http/Controllers/GlobalViewOPInternalReferralController.php`)
  - **Action Methods**: `viewInternalReferral()`, `getGlobalViewInternalReferral()`, `getRegsiterForInternalRef()`, `OPIntRefNotification()`, `getGVTagDetails()`, `getViewOPReferralRemark()`, `getBranchBasedGlobalFilter()`, `getBranchBasedSpecialities()`
- *(+92 more controllers handling ELECTRONIC MEDICAL RECORDS)*

### 5. Form Requests & Input Validation Rules
- **Form Request**: `StoreEMRCommonMastersTypeRequest` (`app/Http/Requests/StoreEMRCommonMastersTypeRequest.php`)
  - **Validation Rules**:
    - `//         EMR_Common_Type_Description => required|string|max:200`
    - `//         Order_Sequence => required|integer`
    - `//         Branch_Code => required|string|max:20|unique:EMR_Common_Masters_Type,Branch_Code`
    - `//         selectedData.*.EMR_Common_Description => required|string|max:200`
    - `//         selectedData.*.Textbox_Required => required|string|in:Y,N`
    - `//         selectedData.*.Score_Is_Applicable => required|string|in:Y,N`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/viewOPInternalReferral/{id?}` | `GlobalViewOPInternalReferralController` | `viewInternalReferral` | `web/api` |
| `GET` | `/checkMobileAndUsername` | `OnlineAppointmentSchedulerController` | `checkMobileAndUsername` | `web/api` |
| `GET` | `/checkMobileAndUsernameEdit` | `OnlineAppointmentSchedulerController` | `checkMobileAndUsernameEdit` | `web/api` |
| `GET` | `/getAptSpeciality` | `OnlineAppointmentSchedulerController` | `getAptSpeciality` | `web/api` |
| `GET` | `/getAptSpecialityResource` | `OnlineAppointmentSchedulerController` | `getAptSpecialityResource` | `web/api` |
| `GET` | `/apsOnlineFetchResources` | `OnlineAppointmentSchedulerController` | `fetchResourceLists` | `web/api` |
| `GET` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `getEditOnlinePatient` | `web/api` |
| `POST` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `postEditOnlinePatient` | `web/api` |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/loadRemainingDrugRecords` | `DrugController` | `loadRemainingDrugRecordsToSearch` | `web/api` |
| *...* | *+1333 more routes mapped to ELECTRONIC MEDICAL RECORDS* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `EMRDiagnosisFilterService` (`app/Services/EMRDiagnosisFilterService.php`)
  - Methods: `getDiagnosis()`
- **Service**: `AppointmentSMS` (`app/Services/AppointmentSMS.php`)
  - Methods: `getAppointmentDetails()`
- **Service**: `IPPharmacyService` (`app/Services/IPPharmacyService.php`)
  - Methods: `checkPatientEMRAllergies()`, `getEPrescribePatientAllergies()`, `postPatientAllergiesReview()`
- **Service**: `AppointmentService` (`app/Services/AppointmentService.php`)
  - Methods: `getPatientAppointmentDetails()`
- **Service**: `GlobalViewofIPPharmacyService` (`app/Services/GlobalViewofIPPharmacyService.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: FEEDBACK (ID: PFB)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PFB`
- **Module Name**: `FEEDBACK`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Patient Feedback Branch Department, Patient Feedback Department, Patient Feedback Form, Patient Feedback Questions, Patient Satisfaction Survey, Survey Master
- **Discovered Sub-functions & Action Page Links** (6 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `PFB` | FEEDBACK | `#` | Patient Satisfaction Survey | Satisfaction Survey |
| `PFBK` | PATIENT FEEDBACK | `patientFeedback` | Patient Feedback Form | - |
| `PATFBBDQ` | PATIENT FEEDBACK BRANCH DEPARTMENT | `branchBasedDepartmentList` | Patient Feedback Branch Department | - |
| `PATFBDEPT` | PATIENT FEEDBACK DEPARTMENT | `patientFeedbackDepartment` | Patient Feedback Department | - |
| `PATFBM` | PATIENT FEEDBACK MASTERS | `#` | Survey Master | View & Manage Surveys |
| `PATFBQUES` | PATIENT FEEDBACK QUESTIONS | `patientFeedbackQuestions` | Patient Feedback Questions | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Associated Tables Count**: 6 tables identified
- **Key Tables**: `Himes_Client_Feedback`, `Patient_Feedback`, `Patient_Feedback_Department`, `Patient_Feedback_Department_Branch_Questions`, `Patient_Feedback_Notes`, `Patient_Feedback_Questions`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `patPortalFeedbackController` (`app/Http/Controllers/patPortalFeedbackController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewPatientPortalSystem()`
- **Controller**: `patientFeedbackRoute` (`app/Http/Controllers/Feedback/patientFeedbackRoute.php`)
  - **Action Methods**: RESTful defaults
- **Controller**: `PatientFeedbackController` (`app/Http/Controllers/Feedback/PatientFeedbackController.php`)
  - **Action Methods**: `checkForSupportedImageFormat()`, `getDepartmentDetails()`, `getBranchBasedDepartmentList()`, `getQuestionAutocomplete()`, `updateFeedbackDepartment()`, `updateDepartmentDetails()`, `deleteBranchDeptQuestionList()`, `insertDepartmentDetails()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/patientPortalSystem` | `patPortalFeedbackController` | `viewPatientPortalSystem` | `web/api` |
| `GET` | `/patientFeedbackDepartment/{id?}` | `PatientFeedbackController` | `departmentList` | `web/api` |
| `GET` | `/addFeedbackDepartment` | `PatientFeedbackController` | `getDepartmentDetails` | `web/api` |
| `POST` | `/addFeedbackDepartment` | `PatientFeedbackController` | `insertDepartmentDetails` | `web/api` |
| `GET` | `/editFeedbackDepartment/{code?}` | `PatientFeedbackController` | `updateFeedbackDepartment` | `web/api` |
| `POST` | `/editFeedbackDepartment/{code?}` | `PatientFeedbackController` | `updateDepartmentDetails` | `web/api` |
| `GET` | `/deleteFeedbackDepartment/{code?}` | `PatientFeedbackController` | `deleteFeedbackDepartmentDetails` | `web/api` |
| `GET` | `/downloadFeedbackDepartment` | `PatientFeedbackController` | `downloadDepartmentDetails` | `web/api` |
| `GET` | `/changefbDeptStatus/{deptCode}/{status}` | `PatientFeedbackController` | `changeFeedbackDeptstatus` | `web/api` |
| `POST` | `/addFeedbackDepartment/alreadyExists` | `PatientFeedbackController` | `alreadyexitsDepartment` | `web/api` |
| *...* | *+20 more routes mapped to FEEDBACK* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: HISTO PATHLOGIST (ID: HP)

### 1. Module Overview & Navigation Structure
- **Module ID**: `HP`
- **Module Name**: `HISTO PATHLOGIST`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: APS Masters, Global View Of APS Orders, Grossing Template, HP Branch Histopathology Setup, HP Laterality Type, HP Report Template, HP STAINER USER, HP Sample Type
- **Discovered Sub-functions & Action Page Links** (9 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `HPMSTR` | APS Masters | `#` | APS Masters | View & Manage APS Configs |
| `GVHISTO` | Global View Of APS Orders | `globalViewOfHistoPathology` | Global View Of APS Orders | Anatomical Pathology System |
| `HPMOD` | HISTO PATHLOGIST MODULE | `#` | - | Anatomical Pathology System |
| `HPBRASTUP` | HP BRANCH HISTOPATHOLOGY SETUP | `viewHPBranchHistopathologySetup` | HP Branch Histopathology Setup | - |
| `HPGROSTEMP` | HP Grossing Template | `viewGrossingTemplate` | Grossing Template | - |
| `HPREPTEMP` | HP REPORT TEMPLATE | `ViewHPReportTemplate` | HP Report Template | - |
| `HPSTINUSER` | HP STAINER USER | `viewHPStainerNameUsers` | HP STAINER USER | - |
| `HPLAPTYPE` | LATERALITY TYPE | `viewHPLateralityType` | HP Laterality Type | - |
| `HPSAMPTYPE` | SAMPLE TYPE | `viewHPSampleType` | HP Sample Type | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Histo_` (1 tables), `HP_` (16 tables)
- **Associated Tables Count**: 122 tables identified
- **Key Tables**: `DSR_Action_Allergies_Visit_History`, `DSR_Action_CPT_Visit_History`, `DSR_Action_Chief_Complaint_Visit_History`, `DSR_Action_Drug_Visit_History`, `DSR_Action_ICD_Visit_History`, `DSR_Action_Lab_Result_Visit_History`, `DSR_Action_Physical_Exam_Visit_History`, `DSR_Action_ROS_Visit_History`, `DSR_Action_Vitals_Visit_History`, `EMR_Med_Fam_Social_History_Alcohol`, `EMR_Med_Fam_Social_History_Alcohol_Notes`, `EMR_Med_Fam_Social_History_Alcohol_Notes_Users_Link`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `EMRMedFamSocialHistoryController` (`app/Http/Controllers/EMRMedFamSocialHistoryController.php`)
  - **Action Methods**: `statusSocialHistory()`
- **Controller**: `MedFamSocialHistoryCommonMasterController` (`app/Http/Controllers/MedFamSocialHistoryCommonMasterController.php`)
  - **Action Methods**: `index()`, `create()`, `show()`, `saveMedFamComModelDetails()`, `initMedFamSocHisComMasterBasedOnBranch()`, `deleteMedFamSocialHistoryComMasterDetail()`, `editMedFamSocHisComMaster()`, `updateMedFamSocialHistoryComMaster()`
- **Controller**: `HISTOController` (`app/Http/Controllers/HISTOController.php`)
  - **Action Methods**: `getHistoRegistration()`, `viewHistoGrossing()`, `getProcessingView()`, `getEmbeddingView()`, `viewHistoMicrotomy()`, `viewHistoSlides()`, `viewHistoSlideStaus()`, `postUpdateHtmlfile1212()`
- **Controller**: `EMRMedicalHistoryController` (`app/Http/Controllers/EMRMedicalHistoryController.php`)
  - **Action Methods**: `getviewCCHPIMedicalHistory()`, `MedFamSocHistoryList()`, `getHistoryDetail()`, `getHistoryDetailById()`, `getHistoryDetailList()`, `EMRAddMedHistory()`, `PostAddMFSHistory()`, `EMRDeleteMedHistory()`
- **Controller**: `EMRVisitHistoryController` (`app/Http/Controllers/EMRVisitHistoryController.php`)
  - **Action Methods**: `getPatientVisitHistorySearch()`, `loadVisitHistoryBasedDetails()`, `getPatientVisitDocuments()`, `getPatientVisitDocumentImage()`, `emrVisitHistorySearchTable()`, `getServiceDetails()`, `getVisitHistoryServiceBasedResults()`, `getDrugDetails()`
- **Controller**: `ItemTransHistoryController` (`app/Http/Controllers/ItemTransHistoryController.php`)
  - **Action Methods**: `ViewItemTransHistory()`, `ShowItemTransHistory()`, `ShowItemTransHistory()`, `ShowItemTransHistory()`, `getItemTransactionHistoryColumnOrder()`
- *(+13 more controllers handling HISTO PATHLOGIST)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/getBatchHistoryUrlADJ` | `StockPositiveAdjusTransController` | `getBatchHistoryUrlADJ` | `web/api` |
| `GET` | `/viewEMRROSHistory` | `EMRReviewOfSymptomController` | `viewEMRROSHistory` | `web/api` |
| `GET` | `/getROSHistoryPopup` | `EMRReviewOfSymptomController` | `getROSHistoryPopup` | `web/api` |
| `GET` | `/viewEMRPEHistory` | `EMRPhysicalExamController` | `viewEMRPEHistory` | `web/api` |
| `GET` | `/getPEHistoryPopup` | `EMRPhysicalExamController` | `getPEHistoryPopup` | `web/api` |
| `GET` | `/viewSocialHistory/{id?}` | `EMRMedFamSocialHistoryController` | `viewSocialHistory` | `web/api` |
| `GET` | `/addSocialHistory` | `EMRMedFamSocialHistoryController` | `addSocialHistory` | `web/api` |
| `POST` | `/postSocialHistory` | `EMRMedFamSocialHistoryController` | `postSocialHistory` | `web/api` |
| `GET` | `/editSocialHistory/{id}/{type}` | `EMRMedFamSocialHistoryController` | `editSocialHistory` | `web/api` |
| `POST` | `/postEditSocialHistory` | `EMRMedFamSocialHistoryController` | `postEditSocialHistory` | `web/api` |
| *...* | *+196 more routes mapped to HISTO PATHLOGIST* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `HistoryofIllnessService` (`app/Services/EmbeddedFields/HistoryofIllnessService.php`)
  - Methods: `getPatientVisitHistoryofIllness()`
- **Service**: `MedicalHistoryService` (`app/Services/EmbeddedFields/MedicalHistoryService.php`)
  - Methods: `getMedicalHistory()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: HISTO PATHOLOGY (ID: HIS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `HIS`
- **Module Name**: `HISTO PATHOLOGY`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Cytopathology, HP Stainer Name, HP Stainer Sub Category, Histopathology, Registration
- **Discovered Sub-functions & Action Page Links** (15 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `CYTOPANEL` | CYTO PANELS | `cytoPathologyPanels` | Cytopathology | Cytopathology Management System |
| `CYTOSLIDE` | CYTOLOGY SLIDE | `histoPatient/CytologySlide` | - | - |
| `CYTOSLDREQ` | CYTOLOGY SLIDE REQUEST | `histoPatient/CytologySlideRequest` | - | - |
| `HPREPORT` | Direct Reporting | `histoPatient/Report` | - | Direct Reporting |
| `EMBEDDING` | EMBEDDING | `HistoEmbedding` | - | - |
| `GROSSING` | GROSSING | `HistoGrossing` | - | - |
| `HISTOPANEL` | HISTO PANElS | `histoPathologyPanels` | Histopathology | Histopathology Management System |
| `HPPATREGIS` | HP REGISTRATION | `histoPatient/Registration` | Registration | Registration |
| `HPSTINAME` | HP STAINER NAME | `viewHPStainerName` | HP Stainer Name | - |
| `HPSTISUBC` | HP STAINER SUB CATEGORY | `viewHPStainerSubCategory` | HP Stainer Sub Category | - |
| `MICROTOMY` | MICROTOMY | `HistoMicrotomy` | - | - |
| `PROCESSING` | PROCESSING | `HistoProcessing` | - | - |
| `HPRPTVIEW` | Reporting Worklist | `globalViewOfHistoReports` | - | Reporting Worklist |
| `SLIDEREQ` | SLIDE REQUESTS | `HistoSlides` | - | - |
| `SLIDESTAT` | SLIDE STATUS | `HistoSlideStaus` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Histo_` (1 tables), `registration_` (2 tables), `Registration_` (1 tables), `Report_` (11 tables), `Reporting_` (1 tables)
- **Associated Tables Count**: 193 tables identified
- **Key Tables**: `Branch_Based_EMR_Panel_Report`, `Branch_Based_EMR_Panel_Report_Sub_Details`, `DHA_Report_Code`, `DSR_Action_Allergies_Visit_History`, `DSR_Action_CPT_Visit_History`, `DSR_Action_Chief_Complaint_Visit_History`, `DSR_Action_Drug_Visit_History`, `DSR_Action_ICD_Visit_History`, `DSR_Action_Lab_Result_Visit_History`, `DSR_Action_Physical_Exam_Visit_History`, `DSR_Action_ROS_Visit_History`, `DSR_Action_Vitals_Visit_History`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `HimesReportsScheduleDetailsLogs` (`app/Models/HimesReportsScheduleDetailsLogs.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details_Logs` | **Primary Key**: `Himes_Reports_Schedule_Details_Logs_Serial_No`
- **Model**: `ReportBasedBranch` (`app/Models/ReportBasedBranch.php`)
  - **Database Table**: `Report_Based_Branch_Details` | **Primary Key**: `Report_Based_Branch_User_Details_Serial_No`
- **Model**: `HimesReportsScheduleDetails` (`app/Models/HimesReportsScheduleDetails.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details` | **Primary Key**: `Himes_Reports_Schedule_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(ReportFunctionURL)` [Key/Pivot: `Report_Function_URL_Serial_No`]
- **Model**: `ReportFunctionURL` (`app/Models/ReportFunctionURL.php`)
  - **Database Table**: `Report_Function_URL` | **Primary Key**: `Report_Function_URL_Serial_No`
- **Model**: `Registration_Common_Masters` (`app/Models/Registration_Common_Masters.php`)
  - **Database Table**: `Registration_Common_Masters` | **Primary Key**: `Registration_Common_Masters_Serial_No`
- *(+11 additional Eloquent models associated with HISTO PATHOLOGY)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `UserTestResultReportingConroller` (`app/Http/Controllers/UserTestResultReportingConroller.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getviewusertestresultreprting()`, `getaddusertestresultreprting()`
- **Controller**: `GlobalViewRegistrationController` (`app/Http/Controllers/GlobalViewRegistrationController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewGlobalRegistration()`, `testglobalreg()`, `downloadglobal()`, `getgeneratePDF()`, `getgeneratePrint()`, `getPatientSearch()`, `temppatientsearchSession()`
- **Controller**: `UserTestResultReportingController` (`app/Http/Controllers/UserTestResultReportingController.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getViewUserTestResultReportingprivilages()`, `getAddUserTestResultReporting()`, `getservicevalues()`, `gettemplatedetails()`
- **Controller**: `EmrRadiologyReportController` (`app/Http/Controllers/EmrRadiologyReportController.php`)
  - **Action Methods**: `emrRadiologyReportgeneration()`, `getEmrRadiologyReportReviewed()`
- **Controller**: `NewReportTemplateController` (`app/Http/Controllers/NewReportTemplateController.php`)
  - **Action Methods**: `NewaddReportTemplate()`, `Ristemlateeditor()`, `getriseditorval()`, `PatientvisitpayemtdetailsPanel()`, `viewPatientHeader()`, `patientpaymentdetailpanel()`, `newpatientpaymentdetailpanel()`, `MultipletemplateEdit()`
- **Controller**: `reportJRSController1` (`app/Http/Controllers/reportJRSController1.php`)
  - **Action Methods**: `reportJRS()`, `reportdownJRS1()`, `reportdownJRS2()`
- *(+110 more controllers handling HISTO PATHOLOGY)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/testReport` | `TestReportController` | `gettestReportDetails` | `web/api` |
| `GET` | `/Reportpdfgeneration` | `TestReportController` | `getreportpdfgeneration` | `web/api` |
| `GET` | `/generatePDFreport` | `TestReportController` | `viewgeneratipdf` | `web/api` |
| `GET` | `/reportpdfgenetationtest` | `TestReportController` | `postreportpdfgeneration` | `web/api` |
| `GET` | `/viewReportSchedule/{id?}` | `ReportScheduleController` | `getListReportSchedule` | `web/api` |
| `GET` | `/editReportSchedule/{id?}` | `ReportScheduleController` | `getEditReportSchedule` | `web/api` |
| `GET` | `/runScheduleJob/{id?}` | `ReportScheduleController` | `runScheduleJob` | `web/api` |
| `GET` | `/editStatusReportSchedule/{id?}` | `ReportScheduleController` | `getEditStatusReportSchedule` | `web/api` |
| `GET` | `/deleteReportSchedule/{id?}` | `ReportScheduleController` | `getDeleteReportSchedule` | `web/api` |
| `GET` | `/reportSchedule/{id?}` | `ReportScheduleController` | `getViewReportSchedule` | `web/api` |
| *...* | *+1393 more routes mapped to HISTO PATHOLOGY* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `JasperReportDownloadForftp` (`app/Services/JasperReportDownloadForftp.php`)
  - Methods: `ReportDownloadForftp()`
- **Service**: `PODRegistrationService` (`app/Services/PODRegistrationService.php`)
  - Methods: `PODRegistrationSave()`, `updatePatientPODStatus()`, `insertOldVisitPOD()`, `getPODCategoryData()`, `getVisitPODCategoryData()`
- **Service**: `ReportGeneratorService` (`app/Services/ReportGeneratorService.php`)
  - Methods: `generateAndSend()`
- **Service**: `HimesReportService` (`app/Services/HimesReportService.php`)
- **Service**: `RegistrationCommonMasterService` (`app/Services/RegistrationCommonMasterService.php`)
  - Methods: `addRegistrationCommonMaster()`, `updateRegistrationCommonMaster()`, `getRegistrationCommonMasterdata()`, `getFamilyRelationshipdata()`, `getReferalClinicData()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: HR AND PAYROLL (ID: HRP)

### 1. Module Overview & Navigation Structure
- **Module ID**: `HRP`
- **Module Name**: `HR AND PAYROLL`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (1 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `HUMRES` | HR AND PAYROLL | `HRMain` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Employee_` (1 tables), `EmployeeDetails_` (2 tables), `Employees_` (30 tables), `HR_` (2 tables)
- **Associated Tables Count**: 36 tables identified
- **Key Tables**: `EmployeeDetails_CF_Log`, `EmployeeDetails_PHH`, `Employee_Appraisal`, `Employees`, `Employees_Accommodation`, `Employees_Allowances`, `Employees_Allowances_Increments`, `Employees_Attendance`, `Employees_Bank_Account_Details`, `Employees_Basic_Pay`, `Employees_Basic_Pay_Increments`, `Employees_Benefits`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `HRGradeController` (`app/Http/Controllers/HR/HRGradeController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `getNoticePeriodType()`, `getgradename()`, `viewGradeDefDetAdd()`, `getPostAddGradeDefinition()`, `getHREditGradeDefintn()`, `getupdateHrGradeDefinition()`, `hrGradeStatus()`
- **Controller**: `HRCommonController` (`app/Http/Controllers/HR/HRCommonController.php`)
  - **Action Methods**: `getUserId()`, `getHRBranch()`, `getHRDepBran()`, `getHRSubDep()`, `getHRSpeciality()`, `getHRDesignations()`, `getHRPositions()`, `getHRGender()`
- **Controller**: `HRPositionController` (`app/Http/Controllers/HR/HRPositionController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewPositionDef()`, `viewPositionDefDetAdd()`, `getPositionName()`, `getPostAddPositionDefinition()`, `getEditHRPosition()`, `getupdateHrPositionDef()`, `hrPositionStatus()`
- **Controller**: `HRMasterController` (`app/Http/Controllers/HR/HRMasterController.php`)
  - **Action Methods**: `getBranch()`, `getCompany()`, `getLeaveTypeAutoComplteData()`, `gethrVehicleAutoComplete()`, `posthrVehicleDataAdd()`, `posthrBranchVehicleStatusChange()`, `posthrDeleteBranchVehicle()`, `getHrDownloadBranchVehicle()`
- **Controller**: `HREmployeeEDBBenefitsController` (`app/Http/Controllers/HR/HREmployeeEDBBenefitsController.php`)
  - **Action Methods**: `getEmployeeEarningDeductionBenefit()`, `getAutoCompleteEDBBenefits()`, `getEDBBenefitsName()`, `getProcessForDurationType()`, `getCurrency()`, `getEDBEmployeeBank()`, `getBasicPayRange()`, `postEmployeeEDBBenefits()`
- **Controller**: `HumanResourceController` (`app/Http/Controllers/HR/HumanResourceController.php`)
  - **Action Methods**: `hrDashboard()`, `hrDependentBasicDetails()`, `hrDependentPassportDetails()`, `hrEmployeeDependentPassportDetails()`, `getEmployeeDependentDetails()`, `getEmployeeDependentPassprtDetails()`, `getEmployeeDependentVisaDetails()`, `getDependentVisaDetails()`
- *(+37 more controllers handling HR AND PAYROLL)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/hrEmployeeVehicle` | `HumanResourceController` | `getEmployeeVehicleDetails` | `web/api` |
| `GET` | `/viewHRPayRoll` | `HRMasterController` | `geviewHRPayRoll` | `web/api` |
| `GET` | `/viewpayrollReasontypePageLoad` | `HRMasterController` | `viewpayrollReasontypePageLoad` | `web/api` |
| `GET` | `/hrDownloadPayrollReasonTypes` | `HRMasterController` | `DownloadPayrollReasonTypes` | `web/api` |
| `GET` | `/hrEditPayrollReasonTypes` | `HRMasterController` | `gethrEditPayrollReasonTypes` | `web/api` |
| `POST` | `/hrPayrollReasonTypeEdit` | `HRMasterController` | `posthrPayrollReasonTypeEdit` | `web/api` |
| `GET` | `/viewPayrollReasonType` | `HRMasterController` | `getviewPayrollReasonType` | `web/api` |
| `GET` | `/addhrPayrollReasonCode` | `HRMasterController` | `addPayrollReasonType` | `web/api` |
| `POST` | `/hrPayrollReasonTypeAdd` | `HRMasterController` | `postPayrollReasonType` | `web/api` |
| `GET` | `/hrDeletePayrollReasonTypes` | `HRMasterController` | `hrDeletePayrollReasonTypes` | `web/api` |
| *...* | *+276 more routes mapped to HR AND PAYROLL* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: Incentive (ID: INT)

### 1. Module Overview & Navigation Structure
- **Module ID**: `INT`
- **Module Name**: `Incentive`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Incentive, Incentive Calculation, Incentive Department, Incentive Masters, Incentive Miscellaneous Income, Incentive Payment Type, Incentive Payment Type Deduction, Incentive Payments, Incentive Service Group, Incentive Service Group Department
- **Discovered Sub-functions & Action Page Links** (14 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `INT` | Incentive | `#` | Incentive | Incentive Calculation Module |
| `INCALCUL` | Incentive Calculation | `viewIncentiveCalculation` | Incentive Calculation | - |
| `INDEPT` | Incentive Department | `viewIncentDept` | Incentive Department | - |
| `INTMSTR` | Incentive Masters | `dashboard` | Incentive Masters | Incentive Calculation Master |
| `INMINCOME` | Incentive Miscellaneous Income | `viewIncentMiscellaneousIncome` | Incentive Miscellaneous Income | - |
| `INPAYTYPE` | Incentive Payment Type | `viewIncentPaymentType` | Incentive Payment Type | - |
| `INPTDEDUC` | Incentive Payment Type Deduction | `viewIncentPaymentType` | Incentive Payment Type Deduction | - |
| `INPAYDTAIL` | Incentive Payments | `viewIncentivePaymenDetails` | Incentive Payments | - |
| `INSERVGRP` | Incentive Service Group | `viewIncentServGrp` | Incentive Service Group | - |
| `INSGDLINK` | Incentive Service Group Department | `viewIncentServGrpDeptLink` | Incentive Service Group Department | - |
| `INSERVINEX` | Incentive Service Include Exclude | `viewIncentServIncludeExclude` | Incentive Service Include Exclude | - |
| `INUNGRPSER` | Resource Incentive Deduction | `viewIncentiveUnGroupService` | Resource Incentive Deduction | - |
| `INDEPTSERV` | Service Group Department | `viewIncentGrpDeptServ` | Service Group Department | - |
| `REINSERGRP` | Service Group Resource | `viewResourceIncentiveServiceGroup` | Service Group Resource | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Incentive_` (16 tables)
- **Associated Tables Count**: 17 tables identified
- **Key Tables**: `EMR_User_Dashboard`, `Incentive_Batch_No_Generation`, `Incentive_Batch_No_Generation_Details`, `Incentive_Batch_Paid_Payment_Details`, `Incentive_Batch_Processed_Payment_Details`, `Incentive_Calculation_Details`, `Incentive_Department`, `Incentive_Department_Service`, `Incentive_Department_Service_Group`, `Incentive_Department_Service_Group_Include_Exclude`, `Incentive_Department_Service_Un_Group_Service`, `Incentive_Miscellaneous_Income`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DashboardController` (`app/Http/Controllers/DashboardController.php`)
  - **Action Methods**: `getIndex()`
- **Controller**: `InventoryDashboardController` (`app/Http/Controllers/InventoryDashboardController.php`)
  - **Action Methods**: `getInventoryDashboard()`, `InventoryDashboardDetails()`
- **Controller**: `IncentiveCalculationController` (`app/Http/Controllers/IncentiveCalculationController.php`)
  - **Action Methods**: `viewIncentiveUnGroupService()`, `getIncAutoComplete()`, `copyIncentiveResDetails()`, `saveInsDeptUnSerValues()`, `loadIncentiveServiceGrid()`, `viewIncentiveCalculation()`, `loadDeptWiseCalculation()`, `loadDeptWiseCalculationCount()`
- **Controller**: `IncentiveServiceIncludeExcludeController` (`app/Http/Controllers/Incentive/IncentiveServiceIncludeExcludeController.php`)
  - **Action Methods**: `viewIncentServIncludeExclude()`, `postAddUpdateIncentServIncludeExclude()`, `getEditIncentServIncludeExclude()`, `statusUpdateIncentServIncludeExclude()`, `removeIncentServIncludeExclude()`, `apiViewIncentServIncludeExclude()`, `apiViewIncentServIncludeExcludeSearch()`, `apiPostAddUpdateIncentServIncludeExclude()`
- **Controller**: `IncentiveDepartmentController` (`app/Http/Controllers/Incentive/IncentiveDepartmentController.php`)
  - **Action Methods**: `viewIncentDept()`, `postAddUpdateIncentDept()`, `getEditIncentDept()`, `statusUpdateIncentDept()`, `removeIncentDept()`, `apiViewIncentDept()`, `apiViewIncentDeptSearch()`, `apiPostAddUpdateIncentDept()`
- **Controller**: `IncentivePaymentTypeDeductionController` (`app/Http/Controllers/Incentive/IncentivePaymentTypeDeductionController.php`)
  - **Action Methods**: `viewIncentPayTypeDeduction()`, `postAddUpdateIncentPayTypeDeduction()`, `getEditIncentPayTypeDeduction()`, `statusUpdateIncentPayTypeDeduction()`, `apiViewIncentPayTypeDeduction()`, `apiViewIncentPayTypeDeductionSearch()`, `apiPostAddUpdateIncentPayTypeDeduction()`, `apiGetEditIncentPayTypeDeduction()`
- *(+8 more controllers handling Incentive)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/InventoryDashboard/{id?}` | `InventoryDashboardController` | `getInventoryDashboard` | `web/api` |
| `POST` | `/InventoryDashboardDetails` | `InventoryDashboardController` | `InventoryDashboardDetails` | `web/api` |
| `GET` | `/hrDashboard` | `HRPayrollDashboardController` | `hrDashboard` | `web/api` |
| `GET` | `/getHRDashboardEmployeePiechart` | `HRPayrollDashboardController` | `getHRDashboardEmployeePiechart` | `web/api` |
| `GET` | `/ReferrerDashboard/{id?}` | `ReferrerLoginController` | `ReferrerDashboard` | `web/api` |
| `GET` | `/viewIncentiveUnGroupService/{id?}` | `IncentiveCalculationController` | `viewIncentiveUnGroupService` | `web/api` |
| `GET` | `/getIncAutoComplete` | `IncentiveCalculationController` | `getIncAutoComplete` | `web/api` |
| `GET` | `/copyIncentiveResDetails` | `IncentiveCalculationController` | `copyIncentiveResDetails` | `web/api` |
| `GET` | `/saveInsDeptUnSerValues` | `IncentiveCalculationController` | `saveInsDeptUnSerValues` | `web/api` |
| *...* | *+133 more routes mapped to Incentive* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: INSURANCE (ID: INS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `INS`
- **Module Name**: `INSURANCE`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Claim Dashboard, Claim Payment Bank, Claim RA Files Details, Claim Status, Claim Tracking, Claim Type, E-Claim Management, E-Claim Masters, E-Claims, GV Claim Search
- **Discovered Sub-functions & Action Page Links** (23 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `CLAIMMERGE` | Claim Merge | `claimmerge` | - | - |
| `INSOBSOUT` | Claim Observation from Outsource Visit | `#` | - | - |
| `INSCLMBANK` | CLAIM PAYMENT BANK | `viewPaymentBankDetails` | Claim Payment Bank | - |
| `CLMSTATUS` | CLAIM STATUS | `viewClaimStatus` | Claim Status | - |
| `CLAIMTAB` | CLAIM TAB | `previous_value` | - | - |
| `CLAIMTYPE` | CLAIM TYPE | `viewclaimtype` | Claim Type | - |
| `GLBCLMSRC` | GLOBAL CLAIM SEARCH | `viewGlobalSearchTransaction` | GV Claim Search | Global View of claim search |
| `GLOBVCLATR` | GLOBAL VIEW CLAIM TRACKING | `ViewClaimTracking` | Claim Tracking | Track a specific claim |
| `CLMEXPORT` | Global view of claim extraction | `viewClaimExtractionDetails` | Global view of claim extraction | Batch wise claim extraction |
| `GVCLMRAFL` | GLOBAL VIEW OF CLAIM RAFILES | `viewGlobalClaimRAFiles` | Claim RA Files Details | Claim RA Files New and Downloaded |
| `GLBVEINS` | Global View of Insurance | `viewInsuranceModule` | E-Claim Management | View & Manage Claims |
| `DOCDETINS` | INS Patient Document Details | `previous_value` | - | - |
| `INCMINVGEN` | INSURANCE CLAIM INVOICE GENERATION | `viewInsClmInvioceGeneration` | Insurance Claim Invoice Generation | - |
| `INSCMFLNAM` | INSURANCE COMPANY FILE NAME | `getViewInsComFileName` | Insurance Company File Name | - |
| `INSDASHBD` | INSURANCE DASHBOARD | `viewInsuranceDashboard` | Claim Dashboard | Remittance Progress Overview |
| *...* | *+8 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Claim_` (42 tables), `Insurance_` (38 tables), `insurance_` (1 tables)
- **Associated Tables Count**: 209 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bill_Auto_Eclaim_Post_Close`, `Branch_EClaim_Link`, `Branch_Wise_IPD_Claim_Forms`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `CPT_InsuranceDept`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `StockItemInsurancePrice` (`app/Models/StockItemInsurancePrice.php`)
  - **Database Table**: `Stock_Item_Insurance_Price` | **Primary Key**: `Stock_Item_Insurance_Price_Serial_No`
- **Model**: `SecondaryCardDetails` (`app/Models/SecondaryCardDetails.php`)
  - **Database Table**: `Patient_Visit_Secondary_Insurance_Card_Details` | **Primary Key**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Insurance_Card_Details_Serial_No`, `Patient_Visit_Insurance_Remarks`, `Show_Remarks_Alert_In_Billing`, `Remarks_Read_In_Billing`, `Insurance_Plan_Serial_No`, `Insurance_Company_Serial_No`...
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `EncounterBasedClaimTime` (`app/Models/EncounterBasedClaimTime.php`)
  - **Database Table**: `Encounter_Based_Claim_Time` | **Primary Key**: `Encounter_Based_Claim_Time_Serial_No`
  - **Fillable Attributes**: `Effective_Start_Date`, `Visit_Encounter_Type_Serial_No`, `Encounter_Start_Time`, `Encounter_End_Time`, `Activity_Time`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
- **Model**: `ClaimRemittanceDetailsNotMatchedClaim` (`app/Models/ClaimRemittanceDetailsNotMatchedClaim.php`)
  - **Database Table**: `Claim_Remittance_Details_Not_Matched_Claims` | **Primary Key**: `Remittance_Details_Serial_No`
  - **Fillable Attributes**: `Remittance_WS_UniqueID`, `Hdr_SenderID`, `Hdr_ReceiverID`, `Hdr_TransactionDate`, `Hdr_RecordCount`, `Hdr_DispositionFlag`, `Claim_ID`, `Claim_IDPayer`...
- **Model**: `BranchEClaimLink` (`app/Models/BranchEClaimLink.php`)
  - **Database Table**: `Branch_EClaim_Link` | **Primary Key**: `Eclaim_Link_Serial_No`
  - **Fillable Attributes**: `Eclaim_Link_Name`, `Eclaim_Login_Name`, `Eclaim_Login_Password`, `Branch_Code`, `License_No`, `Insurance_Company_Serial_No`...
  - **Eloquent Relationships**: `belongsTo(Branch)` [Key/Pivot: `Branch_Code`]
- *(+38 additional Eloquent models associated with INSURANCE)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PolicyInsuranceCompanyAndPlanController` (`app/Http/Controllers/PolicyInsuranceCompanyAndPlanController.php`)
  - **Action Methods**: `viewPolicyInsuranceCompanyAndPlan()`, `getAddPolicyInsuranceCompanyAndPlan()`, `getPolicyDescription()`, `getpaymentType()`, `getInsuranceCompanyName()`, `getpatientIncomenetworkName()`, `getInsurancePlanNames()`, `PostAddPolicyInsCmpyAndPlan()`
- **Controller**: `InsuranceassociatecompanyController` (`app/Http/Controllers/InsuranceassociatecompanyController.php`)
  - **Action Methods**: `getIndex()`, `getAdd()`, `postAddinsuranceAssociate()`, `getInsuranceAssociatestatus()`, `getDeleteInsuranceAssociate()`, `getEditinsuranceAssociate()`, `postEditInsuranceAssociateCompany()`, `downloadInsuranceAssociateCompanyDetails()`
- **Controller**: `InsurancePlanPriorApprovalController` (`app/Http/Controllers/InsurancePlanPriorApprovalController.php`)
  - **Action Methods**: `getAddInsurancePlanPriorApproval()`, `postAddInsurancePlanPriorApproval()`, `getViewInsurancePlanPriorApproval()`, `getEditStatusInsurancePlanPriorApproval()`, `getDeleteInsurancePlanPriorApproval()`, `getDownloadInsurancePlanPriorApproval()`, `getEditInsurancePlanPriorApproval()`, `postEditInsurancePlanPriorApproval()`
- **Controller**: `CompanyBasedInventoryInsuranceController` (`app/Http/Controllers/CompanyBasedInventoryInsuranceController.php`)
  - **Action Methods**: `viewCompanyBasedInventoryInsurance()`, `addCompanyBasedInventoryInsurance()`, `postAddCompanyBasedInventoryInsurance()`, `editCompanyBasedInventoryInsurance()`, `posteditCompanyBasedInventoryInsurance()`, `changeStatusCompanyBasedInventoryInsurance()`, `downloadCompanyBasedInventoryInsurance()`, `addItemBasedInventoryInsurance()`
- **Controller**: `AutoEclaimPostController` (`app/Http/Controllers/AutoEclaimPostController.php`)
  - **Action Methods**: `viewAutoEclaim()`, `addAutoEclaim()`, `postAddAutoEclaim()`, `editAutoEclaim()`, `changeAutoEclaimStatus()`, `postUpdateAutoEclaim()`
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- *(+102 more controllers handling INSURANCE)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/insert` | `DummyController` | `ins` | `web/api` |
| `GET` | `/viewInsuranceCompany/{id}` | `InsurancecompanyController` | `getListInsuranceCompany` | `web/api` |
| `GET` | `/downloadInsuranceCompany` | `InsurancecompanyController` | `downloadInsuranceCompanyDetails` | `web/api` |
| `GET` | `/insurancePlanDrugDetails/{id?}` | `InsurancePlanDrugController` | `getInsurancePlanDrugDetails` | `web/api` |
| `GET` | `/addInsurancePlanDrug` | `InsurancePlanDrugController` | `getaddDrug` | `web/api` |
| `GET` | `/getDrugDetails` | `InsurancePlanDrugController` | `getDrugDetails` | `web/api` |
| `POST` | `/addInsurancePlanDrug` | `InsurancePlanDrugController` | `postaddDrug` | `web/api` |
| `GET` | `/getDrugByChecked` | `InsurancePlanDrugController` | `getDrug` | `web/api` |
| `GET` | `/editInsurancePlanDrug/{comSno}/{id?}` | `InsurancePlanDrugController` | `getEditDrug` | `web/api` |
| `POST` | `/postEditInsurancePlanDrug/{comSno}/{id?}` | `InsurancePlanDrugController` | `postEditDrug` | `web/api` |
| *...* | *+1083 more routes mapped to INSURANCE* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `ClaimMandatoryObservationTypeService` (`app/Services/ClaimMandatoryObservationTypeService.php`)
  - Methods: `saveClaimMandatoryObservationType()`, `getClaimMandatoryObservationTypedata()`, `changestatus()`, `ClaimMandatoryObservationTypeDownload()`, `getBranchBasedModule()`
- **Service**: `PharmacyEclaimValidationService` (`app/Services/PharmacyEclaimValidationService.php`)
  - Methods: `checkQuantityFullyReturned()`
- **Service**: `PostingMergeClaim` (`app/Services/PostingMergeClaim.php`)
  - Methods: `postMergeClaim()`, `insertMergeClaim()`, `mergeClaimIcdDiagnosis()`, `getAutoPostClaimApp()`, `getLISRISServiceStatus()`
- **Service**: `InsuranceEligibilityCheckRPAService` (`app/Services/InsuranceEligibilityCheckRPAService.php`)
  - Methods: `postPatientInsuranceEligibilityService()`, `getPatientInsuranceEligibilityCheckService()`, `postUpdatePatientInsuranceEligibilityService()`, `getPatientRPADetailService()`, `updatePatientInsuranceEligibilityUtilizeVisitService()`
- **Service**: `ClaimSubmission` (`app/Services/ClaimSubmission.php`)
  - Methods: `claimSubmissionFile()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: INVENTORY (ID: INV)

### 1. Module Overview & Navigation Structure
- **Module ID**: `INV`
- **Module Name**: `INVENTORY`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Abc Analysis, Ageing Analysis, Bar Codes, Bin Location, Branch Based GRN, Branch Based Purchase Invoice, Branch Based Purchase Order, Branch Based Purchase Request, Customer Contacts, Customer Master
- **Discovered Sub-functions & Action Page Links** (68 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ABCANALY` | ABC ANALYSIS | `ABCAnalysis` | Abc Analysis | - |
| `AEGANALY` | AGEING ANALYSIS | `AgeingAnalysis` | Ageing Analysis | - |
| `BARCODE` | BARCODE | `ViewBarcodeList` | Bar Codes | - |
| `BINLOC` | BIN LOCATION | `ViewBinLocation` | Bin Location | - |
| `BRBSEGRN` | BRANCH BASED GRN | `BrnchBaseGRN` | Branch Based GRN | BRANCH BASED GRN MASTER |
| `BRPRCHINVC` | BRANCH BASED PURCHASE INVOICE | `BrnchBsePrchaseInv` | Branch Based Purchase Invoice | BRANCH BASED PURCHASE INVOICE MASTER |
| `BRPRCHODR` | BRANCH BASED PURCHASE ORDER | `BrnchBsePrchaseOdr` | Branch Based Purchase Order | BRANCH BASED PURCHASE ORDER MASTER |
| `BRPRCHREQ` | BRANCH BASED PURCHASE REQUEST | `BrnchBsePrchaseReq` | Branch Based Purchase Request | BRANCH BASED PURCHASE REQUEST MASTER |
| `CUSTOMER` | CUSTOMER | `customers` | Customer Master | - |
| `CUSCONTACT` | CUSTOMER CONTACT | `CustomerContact` | Customer Contacts | - |
| `DOCGPSC` | DELIVERY NOTE CUM GATE PASS SERIES COUNTER | `GatePassSeriesCounter` | Delivery Note Cum Gate Pass Series Counter | - |
| `DELGATPAS` | DELIVERY NOTE-CUM-GATE PASS TRANSACTION | `DeliveryGatePassTransList` | Gate Pass | View & Manage Supplier Gate Passes |
| `FSNANALY` | FSN ANALYSIS | `FSNAnalysis` | Fsn Analysis | - |
| `INVGLBEREQ` | GLOBAL VIEW OF REQUEST | `globalViewOfRequest` | Material Request/Transfer | View & Manage In/Out Material Requets |
| `INVTRY` | INVENTORY | `dashboard` | - | - |
| *...* | *+53 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Inventory_` (13 tables), `Stock_` (21 tables)
- **Associated Tables Count**: 140 tables identified
- **Key Tables**: `AAA_AVH_Given_Stock_Sheet_Cons`, `AAA_AVH_Given_Stock_Sheet_Med`, `AAA_Avh_Given_Stock_Sheet_1`, `AAA_Avh_Stock_Item_Price_Temp`, `AAA_Given_Additional_Stock_template_qmc`, `AAA_Given_Stock_Template_QMC`, `AAA_given_Pharmacy_Stock_template`, `Adm_Inventory_ConsItem`, `Adm_Inventory_MedItem`, `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `StockItemInsurancePrice` (`app/Models/StockItemInsurancePrice.php`)
  - **Database Table**: `Stock_Item_Insurance_Price` | **Primary Key**: `Stock_Item_Insurance_Price_Serial_No`
- **Model**: `EMRInventoryConsumption` (`app/Models/EMRInventoryConsumption.php`)
  - **Database Table**: `EMR_Inventory_Internal_Consumption` | **Primary Key**: `EMR_Inventory_Internal_Consumption_Serial_No`
- **Model**: `StockItemPrice` (`app/Models/StockItemPrice.php`)
  - **Database Table**: `Stock_Item_Price` | **Primary Key**: `Stock_Item_Price_Serial_No`
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory` (`app/Models/Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory.php`)
  - **Database Table**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory` | **Primary Key**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory_Serial_No`
- **Model**: `ItemMaster` (`app/Models/ItemMaster.php`)
  - **Database Table**: `Item_Master` | **Primary Key**: `Item_Master_Serial_No`
- *(+29 additional Eloquent models associated with INVENTORY)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `CompanyBasedInventoryInsuranceController` (`app/Http/Controllers/CompanyBasedInventoryInsuranceController.php`)
  - **Action Methods**: `viewCompanyBasedInventoryInsurance()`, `addCompanyBasedInventoryInsurance()`, `postAddCompanyBasedInventoryInsurance()`, `editCompanyBasedInventoryInsurance()`, `posteditCompanyBasedInventoryInsurance()`, `changeStatusCompanyBasedInventoryInsurance()`, `downloadCompanyBasedInventoryInsurance()`, `addItemBasedInventoryInsurance()`
- **Controller**: `StockItemTaxTypeController` (`app/Http/Controllers/StockItemTaxTypeController.php`)
  - **Action Methods**: `viewStockItemTaxType()`, `addStockItemTaxType()`, `postAddStockItemTaxType()`, `editStockItemTaxType()`, `postEditStockItemTaxType()`, `changeStatusStockItemTaxType()`, `downloadStockItemTaxType()`, `deleteStockItemTaxType()`
- **Controller**: `StockItemDiscountController` (`app/Http/Controllers/StockItemDiscountController.php`)
  - **Action Methods**: `viewStockItemDiscount()`, `addStockItemDiscount()`, `getStockItemBasedDrug()`, `posAddStockItemDiscount()`, `editStockItemDiscount()`, `posEditStockItemDiscount()`, `changeStockItemDiscountStatus()`, `downloadStockItemDiscount()`
- **Controller**: `PhysicalvsComputerController` (`app/Http/Controllers/PhysicalvsComputerController.php`)
  - **Action Methods**: `getPhysicalvsComputerList()`, `getPhysicalvsComputerAdd()`, `ProcessPhysicalStockAdd()`, `PostAddPhysicalStock()`, `RemoveItemDetailByBinLoc()`, `getPhysicalvsComputerEdit()`, `getPhysicalStockItems()`, `ProcessPhysicalStockEdit()`
- **Controller**: `StockReturnToSupplierTransController` (`app/Http/Controllers/StockReturnToSupplierTransController.php`)
  - **Action Methods**: `getStockReturnToSupplierTransactionList()`, `getAddStockReturnToSupplierTransaction()`, `ProcessOnReturntoSupplierItems()`, `getEditStockReturnToSupplierTransaction()`, `getCancelStockReturnToSupplierTransaction()`, `AddStockReturnToSuppTransID()`, `postStockReturnToSupplierAdd()`, `updateInwardTransaction()`
- **Controller**: `InventoryReasonController` (`app/Http/Controllers/InventoryReasonController.php`)
  - **Action Methods**: `getAllInvReason()`, `getAddInvReason()`, `postAddInvReason()`, `getInvReasonToEdit()`, `postUpdateInvReason()`, `deleteInvReason()`, `downloadAllInvReason()`, `changeStatus()`
- *(+57 more controllers handling INVENTORY)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/universalCodeGroupsValues/{id?}` | `UniversalCodeGroupsValuesController` | `getIndex` | `web/api` |
| `GET` | `/loadUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `loadUniversalCodeGroupValues` | `web/api` |
| `GET` | `/CheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `CheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/EditCheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `EditCheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `getAddUniversalCodeGroupValues` | `web/api` |
| `POST` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `postAddUniversalCodeGroupValues` | `web/api` |
| `GET` | `/changeUniversalCodeGroupValuestatus/{id}/{status}` | `UniversalCodeGroupsValuesController` | `getChangeUniversalCodeGroupValuestatus` | `web/api` |
| `GET` | `/deletUniversalCodeGroupValue/{id}` | `UniversalCodeGroupsValuesController` | `getDeletUniversalCodeGroupValue` | `web/api` |
| `GET` | `/downloadUniversalcodeGroupValues` | `UniversalCodeGroupsValuesController` | `downloadUniversalcodeGroupValues` | `web/api` |
| *...* | *+929 more routes mapped to INVENTORY* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `Inventory` (`app/Services/Inventory.php`)
  - Methods: `referenceDocument()`, `stockTransaction()`, `stockItem()`, `quantityManager()`, `getStockLocationCode()`
- **Service**: `StockItem` (`app/Services/InventoryServices/StockItem.php`)
  - Methods: `getItem()`, `update()`, `addQuantity()`, `deductQuantity()`, `addTransferInQuantity()`
- **Service**: `InventorySearchQuery` (`app/Services/InventoryServices/InventorySearchQuery.php`)
- **Service**: `ReferenceDocument` (`app/Services/InventoryServices/ReferenceDocument.php`)
  - Methods: `addHeader()`, `addDetail()`, `getRefDocTypeSNo()`, `generateReferenceDocNo()`, `referenceDocNoExists()`
- **Service**: `QuantityManager` (`app/Services/InventoryServices/CalculateManager.php`)
  - Methods: `calculateInventoryCalc()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: INVENTORY BILLING (ID: IBL)

### 1. Module Overview & Navigation Structure
- **Module ID**: `IBL`
- **Module Name**: `INVENTORY BILLING`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (0 total):
*(Core background or reporting module - navigation managed dynamically via service or API)*

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Billing_` (2 tables), `Inventory_` (13 tables)
- **Associated Tables Count**: 29 tables identified
- **Key Tables**: `Adm_Inventory_ConsItem`, `Adm_Inventory_MedItem`, `Billing_Deleted_Log_Details`, `Billing_Shipment_Details`, `Company_Based_Inventory_Insurance_Item_Price`, `Company_Based_Inventory_Insurance_Price`, `EMR_Inventory_Internal_Consumption`, `EMR_Inventory_Internal_Consumption_Batch`, `Insurance_Plan_Inventory_Coverage_Applicable_Encounter`, `Inventory_Activity`, `Inventory_Installation_Parameters`, `Inventory_Insurance_Company_Patient_Income_Network`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `Billing_Deleted_Log_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Billing_Deleted_Log_Details_Serial_No` | `bigint` | - | NO | - |
| `Bill_Header_Serial_No` | `bigint` | - | NO | - |
| `Bill_Header_Json_Data` | `varchar` | -1 | YES | - |
| `Bill_Detail_Json_Data` | `varchar` | -1 | YES | - |
| `Bill_Amount_Received_Data` | `varchar` | -1 | YES | - |
| `Bill_Deposit_Json_data` | `varchar` | -1 | YES | - |
| `Page_Type` | `varchar` | 10 | YES | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `varchar` | 1 | NO | - |

### 3. Eloquent Models & Data Architecture
- **Model**: `EMRInventoryConsumption` (`app/Models/EMRInventoryConsumption.php`)
  - **Database Table**: `EMR_Inventory_Internal_Consumption` | **Primary Key**: `EMR_Inventory_Internal_Consumption_Serial_No`
- **Model**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory` (`app/Models/Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory.php`)
  - **Database Table**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory` | **Primary Key**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory_Serial_No`
- **Model**: `InventoryReasonType` (`app/Models/InventoryReasonType.php`)
  - **Database Table**: `Inventory_Reason_Type` | **Primary Key**: `Inventory_Reason_Type_Serial_No`
- **Model**: `PatientVisitDrugScheduleInventoryIVAdminstration` (`app/Models/PatientVisitDrugScheduleInventoryIVAdminstration.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_Inventory_IV_Administration` | **Primary Key**: `Patient_Visit_Drug_Schedule_Inventory_IV_Adminstration_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drugs_Scheduled_Inventory_Serial_No`, `IV_Start_Time`, `IV_End_Time`, `IV_Remarks`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`...
  - **Eloquent Relationships**: `hasMany(PatientVisitDrugScheduleInventoryIVAdminstrationLog)` [Key/Pivot: `Patient_Visit_Drug_Schedule_Inventory_IV_Adminstration_Serial_No`]
- **Model**: `InventoryInstallationParameters` (`app/Models/InventoryInstallationParameters.php`)
  - **Database Table**: `Inventory_Installation_Parameters` | **Primary Key**: `Inventory_Installation_Parameters_Serial_No`
- **Model**: `PatientVisitInventoryBilling` (`app/Models/PatientVisitInventoryBilling.php`)
  - **Database Table**: `Patient_Visit_Inventory_Billing` | **Primary Key**: `Patient_Visit_Inventory_Billing_Serial_No`
  - **Fillable Attributes**: `Inventory_Billing_Type`, `Patient_Basic_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No`, `Package_Service_Serial_No`, `Patient_Visit_Drugs_Prescribed_Serial_No`, `Running_Serial_No`, `Item_Drug_Link_Serial_No`...
- *(+3 additional Eloquent models associated with INVENTORY BILLING)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PatientBillingBackendController` (`app/Http/Controllers/PatientBillingBackendController.php`)
  - **Action Methods**: `modifyInvoiceDate()`, `UPDInvoiceDate()`, `modifyInvoiceReceipt()`, `UPDInvoiceReceipt()`, `UPDInvoiceReceiptAmt()`, `getInvoiceVisitRegisteredDateTime()`
- **Controller**: `CompanyBasedInventoryInsuranceController` (`app/Http/Controllers/CompanyBasedInventoryInsuranceController.php`)
  - **Action Methods**: `viewCompanyBasedInventoryInsurance()`, `addCompanyBasedInventoryInsurance()`, `postAddCompanyBasedInventoryInsurance()`, `editCompanyBasedInventoryInsurance()`, `posteditCompanyBasedInventoryInsurance()`, `changeStatusCompanyBasedInventoryInsurance()`, `downloadCompanyBasedInventoryInsurance()`, `addItemBasedInventoryInsurance()`
- **Controller**: `InventoryReasonController` (`app/Http/Controllers/InventoryReasonController.php`)
  - **Action Methods**: `getAllInvReason()`, `getAddInvReason()`, `postAddInvReason()`, `getInvReasonToEdit()`, `postUpdateInvReason()`, `deleteInvReason()`, `downloadAllInvReason()`, `changeStatus()`
- **Controller**: `InventoryMRPAutoUpdateStockLocationController` (`app/Http/Controllers/InventoryMRPAutoUpdateStockLocationController.php`)
  - **Action Methods**: `viewInvMRPAutoupdstkloc()`, `addInvMRPAutoupdstkloc()`, `postaddInvMRPAutoupdstkloc()`, `editInvMRPAutoupdstkloc()`, `posteditInvMRPAutoupdstkloc()`, `changeStatusInvMRPAutoupdstkloc()`, `downloadInvMRPAutoupdstkloc()`, `getInvMRPAutoupdstklocToDelete()`
- **Controller**: `GlobalViewRefundBillingController` (`app/Http/Controllers/GlobalViewRefundBillingController.php`)
  - **Action Methods**: `getViewGlobalAppointment()`, `getViewGlobal()`, `getspeciality()`, `getresource()`, `getPatientInvoice()`, `getbilbaranchdetls()`, `getname()`, `getnamesort()`
- **Controller**: `PatientBillingGetController` (`app/Http/Controllers/PatientBillingGetController.php`)
  - **Action Methods**: `getPatientBilling()`, `getPhyPrescribePatientAllergies()`, `getpatientbillinginvoicehistroy()`, `viewPatientBilling()`, `viewPatientBillingSearch()`, `getbillAddRowMore()`, `getBillCounter()`, `getAjaxAddReceivedPayment()`
- *(+37 more controllers handling INVENTORY BILLING)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/postServiceDeliveryInventory` | `AnesthesiaMedicationPanelController` | `postServiceDeliveryInventory` | `web/api` |
| `GET` | `/saveIVdrugScheduleInventoryDetails` | `AnesthesiaMedicationPanelController` | `saveIVdrugScheduleInventoryDetails` | `web/api` |
| `GET` | `/getInventoryIVScheduleDetails` | `AnesthesiaMedicationPanelController` | `getInventoryIVScheduleDetails` | `web/api` |
| `GET` | `/deleteInventoryIVScheduleDetails` | `AnesthesiaMedicationPanelController` | `deleteInventoryIVScheduleDetails` | `web/api` |
| `GET` | `/updateInventoryIVdrugScheduleDetails` | `AnesthesiaMedicationPanelController` | `updateInventoryIVdrugScheduleDetails` | `web/api` |
| `GET` | `/pauseInventoryIVAdministration` | `AnesthesiaMedicationPanelController` | `pauseInventoryIVAdministration` | `web/api` |
| `GET` | `/resumeInventoryIVAdministration` | `AnesthesiaMedicationPanelController` | `resumeInventoryIVAdministration` | `web/api` |
| `GET` | `/getInventoryIVConsumedVolumeCalculation` | `AnesthesiaMedicationPanelController` | `getInventoryIVConsumedVolumeCalculation` | `web/api` |
| `GET` | `/InvReason/{id?}` | `InventoryReasonController` | `getAllInvReason` | `web/api` |
| `GET` | `/addInventoryReason` | `InventoryReasonController` | `getAddInvReason` | `web/api` |
| *...* | *+460 more routes mapped to INVENTORY BILLING* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `PatientBillingServices` (`app/Services/PatientBillingServices.php`)
  - Methods: `validateInventoryItemAgainstPatient()`
- **Service**: `GlobalViewBillingService` (`app/Services/GlobalViewBillingService.php`)
- **Service**: `Inventory` (`app/Services/Inventory.php`)
  - Methods: `referenceDocument()`, `stockTransaction()`, `stockItem()`, `quantityManager()`, `getStockLocationCode()`
- **Service**: `StockItem` (`app/Services/InventoryServices/StockItem.php`)
  - Methods: `getItem()`, `update()`, `addQuantity()`, `deductQuantity()`, `addTransferInQuantity()`
- **Service**: `InventorySearchQuery` (`app/Services/InventoryServices/InventorySearchQuery.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: Inventory Consumption (ID: INC)

### 1. Module Overview & Navigation Structure
- **Module ID**: `INC`
- **Module Name**: `Inventory Consumption`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Inventory Cons, Inventory Consumption, InventoryConsumption
- **Discovered Sub-functions & Action Page Links** (3 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `INVCONSBAT` | Global View Of Inventory Consumption Batch | `viewEMRInventoryConsumptionBatch` | Inventory Consumption | View & Manage Inventory Consumption |
| `INVCONS` | Inventory Consumptions | `dashboard` | InventoryConsumption | Manage Inventory Consumptions |
| `INVCONS` | Inventory Consumptions | `dashboard` | Inventory Cons | Manage Inventory Consumptions |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Inventory_` (13 tables)
- **Associated Tables Count**: 27 tables identified
- **Key Tables**: `Adm_Inventory_ConsItem`, `Adm_Inventory_MedItem`, `Company_Based_Inventory_Insurance_Item_Price`, `Company_Based_Inventory_Insurance_Price`, `EMR_Inventory_Internal_Consumption`, `EMR_Inventory_Internal_Consumption_Batch`, `EMR_User_Dashboard`, `Insurance_Plan_Inventory_Coverage_Applicable_Encounter`, `Inventory_Activity`, `Inventory_Installation_Parameters`, `Inventory_Insurance_Company_Patient_Income_Network`, `Inventory_Insurance_Company_Patient_Income_Network_Items`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `EMRInventoryConsumption` (`app/Models/EMRInventoryConsumption.php`)
  - **Database Table**: `EMR_Inventory_Internal_Consumption` | **Primary Key**: `EMR_Inventory_Internal_Consumption_Serial_No`
- **Model**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory` (`app/Models/Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory.php`)
  - **Database Table**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory` | **Primary Key**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Inventory_Serial_No`
- **Model**: `InventoryReasonType` (`app/Models/InventoryReasonType.php`)
  - **Database Table**: `Inventory_Reason_Type` | **Primary Key**: `Inventory_Reason_Type_Serial_No`
- **Model**: `PatientVisitDrugScheduleInventoryIVAdminstration` (`app/Models/PatientVisitDrugScheduleInventoryIVAdminstration.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_Inventory_IV_Administration` | **Primary Key**: `Patient_Visit_Drug_Schedule_Inventory_IV_Adminstration_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drugs_Scheduled_Inventory_Serial_No`, `IV_Start_Time`, `IV_End_Time`, `IV_Remarks`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`...
  - **Eloquent Relationships**: `hasMany(PatientVisitDrugScheduleInventoryIVAdminstrationLog)` [Key/Pivot: `Patient_Visit_Drug_Schedule_Inventory_IV_Adminstration_Serial_No`]
- **Model**: `InventoryInstallationParameters` (`app/Models/InventoryInstallationParameters.php`)
  - **Database Table**: `Inventory_Installation_Parameters` | **Primary Key**: `Inventory_Installation_Parameters_Serial_No`
- **Model**: `PatientVisitInventoryBilling` (`app/Models/PatientVisitInventoryBilling.php`)
  - **Database Table**: `Patient_Visit_Inventory_Billing` | **Primary Key**: `Patient_Visit_Inventory_Billing_Serial_No`
  - **Fillable Attributes**: `Inventory_Billing_Type`, `Patient_Basic_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No`, `Package_Service_Serial_No`, `Patient_Visit_Drugs_Prescribed_Serial_No`, `Running_Serial_No`, `Item_Drug_Link_Serial_No`...
- *(+2 additional Eloquent models associated with Inventory Consumption)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `CompanyBasedInventoryInsuranceController` (`app/Http/Controllers/CompanyBasedInventoryInsuranceController.php`)
  - **Action Methods**: `viewCompanyBasedInventoryInsurance()`, `addCompanyBasedInventoryInsurance()`, `postAddCompanyBasedInventoryInsurance()`, `editCompanyBasedInventoryInsurance()`, `posteditCompanyBasedInventoryInsurance()`, `changeStatusCompanyBasedInventoryInsurance()`, `downloadCompanyBasedInventoryInsurance()`, `addItemBasedInventoryInsurance()`
- **Controller**: `InventoryReasonController` (`app/Http/Controllers/InventoryReasonController.php`)
  - **Action Methods**: `getAllInvReason()`, `getAddInvReason()`, `postAddInvReason()`, `getInvReasonToEdit()`, `postUpdateInvReason()`, `deleteInvReason()`, `downloadAllInvReason()`, `changeStatus()`
- **Controller**: `InventoryMRPAutoUpdateStockLocationController` (`app/Http/Controllers/InventoryMRPAutoUpdateStockLocationController.php`)
  - **Action Methods**: `viewInvMRPAutoupdstkloc()`, `addInvMRPAutoupdstkloc()`, `postaddInvMRPAutoupdstkloc()`, `editInvMRPAutoupdstkloc()`, `posteditInvMRPAutoupdstkloc()`, `changeStatusInvMRPAutoupdstkloc()`, `downloadInvMRPAutoupdstkloc()`, `getInvMRPAutoupdstklocToDelete()`
- **Controller**: `InventoryCommonController` (`app/Http/Controllers/InventoryCommonController.php`)
  - **Action Methods**: `getbranchPurchaseGRNTrans()`, `setCurStkLoc()`, `getAllStockTransactionType()`, `checkbalqty()`, `checkunitcost()`, `checkunitcostForIssue()`, `checkunitcostForRefDoc()`, `unitcostFormPriceList()`
- **Controller**: `InventoryController` (`app/Http/Controllers/InventoryController.php`)
  - **Action Methods**: `getAllBinLocation()`, `getAllInventoryReason()`, `getAllCustomer()`, `getAllcountry_base_currency_daily_exchange_rates()`, `getAllgroup()`, `getAllInventoryInstallationParameters()`, `getAllInventoryReasonType()`, `getAllcurrency()`
- **Controller**: `EMRInventoryBillingController` (`app/Http/Controllers/EMRInventoryBillingController.php`)
  - **Action Methods**: `getvisitEMR()`, `StrQuoteReplace()`, `getviewEMRInventoryBilling()`, `getVisitServices()`, `getVisitPrescription()`, `getStockLoc()`, `getItemDescList()`, `getItemDescList()`
- *(+17 more controllers handling Inventory Consumption)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/postServiceDeliveryInventory` | `AnesthesiaMedicationPanelController` | `postServiceDeliveryInventory` | `web/api` |
| `GET` | `/saveIVdrugScheduleInventoryDetails` | `AnesthesiaMedicationPanelController` | `saveIVdrugScheduleInventoryDetails` | `web/api` |
| `GET` | `/getInventoryIVScheduleDetails` | `AnesthesiaMedicationPanelController` | `getInventoryIVScheduleDetails` | `web/api` |
| `GET` | `/deleteInventoryIVScheduleDetails` | `AnesthesiaMedicationPanelController` | `deleteInventoryIVScheduleDetails` | `web/api` |
| `GET` | `/updateInventoryIVdrugScheduleDetails` | `AnesthesiaMedicationPanelController` | `updateInventoryIVdrugScheduleDetails` | `web/api` |
| `GET` | `/pauseInventoryIVAdministration` | `AnesthesiaMedicationPanelController` | `pauseInventoryIVAdministration` | `web/api` |
| `GET` | `/resumeInventoryIVAdministration` | `AnesthesiaMedicationPanelController` | `resumeInventoryIVAdministration` | `web/api` |
| `GET` | `/getInventoryIVConsumedVolumeCalculation` | `AnesthesiaMedicationPanelController` | `getInventoryIVConsumedVolumeCalculation` | `web/api` |
| `GET` | `/InvReason/{id?}` | `InventoryReasonController` | `getAllInvReason` | `web/api` |
| *...* | *+250 more routes mapped to Inventory Consumption* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `Inventory` (`app/Services/Inventory.php`)
  - Methods: `referenceDocument()`, `stockTransaction()`, `stockItem()`, `quantityManager()`, `getStockLocationCode()`
- **Service**: `StockItem` (`app/Services/InventoryServices/StockItem.php`)
  - Methods: `getItem()`, `update()`, `addQuantity()`, `deductQuantity()`, `addTransferInQuantity()`
- **Service**: `InventorySearchQuery` (`app/Services/InventoryServices/InventorySearchQuery.php`)
- **Service**: `ReferenceDocument` (`app/Services/InventoryServices/ReferenceDocument.php`)
  - Methods: `addHeader()`, `addDetail()`, `getRefDocTypeSNo()`, `generateReferenceDocNo()`, `referenceDocNoExists()`
- **Service**: `QuantityManager` (`app/Services/InventoryServices/CalculateManager.php`)
  - Methods: `calculateInventoryCalc()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: INVOICE POSTING (ID: INP)

### 1. Module Overview & Navigation Structure
- **Module ID**: `INP`
- **Module Name**: `INVOICE POSTING`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (0 total):
*(Core background or reporting module - navigation managed dynamically via service or API)*

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Invoice_` (1 tables)
- **Associated Tables Count**: 15 tables identified
- **Key Tables**: `Branch_Based_Purchase_Invoice`, `Branch_Wise_Invoice_Generation`, `Branch_Wise_Proforma_Invoice_Generation`, `Claim_Posting_Reposting_Log_Details`, `Insurance_Claim_Invoice_File_Name_Generation`, `Insurance_Claim_Invoice_Generation`, `Interim_Branch_Wise_Invoice_Generation`, `Invoice_Cancel_Request`, `Ledger_Posting_Batch`, `Ledger_Posting_Batch_Invoice`, `Pharmacy_Branch_Wise_Invoice_Generation`, `Proforma_Invoice_Patient_Bill_Detail_Services_Packages_Resources_Drugs`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `BranchBasedPurchaseInvoiceController` (`app/Http/Controllers/BranchBasedPurchaseInvoiceController.php`)
  - **Action Methods**: `viewBrnchBsePrchaseInv()`, `getdownloadPurchaseInv()`, `changeStatus()`, `getViewBrnchBsePrchaseInv()`, `getAddBrBsePurchaseInv()`, `GetCompany()`, `GetBranch()`, `postAddBrBsePurchaseInv()`
- **Controller**: `PackageInvoiceController` (`app/Http/Controllers/PackageInvoiceController.php`)
  - **Action Methods**: `printPackageInvoicePdf()`
- **Controller**: `InvoiceController` (`app/Http/Controllers/InvoiceController.php`)
  - **Action Methods**: `download()`
- **Controller**: `PatientVisitInvoiceDeactivateController` (`app/Http/Controllers/PatientVisitInvoiceDeactivateController.php`)
  - **Action Methods**: `viewPatientVisitInvoiceDetails()`, `PostPatientVisitInvoiceDetails()`, `getCheckUserBarcode()`, `Branchautocomplete()`, `loadcompanywisebranches()`
- **Controller**: `PatientBillingInvoiceLogDetailController` (`app/Http/Controllers/PatientBillingInvoiceLogDetailController.php`)
  - **Action Methods**: `InvoiceLogDetailByPatient()`, `printReceiptForInvLog()`
- **Controller**: `PurchaseInvoiceController` (`app/Http/Controllers/PurchaseInvoiceController.php`)
  - **Action Methods**: `getPurchaseInvoiceList()`, `PurchaseInvoiceHeaderList()`, `PurchaseInvoiceItemList()`, `PurchaseInvoiceDownload()`, `PurchaseInvoicePrint()`, `getPurchaseInvoiceAdd()`, `getPurchaseInvoiceEdit()`, `getPurchaseInvoiceCancel()`
- *(+22 more controllers handling INVOICE POSTING)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/invoice/download` | `InvoiceController` | `download` | `web/api` |
| `GET` | `/getPatientInvoice` | `GlobalViewPatientBillingController` | `getPatientInvoice` | `web/api` |
| `GET` | `/invoicePendingCodeModal` | `GlobalViewPatientBillingController` | `invoicePendingCodeModal` | `web/api` |
| `GET` | `/getPatientOutstandInvoice` | `GlobalViewOutstandBillingController` | `getPatientOutstandInvoice` | `web/api` |
| `GET` | `/InvoiceLogDetailByPatient` | `PatientBillingInvoiceLogDetailController` | `InvoiceLogDetailByPatient` | `web/api` |
| `GET` | `/printReceiptForInvLog` | `PatientBillingInvoiceLogDetailController` | `printReceiptForInvLog` | `web/api` |
| `GET` | `/modifyInvoiceDate` | `PatientBillingBackendController` | `modifyInvoiceDate` | `web/api` |
| `GET` | `/UPDInvoiceDate` | `PatientBillingBackendController` | `UPDInvoiceDate` | `web/api` |
| `GET` | `/modifyInvoiceReceipt` | `PatientBillingBackendController` | `modifyInvoiceReceipt` | `web/api` |
| `GET` | `/UPDInvoiceReceipt` | `PatientBillingBackendController` | `UPDInvoiceReceipt` | `web/api` |
| *...* | *+236 more routes mapped to INVOICE POSTING* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `PostingMergeClaim` (`app/Services/PostingMergeClaim.php`)
  - Methods: `postMergeClaim()`, `insertMergeClaim()`, `mergeClaimIcdDiagnosis()`, `getAutoPostClaimApp()`, `getLISRISServiceStatus()`
- **Service**: `InvoiceService` (`app/Services/InvoiceService.php`)
  - Methods: `getPatientVisitIds()`, `getHospitalAddress()`, `getPatientBillHeaderDetails()`, `getPaymentsReceivedByInvoice()`, `getInvoiceHeaderDetails()`
- **Service**: `GenerateInvoiceClosedPostedStatus` (`app/Services/GenerateInvoiceClosedPostedStatus.php`)
  - Methods: `getGenInvoiceClosedPostedStatus()`, `insertPatientvisitExcludedPlan()`, `checkseletedItemExcluded()`, `checkInventoryCoverageApplicable()`, `checkPatientPaymentTypes()`
- **Service**: `ClaimInvoiceService` (`app/Services/ClaimInvoiceService.php`)
  - Methods: `ClaimInvoiceDetails()`, `loadInvoiceGridNew()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: LAB INFORMATION SYSTEM (ID: LIS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `LIS`
- **Module Name**: `LAB INFORMATION SYSTEM`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: ALLERGY GROUP, ALLERGY MACHINE TEST CODE, ALLERGY TYPE, ALLERGY TYPE ALLERGY NAME LINK, ALLERGY TYPE PARAMETER, Analyzer, Analyzer Test Mapping, Antibiotic, BULK LIS APPROVAL, Container Type
- **Discovered Sub-functions & Action Page Links** (44 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ALRGYGRP` | ALLERGY GROUP MASTER | `previous_value` | ALLERGY GROUP | ALLERGY GROUP MASTER |
| `ALMNTTCD` | ALLERGY MACHINE TEST CODE | `previous_value` | ALLERGY MACHINE TEST CODE | ALLERGY MACHINE TEST CODE |
| `ALTYPALNK` | ALLERGY TYPE ALLERGY NAME LINK | `previous_value` | ALLERGY TYPE ALLERGY NAME LINK | ALLERGY TYPE ALLERGY NAME LINK |
| `ALRGYTYPE` | ALLERGY TYPE MASTER | `previous_value` | ALLERGY TYPE | ALLERGY TYPE MASTER |
| `ALTYPPARAM` | ALLERGY TYPE PARAMETER | `previous_value` | ALLERGY TYPE PARAMETER | ALLERGY TYPE PARAMETER |
| `ANALZR` | ANALYZER | `getViewAnalyzer` | Analyzer | - |
| `ANALYZR` | ANALYZER AND TESTMAPPING | `viewAnalyzerandTestMapping` | Analyzer Test Mapping | - |
| `ANATOMY` | ANATOMIC PATHOLOGY | `AnatomicPathologyWorkList` | - | - |
| `ANTBIO` | ANITIBIOTIC | `viewAntibiotic` | Antibiotic | - |
| `BCSAMRCV` | Barcode Sample Receive & Acknowledge | `getviewBulkBarcodeScan` | Sample Receive | Barcode Sample Receive & Acknowledge |
| `BULKLISAP` | BULK LIS APPROVAL | `updateBulkLISResult` | BULK LIS APPROVAL | - |
| `CONTYP` | CONTAINERTYPE | `viewContainerType` | Container Type | - |
| `LINKPARAN` | DROP DOWN RESULT LINK PARAMETER | `viewDropDownResultLinkParameter` | Drop Down Result Link Parameter | - |
| `DROPRES` | DROPDOWN RESULT | `viewDropDownResult` | Drop Down Result | - |
| `GROWTH` | GROWTH | `viewGrowth` | Growth | - |
| *...* | *+29 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Lab_` (2 tables), `LIS_` (22 tables), `Microbiology_` (4 tables), `Specimen_` (1 tables)
- **Associated Tables Count**: 102 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`, `Children_MH_Attribute_Values`, `DDWC_Api_Information`, `DSR_All_Attribute_Values`, `Demographic_Attribute_Age_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Patient_Visit_PAC_Assessment_Information_Details` (`app/Models/Patient_Visit_PAC_Assessment_Information_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Assessment_Information_Details` | **Primary Key**: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Assessment_Anaesthesia_Type`], `hasMany(Patient_Visit_PAC_Previous_Anaesthesia_History_Details)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Plan_Of_Care)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Airway_Definition)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Drugs_List)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`]
- **Model**: `RISPatientVisit` (`app/Models/RISPatientVisit.php`)
  - **Database Table**: `RIS_Patient_Visit_Services_Lab` | **Primary Key**: `RIS_Patient_Visit_Services_Lab_Serial_No`
- **Model**: `PatientVisitLISServiceParameterResultLog` (`app/Models/PatientVisitLISServiceParameterResultLog.php`)
  - **Database Table**: `Patient_Visit_LIS_Service_Parameter_Result_Log` | **Primary Key**: `Patient_Visit_LIS_Service_Parameter_Result_Serial_No_Log`
  - **Fillable Attributes**: `Patient_Visit_LIS_Service_Parameter_Result_Serial_No`, `Before_After_Flag`, `Result_Value`, `Result_Value_Type`, `Result_Value_Flag`, `Reporting_Unit_Type_Serial_No`, `Reporting_Unit_Type_Inserted_Value`, `Parameter_Reference_Range_Serial_No`...
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- **Model**: `ServiceLIS` (`app/Models/ServiceLIS.php`)
  - **Database Table**: `Service_Lis` | **Primary Key**: `Service_Lis_Serial_No`
  - **Fillable Attributes**: `Service_USSDB_Serial_No`, `Sub_Department_Code`, `Department_Branch_Serial_No`, `Min_No_Of_Approval_Needed`, `Stop_Processing_Dispatch`, `LIS_LOINC_Code`, `LIS_Service_Comments`, `LIS_Service_Comments_Checked`...
- *(+21 additional Eloquent models associated with LAB INFORMATION SYSTEM)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `LISMicrobiologyChangeController` (`app/Http/Controllers/LISMicrobiologyChangeController.php`)
  - **Action Methods**: `getviewMicrobiologyDetails()`, `getviewMicrobiologyDetailsToShow()`, `deleteMicorbiologyorganismDetails()`
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `PatientRegistrationImportController` (`app/Http/Controllers/PatientRegistrationImportController.php`)
  - **Action Methods**: `uploadPatientRegistration()`, `postPatientExcelUpload()`, `PostPatientRegistrationUpload()`, `insertPatBasicDet()`, `getPaymentAutoCompletePatUpload()`, `updateDefaultPaymentDetails()`, `AddPatientBilling()`, `addRefEntDetails()`
- **Controller**: `specialityDepartmentVisitServiceStatusValuesController` (`app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`)
  - **Action Methods**: `getspecialityDepartmentVisitServiceStatusValues()`, `alreadyExists()`, `getDownloadspecialityDepartmentVisitServiceStatusValues()`
- **Controller**: `GlobalViewOfUniversalCodeGroupsValuesController` (`app/Http/Controllers/GlobalViewOfUniversalCodeGroupsValuesController.php`)
  - **Action Methods**: `ViewGlobalViewOfUniversalCodeGroupsValues()`, `LoadOptionForUniversalCodeGroupsValuesField()`
- **Controller**: `SpecimenTypeController` (`app/Http/Controllers/SpecimenTypeController.php`)
  - **Action Methods**: `getviewSpecimenType()`, `addSpecimenType()`, `branchdetailsvalue()`, `postaddSpecimenType()`, `geteditSpecimenType()`, `posteditSpecimenType()`, `downloadSpecimenType()`, `specimentypestatus()`
- *(+16 more controllers handling LAB INFORMATION SYSTEM)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/universalCodeGroupsValues/{id?}` | `UniversalCodeGroupsValuesController` | `getIndex` | `web/api` |
| `GET` | `/loadUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `loadUniversalCodeGroupValues` | `web/api` |
| `GET` | `/CheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `CheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/EditCheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `EditCheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `getAddUniversalCodeGroupValues` | `web/api` |
| `POST` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `postAddUniversalCodeGroupValues` | `web/api` |
| `GET` | `/changeUniversalCodeGroupValuestatus/{id}/{status}` | `UniversalCodeGroupsValuesController` | `getChangeUniversalCodeGroupValuestatus` | `web/api` |
| `GET` | `/deletUniversalCodeGroupValue/{id}` | `UniversalCodeGroupsValuesController` | `getDeletUniversalCodeGroupValue` | `web/api` |
| `GET` | `/downloadUniversalcodeGroupValues` | `UniversalCodeGroupsValuesController` | `downloadUniversalcodeGroupValues` | `web/api` |
| *...* | *+352 more routes mapped to LAB INFORMATION SYSTEM* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `LISResultEntryVerificationAndResultApprovalValidationService` (`app/Services/LISResultEntryVerificationAndResultApprovalValidationService.php`)
- **Service**: `LaboratorySTDPanel` (`app/Services/EMR/LaboratorySTDPanel.php`)
  - Methods: `LabStdpanelquery()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: LEDGER (ID: LED)

### 1. Module Overview & Navigation Structure
- **Module ID**: `LED`
- **Module Name**: `LEDGER`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Branch Based Business Unit, Department Based License, Department Grouping, GL Masters, General Ledger, Global View of Ledger, Ledger Type, Ledger Type Department
- **Discovered Sub-functions & Action Page Links** (8 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `BRNBUSUNT` | BRANCH BASED BUSINESS UNIT | `branchBasedBusnsUnit` | Branch Based Business Unit | - |
| `DEPTBSDLCS` | DEPARTMENT BASED LICENSE | `departmentBasedLicense` | Department Based License | - |
| `DEPTGRPNG` | DEPARTMENT GROUPING | `departmentGrouping` | Department Grouping | - |
| `GLBVELED` | GLOBAL VIEW OF LEDGER | `viewGlobalLedger` | Global View of Ledger | Post Invoices To GL |
| `LEDGERMOD` | LEDGER | `#` | General Ledger | GL Management |
| `LEDGERMAS` | LEDGER MASTERS | `#` | GL Masters | View & Manage The GL |
| `LEGTYPE` | Ledger Type | `viewLedgerType` | Ledger Type | - |
| `LEGTYPDPT` | Ledger Type Department | `viewLedgerTypeDepartment` | Ledger Type Department | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Ledger_` (4 tables)
- **Associated Tables Count**: 6 tables identified
- **Key Tables**: `Ledger_Posting_Batch`, `Ledger_Posting_Batch_Invoice`, `Ledger_Type`, `Ledger_Type_Department`, `Purchase_Item_Group_General_Ledger_Link`, `Supplier_Ledger_Link`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `StockLedgerTransController` (`app/Http/Controllers/StockLedgerTransController.php`)
  - **Action Methods**: `GetStockLedger()`, `GetStockLedgerView()`, `StockLedgerSearchResult()`, `getStockLocByBranchForReport()`, `getInstallParamByStockLoc()`, `getHeaderInfo()`, `GetItemLevelsByStkLoc_BinLoc()`, `getFLOpenBalQty()`
- **Controller**: `GlobalViewLedgerController` (`app/Http/Controllers/GlobalViewLedgerController.php`)
  - **Action Methods**: `viewGlobalLedger()`, `loadLedgerINSInvoiceDataGrid()`, `loadLedgerInvoiceDataGrid()`, `loadInvoiceGrid()`, `postInvoiceLedgerData()`, `loadLedgerInvoiceAmountGrid()`, `loadLedgerINSInvoiceAmountGrid()`, `getLedgerRequestColumnOrder()`
- **Controller**: `DepartmentGroupingController` (`app/Http/Controllers/DepartmentGroupingController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewDepartmentGrouping()`, `addDeptGrouping()`, `postAddDeptGrouping()`, `getEditDepartmentGrouping()`, `postUpdateDeptGrouping()`, `changeDeptGroupinStatus()`, `downloadDeptGrouping()`
- **Controller**: `LedgerTypeController` (`app/Http/Controllers/LedgerTypeController.php`)
  - **Action Methods**: `addLedgerType()`, `addLedgerTypeDetails()`, `viewLedgerType()`, `editLedgerTypeStaus()`, `deleteLedgerType()`, `editLedgerType()`, `editLedgerTypeDetails()`, `downloadLedgerTypeDetails()`
- **Controller**: `LedgerTypeDepartmentController` (`app/Http/Controllers/LedgerTypeDepartmentController.php`)
  - **Action Methods**: `addLedgerTypeDepartment()`, `addLedgerTypeDepartmentDetails()`, `viewLedgerTypeDepartment()`, `editLedgerTypeDepartmentStaus()`, `deleteLedgerTypeDepartment()`, `editLedgerTypeDepartment()`, `editLedgerTypeDepartmentDetails()`, `downloadLedgerTypeDepartmentDetails()`
- **Controller**: `SupplierLedgerAccController` (`app/Http/Controllers/SupplierLedgerAccController.php`)
  - **Action Methods**: `getViewSupplierLedegerAccount()`, `GetSupplier()`, `getSupplierLedegerAccountAdd()`, `postSupplierLedegerAccountAdd()`, `getSupplierLedegerAccountEdit()`, `postSupplierLedegerAccountEdit()`, `ChangeSuppLedAccStatus()`, `getSupplierLedegerAccountDelete()`
- *(+1 more controllers handling LEDGER)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/StockLedger` | `StockLedgerTransController` | `GetStockLedger` | `web/api` |
| `GET` | `/StockLedgerView/{id?}` | `StockLedgerTransController` | `GetStockLedgerView` | `web/api` |
| `POST` | `/StockLedgerSearch` | `StockLedgerTransController` | `StockLedgerSearchResult` | `web/api` |
| `GET` | `/ViewPurchaseItemLedger/{id?}` | `PurchaseItemGrpLegderLinkController` | `getViewPurchaseItemLedger` | `web/api` |
| `GET` | `/AddPurchaseItemLedger` | `PurchaseItemGrpLegderLinkController` | `getAddPurchaseItemGroupLedgerLink` | `web/api` |
| `POST` | `/AddPurchaseItemLedger` | `PurchaseItemGrpLegderLinkController` | `postAddPurchaseItemGroupLedgerLink` | `web/api` |
| `GET` | `/DownloadPurchaseItemLedger/{id?}` | `PurchaseItemGrpLegderLinkController` | `DownloadPurchaseItemLedger` | `web/api` |
| `GET` | `/DeletePurchaseItemGrpLedger/{sNo?}` | `PurchaseItemGrpLegderLinkController` | `DeletePurchaseItemGrpLedger` | `web/api` |
| `GET` | `/EditPurchaseItemGrpLedger/{id?}` | `PurchaseItemGrpLegderLinkController` | `getEditPurchaseItemGroupLedgerLink` | `web/api` |
| `POST` | `/EditPurchaseItemGrpLedger/{id?}` | `PurchaseItemGrpLegderLinkController` | `postEditPurchaseItemGroupLedgerLink` | `web/api` |
| *...* | *+52 more routes mapped to LEDGER* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: MASTERS (ID: MTR)

### 1. Module Overview & Navigation Structure
- **Module ID**: `MTR`
- **Module Name**: `MASTERS`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Masters
- **Discovered Sub-functions & Action Page Links** (1 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `MSTR` | MASTERS | `dashboard` | Masters | Configure HIMES |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Department_` (4 tables), `Master_` (5 tables), `Service_` (33 tables)
- **Associated Tables Count**: 224 tables identified
- **Key Tables**: `AAA_New_Service_Master`, `AAA_given_item_master_QMC`, `Adm_Cast_Service_11032019`, `Adm_ServiceName`, `Adm_Service_01032019`, `Adm_Service_New_2611`, `All_Master_Logs`, `Appointment_Visit_Questionnaire_Types_Services`, `BodySite_SubSite_SubDepartment_Mapping`, `Branch_Free_Paid_Followup_Services`, `Claim_Mandatory_Observation_Type`, `Common_EMR_Service_Search`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `WebServiceLogDetail` (`app/Models/WebServiceLogDetail.php`)
  - **Database Table**: `Web_Service_Log_Details` | **Primary Key**: `Web_Service_Log_Details_Serial_No`
  - **Fillable Attributes**: `Branch_Code`, `Web_Service_Type`, `Web_Service_Method`, `Web_Service_Content`, `Web_Service_Error`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
  - **Eloquent Relationships**: `hasMany(Branch)` [Key/Pivot: `Branch_Code`]
- **Model**: `ItemMaster` (`app/Models/ItemMaster.php`)
  - **Database Table**: `Item_Master` | **Primary Key**: `Item_Master_Serial_No`
- **Model**: `PApatientVisitServices` (`app/Models/PApatientVisitServices.php`)
  - **Database Table**: `PA_Patient_Visit_Services` | **Primary Key**: `PA_Patient_Visit_Services_Serial_No`
- **Model**: `SupplierMaster` (`app/Models/SupplierMaster.php`)
  - **Database Table**: `Supplier_Master` | **Primary Key**: `Supplier_Master_Serial_No`
- **Model**: `DepartmentBranch` (`app/Models/DepartmentBranch.php`)
  - **Database Table**: `Department_Branch` | **Primary Key**: `Department_Branch_Serial_No`
  - **Eloquent Relationships**: `belongsTo(Branch)` [Key/Pivot: `Branch_Code`], `hasMany(Department)` [Key/Pivot: `Department_Code`]
- **Model**: `DiscountCodeDetailsServices` (`app/Models/DiscountCodeDetailsServices.php`)
  - **Database Table**: `Discount_Code_Details_Services` | **Primary Key**: `Discount_Code_Details_Services_Serial_No`
  - **Fillable Attributes**: `Discount_Code_Details_Serial_No`, `Service_USSDB_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
  - **Eloquent Relationships**: `belongsTo(DiscountCodeDetails)` [Key/Pivot: `Discount_Code_Details_Serial_No`], `belongsTo(ServiceUSSDB)` [Key/Pivot: `Service_USSDB_Serial_No`], `belongsTo(User)` [Key/Pivot: `Created_By_User_Id`], `belongsTo(User)` [Key/Pivot: `Modified_By_User_Id`]
- *(+83 additional Eloquent models associated with MASTERS)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `ServiceTestController` (`app/Http/Controllers/ServiceTestController.php`)
  - **Action Methods**: `getViewServiceTest()`, `addServiceTest()`, `postAddServiceTest()`, `getEditServiceTest()`, `getViewDetailServiceTest()`, `postEditServiceTest()`, `getDeleteServiceTest()`, `isExistServiceDeleteId()`
- **Controller**: `EMRServiceAdditionController` (`app/Http/Controllers/EMRServiceAdditionController.php`)
  - **Action Methods**: `addEMRSearchServicetoVisit()`, `panelWiseDraftStatus()`, `insertPatientVisitServiceAndResource()`, `PostDSSVisitFollowupDetails()`, `loadEMRServiceSingleFilterGrid()`, `getActivityTiming()`, `getResourceServiceBasedSubDept()`, `AddSelectedServiceToQuickVisit()`
- **Controller**: `ServiceOperatingController` (`app/Http/Controllers/ServiceOperatingController.php`)
  - **Action Methods**: `viewUpdateServiceOperatingHour()`, `getServicesDetails()`, `addServiceOperatingHoursdetails()`
- **Controller**: `ServiceDiscountController` (`app/Http/Controllers/ServiceDiscountController.php`)
  - **Action Methods**: `getServiceview()`, `getServiceAdd()`, `postAddServiceDiscount()`, `getEditServiceDiscount()`, `postEditServiceDiscount()`, `getDeleteServiceDiscount()`, `isExistServiceDeleteId()`, `getChangeServiceDiscountStatus()`
- **Controller**: `ServicesFormGroupingElementsController` (`app/Http/Controllers/ServicesFormGroupingElementsController.php`)
  - **Action Methods**: `viewServiceFormGroupingElements()`, `getAddServiceFormGroupingElements()`, `postAddServiceFormGroupingElements()`, `getEditServiceFormGroupingElements()`, `postEditServiceFormGroupingElements()`, `editServiceFormGroupingElementsActiveStatus()`, `editServiceFormGroupingElementsDeactiveStatus()`, `deleteServiceFormGroupingElements()`
- **Controller**: `PlanMasterController` (`app/Http/Controllers/PlanMasterController.php`)
  - **Action Methods**: `getIndex()`, `getPlanMasterData()`, `getPlanMasterFetchGroup()`, `getPlanMasterFetchCompany()`, `getPlanMasterFetchBranch()`, `getPlanMasterInsuranceCompany()`, `getinsuranceType()`, `getplanMasterComtonetwrk()`
- *(+108 more controllers handling MASTERS)*

### 5. Form Requests & Input Validation Rules
- **Form Request**: `StoreEMRCommonMastersTypeRequest` (`app/Http/Requests/StoreEMRCommonMastersTypeRequest.php`)
  - **Validation Rules**:
    - `//         EMR_Common_Type_Description => required|string|max:200`
    - `//         Order_Sequence => required|integer`
    - `//         Branch_Code => required|string|max:20|unique:EMR_Common_Masters_Type,Branch_Code`
    - `//         selectedData.*.EMR_Common_Description => required|string|max:200`
    - `//         selectedData.*.Textbox_Required => required|string|in:Y,N`
    - `//         selectedData.*.Score_Is_Applicable => required|string|in:Y,N`
- **Form Request**: `DoctorAvailabilityRequest` (`app/Http/Requests/Resource/DoctorAvailabilityRequest.php`)
  - **Validation Rules**:
    - `location_id => required|string|exists:Branch,Branch_Code`
    - `api_key => required|string|exists:Branch,WebService_Key`
    - `doctor_id => required|integer|exists:Resource_Parent,Resource_Parent_Serial_No`
    - `start_datetime => required|date_format:Y-m-d H:i|date|after:now`
    - `end_datetime => required|date_format:Y-m-d H:i|after:start_datetime`
    - `speciality_code => required|string|exists:Speciality,Speciality_Code`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/loadUserBasedServices` | `EMRServiceSearchController` | `loadUserBasedServices` | `web/api` |
| `GET` | `/getServiceDescriptionEMRServiceForRIS` | `EMRServicesController` | `getServiceDescriptionEMRServiceForRIS` | `web/api` |
| `GET` | `/addEMRSearchServicetoVisit` | `EMRServiceAdditionController` | `addEMRSearchServicetoVisit` | `web/api` |
| `GET` | `/addEMRSearchPendingServicetoVisit` | `EMRServiceAdditionController` | `addEMRSearchPendingServicetoVisit` | `web/api` |
| `POST` | `/functiondepartmentbarnchcheck` | `FunctionPrivilegeRoleController` | `postCheckFunctiondepartmentbarnchcheck` | `web/api` |
| `POST` | `/editFunctionPrivilegeRole/functiondepartmentbarnchcheck` | `FunctionPrivilegeRoleController` | `postCheckFunctiondepartmentbarnchcheck` | `web/api` |
| `POST` | `/getBranchModuleDetail` | `FunctionPrivilegeRoleSSDBController` | `postCheckFunctiondepartmentbarnchcheck` | `web/api` |
| `POST` | `/editFunctionPrivilegeRoleSSDB/getBranchModuleDetail` | `FunctionPrivilegeRoleSSDBController` | `postCheckFunctiondepartmentbarnchcheck` | `web/api` |
| `POST` | `/hrBranchVehicleStatusChange` | `HRMasterController` | `posthrBranchVehicleStatusChange` | `web/api` |
| `POST` | `/hrDeleteBranchVehicle` | `HRMasterController` | `posthrDeleteBranchVehicle` | `web/api` |
| *...* | *+1718 more routes mapped to MASTERS* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `CommonService` (`app/Services/CommonService.php`)
  - Methods: `getRemittanceStatus()`, `getEncounterEndStatus()`, `getexistEncTypedata()`, `checkAcknowledgmentStatus()`, `checkRISServiceCompletedStatus()`
- **Service**: `ClaimMandatoryObservationTypeService` (`app/Services/ClaimMandatoryObservationTypeService.php`)
  - Methods: `saveClaimMandatoryObservationType()`, `getClaimMandatoryObservationTypedata()`, `changestatus()`, `ClaimMandatoryObservationTypeDownload()`, `getBranchBasedModule()`
- **Service**: `BranchConfigurationService` (`app/Services/BranchConfigurationService.php`)
- **Service**: `MuscleStrengthService` (`app/Services/MuscleStrengthService.php`)
  - Methods: `addMuscleStrength()`, `getMuscleStrengthdata()`, `changestatus()`, `MuscleStrengthDownload()`, `updateMuscleStrength()`
- **Service**: `LISQueryService` (`app/Services/LISQueryService.php`)
  - Methods: `ResultEntryQuery()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: MESSAGING AND TASK (ID: MAT)

### 1. Module Overview & Navigation Structure
- **Module ID**: `MAT`
- **Module Name**: `MESSAGING AND TASK`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: DRY DOCKS WORLD CLINIC
- **Discovered Sub-functions & Action Page Links** (8 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `COMPO` | COMPOSE | `viewEmailMessageComposing/task` | - | COMPOSE |
| `TDRAFTS` | DRAFTS | `viewEmailMessageComposing/task` | - | DRAFTS |
| `MSGANTSK` | MESSAGING AND TASK | `viewEmailMessageComposing` | DRY DOCKS WORLD CLINIC | - |
| `SENTMAIL` | SENT MAIL | `viewEmailMessageComposing/task` | - | SENT MAIL |
| `TASKASSIGN` | Task Assigned | `taskAssignViewEmailMessageComposing` | - | - |
| `TGROUP` | Task GROUP | `viewEmailMessageComposing/task` | - | Task GROUP |
| `INBOX` | TASK INBOX | `viewEmailMessageComposing/task` | - | TASK INBOX |
| `TASKRECEI` | Task Received | `taskReceiveViewEmailMessageComposing` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Inbox_` (1 tables), `Task_` (1 tables)
- **Associated Tables Count**: 8 tables identified
- **Key Tables**: `All_Tasks`, `DSR_Action_Schedule_Followup_Tasks`, `Email_Message_Task_Number_Counter`, `IPD_Nursing_Task`, `Inbox_Sent_User_Folders`, `Patient_Visit_Scheduling_Task_Details`, `Task_Type`, `Visit_DSR_Action_Followup_Tasks_Scheduled`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `MessageTaskInboxController` (`app/Http/Controllers/MessageTaskInboxController.php`)
  - **Action Methods**: `getViewInboxMail()`, `fetchInboxContent()`, `deleteSelectedMessage()`, `newdeleteSelectedMessage()`, `newdeletesingleInboxItemMultiMessage()`, `deleteSingleSelectedMessage()`, `newdeleteSingleSelectedMessage()`, `showToReadSelectedMessage()`
- **Controller**: `EmailTaskController` (`app/Http/Controllers/EmailTaskController.php`)
  - **Action Methods**: `viewemailcomposingmail()`, `viewsamplepageforemil()`, `viewTaskReceived()`, `newviewTaskReceived()`, `viewtaskassigned()`, `viewNewTaskReceived()`, `newviewNewTaskReceived()`, `viewnewtaskassigned()`
- **Controller**: `EmailTaskComposeController` (`app/Http/Controllers/EmailTaskComposeController.php`)
  - **Action Methods**: `getUseridForGroupUsers()`, `getUseridForToemail()`, `getUseridForCcemail()`, `deleteEmailMessageGroup()`, `deleteEmailMessageGroupUsers()`, `editEmailMessageGroupUsers()`, `getNewMessageTaskNotification()`, `setMessageDetailsinSession()`
- **Controller**: `emailTaskAssignedController` (`app/Http/Controllers/emailTaskAssignedController.php`)
  - **Action Methods**: `viewTaskAssigned()`, `showTaskAssignedRecord()`, `newshowTaskAssignedRecord()`, `deleteTaskAssingedRecord()`, `getDeletenewTaskAssignedMessages()`, `newdeletesingleAssignedMsg()`, `goToDeleteIndv()`, `newgoToDeleteIndv()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/getNewMessageTaskNoti` | `EmailTaskComposeController` | `getNewMessageTaskNotification` | `web/api` |
| `GET` | `/getViewnewInboxMail` | `MessageTaskInboxController` | `getViewnewInboxMail` | `web/api` |
| `GET` | `/newdeleteTaskAssingedRecord` | `emailTaskAssignedController` | `newdeleteTaskAssingedRecord` | `web/api` |
| `POST` | `/newTaskAssignInsertMessages` | `emailTaskAssignedController` | `newTaskAssignInsertMessages` | `web/api` |
| `GET` | `/viewNewTaskAssignedMessages` | `emailTaskAssignedController` | `viewNewTaskAssignedMessages` | `web/api` |
| `GET` | `/newshowTaskAssignedRecord` | `emailTaskAssignedController` | `newshowTaskAssignedRecord` | `web/api` |
| `GET` | `/newgoToDeleteIndv` | `emailTaskAssignedController` | `newgoToDeleteIndv` | `web/api` |
| `GET` | `/NewcancelTheTask` | `emailTaskAssignedController` | `NewcancelTheTask` | `web/api` |
| `GET` | `/getDeletenewTaskAssignedMessages` | `emailTaskAssignedController` | `getDeletenewTaskAssignedMessages` | `web/api` |
| `GET` | `/getallTaskResource` | `emailTaskAssignedController` | `getallTaskResource` | `web/api` |
| *...* | *+110 more routes mapped to MESSAGING AND TASK* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: PACKAGE (ID: PAC)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PAC`
- **Module Name**: `PACKAGE`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Package Masters, Package-Branch, Package-Discount-Type, Package-Rate-For-Insurance, Package-Rate-For-Non-Insurance, Package-Service, Package-Tax, Package-Tax-Type, Packages
- **Discovered Sub-functions & Action Page Links** (12 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `PAKCOVER` | INSURANCE PLAN PACKAGE COVER | `insurancePlanPackageCover` | - | - |
| `PACK` | PACKAGE | `package` | Packages | - |
| `PACKBRAN` | PACKAGE BRANCH | `packageBranch` | Package-Branch | - |
| `PACKDISTYP` | PACKAGE DISCOUNT TYPE | `packageDiscountType` | Package-Discount-Type | - |
| `PACKMSTR` | PACKAGE MASTERS | `#` | Package Masters | - |
| `PACKMOD` | PACKAGE MODULE | `#` | - | - |
| `PACKINS` | PACKAGE RATE FOR INSURANCE | `packageRateforInsurance` | Package-Rate-For-Insurance | - |
| `PACKNONINS` | PACKAGE RATE FOR NON INSURANCE | `packageRateforNonInsurance` | Package-Rate-For-Non-Insurance | - |
| `PACKSER` | PACKAGE SERVICE | `packageService` | Package-Service | - |
| `PAKTAX` | PACKAGE TAX | `packageTax` | Package-Tax | - |
| `PAKTAXTY` | PACKAGE TAX TYPE | `packageTaxType` | Package-Tax-Type | - |
| `REGPACK` | Registration Package | `#` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Package_` (17 tables)
- **Associated Tables Count**: 40 tables identified
- **Key Tables**: `IPD_Package_Branch_Rates_Category_Details`, `IPD_Package_Category`, `IPD_Package_Category_Service_Item_Details`, `IPD_Visit_Package_Branch_Category_Details`, `IPD_Visit_Package_Branch_Components_Details`, `IPD_Visit_Package_Branch_Details`, `Insurance_Plan_Package_Cover`, `Package`, `Package_Branch`, `Package_Branch_Encounter_Type`, `Package_Branch_Rates`, `Package_Component_Rates`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Patient_Visit_PAC_Assessment_Information_Details` (`app/Models/Patient_Visit_PAC_Assessment_Information_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Assessment_Information_Details` | **Primary Key**: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Assessment_Anaesthesia_Type`], `hasMany(Patient_Visit_PAC_Previous_Anaesthesia_History_Details)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Plan_Of_Care)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Airway_Definition)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Drugs_List)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`]
- **Model**: `Patient_Visit_PAC_Plan_Of_Care` (`app/Models/Patient_Visit_PAC_Plan_Of_Care.php`)
  - **Database Table**: `Patient_Visit_PAC_Plan_Of_Care` | **Primary Key**: `Patient_Visit_PAC_Plan_Of_Care_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRCommonMasters)` [Key/Pivot: `Plan_Of_Care_EMR_Common_Masters_Serial_No`]
- **Model**: `Patient_Visit_PAC_Airway_Definition` (`app/Models/Patient_Visit_PAC_Airway_Definition.php`)
  - **Database Table**: `Patient_Visit_PAC_Airway_Definition` | **Primary Key**: `Patient_Visit_PAC_Airway_Definition_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRCommonMasters)` [Key/Pivot: `Airway_Definition_EMR_Common_Masters_Serial_No`]
- **Model**: `Patient_Visit_PAC_Drugs_List` (`app/Models/Patient_Visit_PAC_Drugs_List.php`)
  - **Database Table**: `Patient_Visit_PAC_Drugs_List` | **Primary Key**: `Patient_Visit_PAC_Drugs_List_Serial_No`
  - **Eloquent Relationships**: `belongsTo(Drug)` [Key/Pivot: `Drug_Serial_No`]
- **Model**: `PatientPackagedAvail` (`app/Models/Package/PatientPackagedAvail.php`)
  - **Database Table**: `Patient_Packaged_Avail` | **Primary Key**: `Patient_Packaged_Avail_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Basic_Details_Serial_No`, `Package_Components_Rates_Serial_No`, `Package_Branch_Serial_No`, `Patient_Payment_Type_Serial_No`, `Component_Type`, `Item_Drug_Link_Serial_No`, `Item_Master_Serial_No`...
- *(+5 additional Eloquent models associated with PACKAGE)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PackageController` (`app/Http/Controllers/PackageController.php`)
  - **Action Methods**: `getPackageview()`, `getPackageadd()`, `postPackageadd()`, `getchangePackageStatus()`, `getPackageUpdate()`, `postPackageUpdate()`, `getPackageDelete()`, `getPackageNameExists()`
- **Controller**: `RegistrationPackageController` (`app/Http/Controllers/RegistrationPackageController.php`)
  - **Action Methods**: `getRegistrationPackageService()`, `getResourcePackageServiceAdd()`, `InsresourcePackageServ()`, `getServiceBySUSSDB()`, `addResourceForPackageService()`
- **Controller**: `PackageInvoiceController` (`app/Http/Controllers/PackageInvoiceController.php`)
  - **Action Methods**: `printPackageInvoicePdf()`
- **Controller**: `PackageServiceDetailsController` (`app/Http/Controllers/PackageServiceDetailsController.php`)
  - **Action Methods**: `getallPackagesService()`, `getPackDetStatus()`, `getpackageserviceDetails()`, `getPackageComponents()`, `getAllPackageMaster()`, `getAllPackageBasedService()`, `getFetchPackageBasedService()`, `getServiceDetailsAdd()`
- **Controller**: `PackageDiscountTypeController` (`app/Http/Controllers/PackageDiscountTypeController.php`)
  - **Action Methods**: `getPackageDiscountTypeview()`, `getPackageDiscountTypeadd()`, `postPackageDiscountTypeadd()`, `alreadyExists()`, `getchangePackageDiscountTypeStatus()`, `getPackageDiscountTypeUpdate()`, `postPackageDiscountTypeUpdate()`, `getPackageDiscountTypeDelete()`
- **Controller**: `IPDPackageDetailsController` (`app/Http/Controllers/IPDPackageDetailsController.php`)
  - **Action Methods**: `getViewIPDPackage()`, `getaddIPDPackage()`, `getIPDPackageEncounter()`, `alreadyIPDPackageExists()`, `postAddIPDPackage()`, `getEditIPDPackage()`, `getSamePackageIds()`, `getSameEncounterIds()`
- *(+18 more controllers handling PACKAGE)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/insurancePlanPackageCover/{id?}` | `InsurancePlanPackageCoverController` | `getIndex` | `web/api` |
| `GET` | `/insurancePlanPackageCoverAdd` | `InsurancePlanPackageCoverController` | `getAddInsurancePackage` | `web/api` |
| `POST` | `/insurancePlanPackageCoverAdded` | `InsurancePlanPackageCoverController` | `postAddedInsurancePackage` | `web/api` |
| `GET` | `/changeInsurancePlanPackagestatus/{id}/{status}` | `InsurancePlanPackageCoverController` | `getInsurancePlanPackagestatus` | `web/api` |
| `GET` | `/editInsurancePlanPackageCover/{id}` | `InsurancePlanPackageCoverController` | `getEditInsurancePlanPackage` | `web/api` |
| `POST` | `/editedInsurancePlanPackageCover` | `InsurancePlanPackageCoverController` | `postEditInsurancePlanPackage` | `web/api` |
| `GET` | `/deleteInsurancePlanPackageCover/{id}` | `InsurancePlanPackageCoverController` | `getDeleteInsurancePlanPackage` | `web/api` |
| `GET` | `/viewInsurancePlanPackageCover/{id}` | `InsurancePlanPackageCoverController` | `getListInsurancePlanPackage` | `web/api` |
| `GET` | `/downloadInsurancePlansPackageCover` | `InsurancePlanPackageCoverController` | `downloadInsurancePlansPackageCover` | `web/api` |
| `GET` | `/package/{id?}` | `PackageController` | `getPackageview` | `web/api` |
| *...* | *+295 more routes mapped to PACKAGE* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `PackageMultiBranchUtilization` (`app/Services/PackageMultiBranchUtilization.php`)
  - Methods: `getUtilizePackageAllBranch()`, `InsertPatientPackageAvailDetails()`, `RevertUtilizedCompServ()`, `UpdatePatientPackageAvailDetails()`, `getSingleVisitPackage()`
- **Service**: `PatientVisitPackageComponentsService` (`app/Services/PatientVisitPackageComponentsService.php`)
  - Methods: `updtSnglVst()`, `postPatientVstServRes()`
- **Service**: `PackageService` (`app/Services/PackageService.php`)
  - Methods: `PackageServicedata()`, `deletePackageService()`, `getIsSinglePackage()`, `getPackageDynamicStatus()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: PATIENT TEST (ID: PAT)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PAT`
- **Module Name**: `PATIENT TEST`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Patient Test
- **Discovered Sub-functions & Action Page Links** (1 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `PATIENTEST` | PATIENT TEST | `previous_value` | Patient Test | for testing only created |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Patient_` (622 tables), `patient_` (2 tables), `Test_` (9 tables)
- **Associated Tables Count**: 776 tables identified
- **Key Tables**: `Adm_AVP_PatientDB`, `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Machine_Test_Code`, `Allergy_Values`, `Analyzer_Test_Mapping`, `Analyzer_Test_Mapping_Parameter`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `Allergy_Machine_Test_Code`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Allergy_Machine_Test_Code_Serial_No` | `bigint` | - | NO | - |
| `Allergy_Machine_Test_Code` | `varchar` | 50 | NO | - |
| `EMR_Allergies_Serial_No` | `bigint` | - | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

### 3. Eloquent Models & Data Architecture
- **Model**: `RIS_Screening_Lock_Patient` (`app/Models/RIS_Screening_Lock_Patient.php`)
  - **Database Table**: `RIS_Screening_Lock_Patient` | **Primary Key**: `RIS_Screening_Lock_Patient_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No `, `Locked_Start_Date_Time`, `Locked_End_Date_Time`, `Locked_By_User_ID`, `Locked_By_Date_Time`, `Order_Sequence`, `Active_Status`...
- **Model**: `Patient_Visit_Anesthesia_Medications_Detailed_Result` (`app/Models/Patient_Visit_Anesthesia_Medications_Detailed_Result.php`)
  - **Database Table**: `Patient_Visit_Anesthesia_Medications_Detailed_Result` | **Primary Key**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Serial_No`
  - **Eloquent Relationships**: `belongsTo(Patient_Visit_Anesthesia_Medications_Result_Items)`
- **Model**: `SecondaryCardDetails` (`app/Models/SecondaryCardDetails.php`)
  - **Database Table**: `Patient_Visit_Secondary_Insurance_Card_Details` | **Primary Key**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Insurance_Card_Details_Serial_No`, `Patient_Visit_Insurance_Remarks`, `Show_Remarks_Alert_In_Billing`, `Remarks_Read_In_Billing`, `Insurance_Plan_Serial_No`, `Insurance_Company_Serial_No`...
- **Model**: `PatientVisitDrugScheduleIVAdministrationLog` (`app/Models/PatientVisitDrugScheduleIVAdministrationLog.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_IV_Administration_Log` | **Primary Key**: `Patient_Visit_Drug_Schedule_IV_Administration_Log_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`, `IV_Start_Resume_Time`, `IV_End_Pause_Time`, `Rate`, `Type`, `Started_By_User_Id`, `Paused_By_User_Id`, `Resume_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(PatientVisitDrugScheduleIVAdminstration)` [Key/Pivot: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`]
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Patient_Visit_Physician_Assessment_Form` (`app/Models/Patient_Visit_Physician_Assessment_Form.php`)
  - **Database Table**: `Patient_Visit_Physician_Assessment_Form` | **Primary Key**: `Patient_Visit_Physician_Assessment_Form_Serial_No`
  - **Constants / Status Flags**: `SAVE_COMPLETE_OPTION_NO = "N"`, `SAVE_COMPLETE_OPTION_COMPLETED = "C"`
- *(+201 additional Eloquent models associated with PATIENT TEST)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PatientBillingBackendController` (`app/Http/Controllers/PatientBillingBackendController.php`)
  - **Action Methods**: `modifyInvoiceDate()`, `UPDInvoiceDate()`, `modifyInvoiceReceipt()`, `UPDInvoiceReceipt()`, `UPDInvoiceReceiptAmt()`, `getInvoiceVisitRegisteredDateTime()`
- **Controller**: `PatientAssitanceTypesController` (`app/Http/Controllers/PatientAssitanceTypesController.php`)
  - **Action Methods**: `getViewPatientAssitanceTypes()`, `getAddPatientAssitanceTypes()`, `alreadyExists()`, `postAddPatientAssitanceTypes()`, `getPatientAssitanceTypesstatus()`, `getEditPatientAssitanceTypes()`, `postEditPatientAssitanceTypes()`, `getDeletePatientAssitanceTypes()`
- **Controller**: `UserTestResultReportingConroller` (`app/Http/Controllers/UserTestResultReportingConroller.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getviewusertestresultreprting()`, `getaddusertestresultreprting()`
- **Controller**: `ServiceTestController` (`app/Http/Controllers/ServiceTestController.php`)
  - **Action Methods**: `getViewServiceTest()`, `addServiceTest()`, `postAddServiceTest()`, `getEditServiceTest()`, `getViewDetailServiceTest()`, `postEditServiceTest()`, `getDeleteServiceTest()`, `isExistServiceDeleteId()`
- **Controller**: `PatientdbfieldsController` (`app/Http/Controllers/PatientdbfieldsController.php`)
  - **Action Methods**: `getviewpatientdbfields()`, `getaddpatientdbfields()`, `postaddpatientdbfields()`, `changepatientdbfieldstatus()`, `getdeletepatientdbfields()`, `geteditpatientdbfields()`, `posteditpatientdbfields()`, `downloadPatientdbfields()`
- **Controller**: `UserTestResultReportingController` (`app/Http/Controllers/UserTestResultReportingController.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getViewUserTestResultReportingprivilages()`, `getAddUserTestResultReporting()`, `getservicevalues()`, `gettemplatedetails()`
- *(+93 more controllers handling PATIENT TEST)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/removePatientRelatedSessionInfo` | `ConnectionsController` | `removePatientRelatedSessionInfo` | `web/api` |
| `GET` | `/testReport` | `TestReportController` | `gettestReportDetails` | `web/api` |
| `GET` | `/Reportpdfgeneration` | `TestReportController` | `getreportpdfgeneration` | `web/api` |
| `GET` | `/generatePDFreport` | `TestReportController` | `viewgeneratipdf` | `web/api` |
| `GET` | `/reportpdfgenetationtest` | `TestReportController` | `postreportpdfgeneration` | `web/api` |
| `GET` | `/changeRegionStateStatus/{code}/{status}` | `RegionStateController` | `getRegionStateStatusToChange` | `web/api` |
| `GET` | `/changeMarketRegionStateStatus/{code}/{status}` | `MarketRegionStateController` | `getMarketRegionStateStatusToChange` | `web/api` |
| `GET` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `getEditOnlinePatient` | `web/api` |
| `POST` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `postEditOnlinePatient` | `web/api` |
| `GET` | `/testmenu` | `MenuController` | `testGetAllMenu` | `web/api` |
| *...* | *+1447 more routes mapped to PATIENT TEST* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `EMRPatientHealthQuestionnaireService` (`app/Services/EMRPatientHealthQuestionnaireService.php`)
  - Methods: `viewEMRPatientHealthQuestionnaireDetails()`, `getEMRCommonMasterDetails()`, `currentVisitData()`, `getPatVisiEMHumptDumptySno()`, `GenAnxDisdrFallPrvntnDatas()`
- **Service**: `PatientVisitDischargeSummaryDetailService` (`app/Services/PatientVisitDischargeSummaryDetailService.php`)
  - Methods: `checkAndGetVisitDischargeSummary()`, `insertOrUpdateVisitDischargeSummary()`, `getPatientVisitDischargeSummary()`, `createUpdateBranchBaseDischarge()`, `StrQuoteReplace()`
- **Service**: `PatientVisitResourceService` (`app/Services/PatientVisitResourceService.php`)
  - Methods: `getPatientVisitResourceNameAndID()`, `getPAPatientVisitResourceUserId()`
- **Service**: `PatientVisitBasicDetailsService` (`app/Services/PatientVisitBasicDetailsService.php`)
  - Methods: `updateEMRStatustoInProgress()`, `updateEMReditedService()`, `getvisitType()`, `getLastVisitInsuranceOrTpaPaymentType()`, `getEncounterTypeByVisitId()`
- **Service**: `PatientBillingServices` (`app/Services/PatientBillingServices.php`)
  - Methods: `validateInventoryItemAgainstPatient()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: Pharmacy (ID: PH)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PH`
- **Module Name**: `Pharmacy`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Global View Of Pharmacy Credit Note, Global View Of Pharmacy Outstanding Invoice, IP Pharmacy Check List, PHARMACY CREDIT NOTE, Pharmacy Deposit, Pharmacy Orders, Pharmacy Pre-Approvals, Pharmacy Refund, Refunded Transactions, Sales Register
- **Discovered Sub-functions & Action Page Links** (16 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `PHCREDNOTE` | ADD PHARMACY CREDIT NOTE | `AddPHCreditNote` | PHARMACY CREDIT NOTE | - |
| `GVATFACLTY` | GIVE AT FACILITY MEDICINE | `previous_value` | - | - |
| `GVOPPHAR` | Global View of OP Pharmacy | `viewGlobalOPPharmacy` | Pharmacy Orders | IP & OP Pharmacy Orders |
| `PHCREDGV` | Global View Of Pharmacy Credit Note | `viewGlobalPHCreditNote` | Global View Of Pharmacy Credit Note | - |
| `GVOPHOUINV` | Global View Of Pharmacy Outstanding Invoice | `viewGlobalOutstandBillPharmarcy` | Global View Of Pharmacy Outstanding Invoice | - |
| `IPPHARCHLI` | IP Pharmacy Check List | `previous_value` | IP Pharmacy Check List | IP Pharmacy Check List |
| `PHARREFUND` | PHARMACY INVOICE REFUND DETAILS | `PharmacyInvoiceRefundDetails` | Refunded Transactions | List of Refunded Invoices |
| `PHYPVDEP` | PHARMACY PATIENT VISIT DEPOSITS | `PharmacybillingDeposit` | Pharmacy Deposit | Advance Payment |
| `PHYPVREFUD` | PHARMACY PATIENT VISIT REFUND | `Pharmacyrefundbilling` | Pharmacy Refund | Payment Refunds |
| `PHPAYTYPE` | Pharmacy Payment Type change | `#` | - | - |
| `PHARMPRIOR` | PHARMACY PRIOR AUTHORIZATION GLOBAL VIEW | `globalViewPharmacyPriorVisit` | Pharmacy Pre-Approvals | PHARMACY PRIOR AUTHORIZATION GLOBAL VIEW |
| `PHARMREG` | PHARMACY REGISTRATION | `pharmacyRegistration` | Sales Register | OP/OTC Pharmacy Sales |
| `PHASPR` | Pharmacy Short Payment Reason | `-` | - | - |
| `PHARSTATUS` | PHARMACY STATUS | `previous_value` | - | - |
| `ITEMTAXPRI` | Stock item tax select | `#` | - | - |
| *...* | *+1 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Drug_` (18 tables), `Drugs_` (1 tables), `Pharmacist_` (1 tables), `Pharmacy_` (34 tables), `RXNow_` (1 tables)
- **Associated Tables Count**: 204 tables identified
- **Key Tables**: `AAA_Item_Drug_map`, `AAA_given_Pharmacy_Stock_template`, `API_Order_Details_For_Pharmacy`, `Adm_Drug_18032019`, `Adm_Drug_21032019`, `Adm_Drug_Covered`, `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Branch_Wise_Drug_Pharmacy`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `PatientVisitDrugScheduleIVAdministrationLog` (`app/Models/PatientVisitDrugScheduleIVAdministrationLog.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_IV_Administration_Log` | **Primary Key**: `Patient_Visit_Drug_Schedule_IV_Administration_Log_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`, `IV_Start_Resume_Time`, `IV_End_Pause_Time`, `Rate`, `Type`, `Started_By_User_Id`, `Paused_By_User_Id`, `Resume_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(PatientVisitDrugScheduleIVAdminstration)` [Key/Pivot: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`]
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `PatientVisitDrugScheduleInventoryIVAdminstration` (`app/Models/PatientVisitDrugScheduleInventoryIVAdminstration.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_Inventory_IV_Administration` | **Primary Key**: `Patient_Visit_Drug_Schedule_Inventory_IV_Adminstration_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drugs_Scheduled_Inventory_Serial_No`, `IV_Start_Time`, `IV_End_Time`, `IV_Remarks`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`...
  - **Eloquent Relationships**: `hasMany(PatientVisitDrugScheduleInventoryIVAdminstrationLog)` [Key/Pivot: `Patient_Visit_Drug_Schedule_Inventory_IV_Adminstration_Serial_No`]
- **Model**: `Patient_Visit_Psychiatric_Assessment_Drugs_List` (`app/Models/Patient_Visit_Psychiatric_Assessment_Drugs_List.php`)
  - **Database Table**: `Patient_Visit_Psychiatric_Assessment_Drugs_List` | **Primary Key**: `Patient_Visit_Psychiatric_Assessment_Drugs_List_Serial_No`
  - **Eloquent Relationships**: `belongsTo(Drug)` [Key/Pivot: `Drug_Serial_No`]
- **Model**: `Patient_Visit_Clinical_Pharmacist_Intervention` (`app/Models/Patient_Visit_Clinical_Pharmacist_Intervention.php`)
  - **Database Table**: `Patient_Visit_Clinical_Pharmacist_Intervention` | **Primary Key**: `Patient_Visit_Clinical_Pharmacist_Intervention_Serial_No`
  - **Eloquent Relationships**: `hasMany(Patient_Visit_Clinical_Pharmacist_Intervention_DRP_Clinical)` [Key/Pivot: `Patient_Visit_Clinical_Pharmacist_Intervention_Serial_No`]
- **Model**: `ItemDrugLink` (`app/Models/ItemDrugLink.php`)
  - **Database Table**: `Item_Drug_Link` | **Primary Key**: `Item_Drug_Link_Serial_No`
- *(+24 additional Eloquent models associated with Pharmacy)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `DrugApprovalController` (`app/Http/Controllers/DrugApprovalController.php`)
  - **Action Methods**: `viewDrugApproval()`, `getAddDrugApproval()`, `postAddDrugApproval()`, `getDrugApprovalStatusChange()`, `getEditDrugApproval()`, `postEditDrugApproval()`, `downloadDrugApproval()`, `getDeleteDrugApproval()`
- **Controller**: `EMRDrugController` (`app/Http/Controllers/mmmm.php`)
  - **Action Methods**: `getvisitEMR()`, `viewEMRDiagnosis()`, `getFavouriteDrugsearch()`, `getFavouriteDrugfullsearch()`
- **Controller**: `specialityDepartmentVisitServiceStatusValuesController` (`app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`)
  - **Action Methods**: `getspecialityDepartmentVisitServiceStatusValues()`, `alreadyExists()`, `getDownloadspecialityDepartmentVisitServiceStatusValues()`
- **Controller**: `InsurancePlanDrugController` (`app/Http/Controllers/InsurancePlanDrugController.php`)
  - **Action Methods**: `getInsurancePlanDrugDetails()`, `getaddDrug()`, `getDrugDetails()`, `postaddDrug()`, `getDrug()`, `getEditDrugDetails()`, `getEditDrug()`, `postEditDrug()`
- **Controller**: `ManualApprovalPharmacyAPIController` (`app/Http/Controllers/ManualApprovalPharmacyAPIController.php`)
  - **Action Methods**: `ManualApprovalPharmacyOrder()`, `UpdateManualApprovalPhInsCoverDetails()`
- *(+42 more controllers handling Pharmacy)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/insurancePlanDrugDetails/{id?}` | `InsurancePlanDrugController` | `getInsurancePlanDrugDetails` | `web/api` |
| `GET` | `/addInsurancePlanDrug` | `InsurancePlanDrugController` | `getaddDrug` | `web/api` |
| `GET` | `/getDrugDetails` | `InsurancePlanDrugController` | `getDrugDetails` | `web/api` |
| `POST` | `/addInsurancePlanDrug` | `InsurancePlanDrugController` | `postaddDrug` | `web/api` |
| `GET` | `/getDrugByChecked` | `InsurancePlanDrugController` | `getDrug` | `web/api` |
| `GET` | `/editInsurancePlanDrug/{comSno}/{id?}` | `InsurancePlanDrugController` | `getEditDrug` | `web/api` |
| `POST` | `/postEditInsurancePlanDrug/{comSno}/{id?}` | `InsurancePlanDrugController` | `postEditDrug` | `web/api` |
| `GET` | `/getInsurancePlanDrugStatus/{comSno}/{id?}` | `InsurancePlanDrugController` | `getDrugStatus` | `web/api` |
| `POST` | `/importPlanDrugCode` | `InsurancePlanDrugController` | `importPlanDrugCode` | `web/api` |
| `GET` | `/getInsurancePlan` | `InsurancePlanDrugController` | `getInsurancePlan` | `web/api` |
| *...* | *+719 more routes mapped to Pharmacy* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `DrugTrackingNotification` (`app/Services/DrugTrackingNotification.php`)
  - Methods: `RSDAPIdetails()`, `service_response()`, `xmlRequest()`, `xml_header()`, `xml_footer()`
- **Service**: `PharmacyEclaimValidationService` (`app/Services/PharmacyEclaimValidationService.php`)
  - Methods: `checkQuantityFullyReturned()`
- **Service**: `IPPharmacyService` (`app/Services/IPPharmacyService.php`)
  - Methods: `checkPatientEMRAllergies()`, `getEPrescribePatientAllergies()`, `postPatientAllergiesReview()`
- **Service**: `GlobalViewofIPPharmacyService` (`app/Services/GlobalViewofIPPharmacyService.php`)
- **Service**: `DrugCodeExcelUploadService` (`app/Services/DrugCodeExcelUploadService.php`)
  - Methods: `handleUpload()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: PRIOR VISIT MODULE (ID: PVM)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PVM`
- **Module Name**: `PRIOR VISIT MODULE`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Global View of Prior Visit, Prior Visit, Prior Visit Access
- **Discovered Sub-functions & Action Page Links** (4 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `GVPAPV` | Global View of Prior Visit | `globalViewForPriorVisitNew` | Global View of Prior Visit | - |
| `PRIORVISIT` | Prior Visit | `#` | Prior Visit | - |
| `PRVISACC` | Prior Visit Access | `viewPriorVisit` | Prior Visit Access | - |
| `DOCDETPVM` | Prior Visit Patient Document Details | `previous_value` | - | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Prior_` (2 tables), `Visit_` (14 tables)
- **Associated Tables Count**: 652 tables identified
- **Key Tables**: `AAA_Given_Visit_Encounter`, `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Appointment_Visit_Questionnaire`, `Appointment_Visit_Questionnaire_Possible_Answers`, `Appointment_Visit_Questionnaire_Types`, `Appointment_Visit_Questionnaire_Types_Services`, `Branch_Wise_Visit_Generation`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `PriorStatus` (`app/Models/PriorStatus.php`)
  - **Database Table**: `Prior_Status` | **Primary Key**: `id`
- **Model**: `Patient_Visit_Anesthesia_Medications_Detailed_Result` (`app/Models/Patient_Visit_Anesthesia_Medications_Detailed_Result.php`)
  - **Database Table**: `Patient_Visit_Anesthesia_Medications_Detailed_Result` | **Primary Key**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Serial_No`
  - **Eloquent Relationships**: `belongsTo(Patient_Visit_Anesthesia_Medications_Result_Items)`
- **Model**: `SecondaryCardDetails` (`app/Models/SecondaryCardDetails.php`)
  - **Database Table**: `Patient_Visit_Secondary_Insurance_Card_Details` | **Primary Key**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Insurance_Card_Details_Serial_No`, `Patient_Visit_Insurance_Remarks`, `Show_Remarks_Alert_In_Billing`, `Remarks_Read_In_Billing`, `Insurance_Plan_Serial_No`, `Insurance_Company_Serial_No`...
- **Model**: `PatientVisitDrugScheduleIVAdministrationLog` (`app/Models/PatientVisitDrugScheduleIVAdministrationLog.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_IV_Administration_Log` | **Primary Key**: `Patient_Visit_Drug_Schedule_IV_Administration_Log_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`, `IV_Start_Resume_Time`, `IV_End_Pause_Time`, `Rate`, `Type`, `Started_By_User_Id`, `Paused_By_User_Id`, `Resume_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(PatientVisitDrugScheduleIVAdminstration)` [Key/Pivot: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`]
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Patient_Visit_Physician_Assessment_Form` (`app/Models/Patient_Visit_Physician_Assessment_Form.php`)
  - **Database Table**: `Patient_Visit_Physician_Assessment_Form` | **Primary Key**: `Patient_Visit_Physician_Assessment_Form_Serial_No`
  - **Constants / Status Flags**: `SAVE_COMPLETE_OPTION_NO = "N"`, `SAVE_COMPLETE_OPTION_COMPLETED = "C"`
- *(+183 additional Eloquent models associated with PRIOR VISIT MODULE)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `EMRVisitEntryController` (`app/Http/Controllers/EMRVisitEntryController.php`)
  - **Action Methods**: `reopenEmrBasedOnGraceTime()`, `getGraceTime()`, `getFinalzedReopenlog()`, `visitConfidentialLock()`, `getCurrentLockStatus()`, `confidentialLockRevision()`
- **Controller**: `VisitEncounterLinkController` (`app/Http/Controllers/VisitEncounterLinkController.php`)
  - **Action Methods**: `index()`, `create()`, `store()`, `edit()`, `update()`, `show()`, `ChangeStatus()`, `Download()`
- **Controller**: `InsurancePlanPriorApprovalController` (`app/Http/Controllers/InsurancePlanPriorApprovalController.php`)
  - **Action Methods**: `getAddInsurancePlanPriorApproval()`, `postAddInsurancePlanPriorApproval()`, `getViewInsurancePlanPriorApproval()`, `getEditStatusInsurancePlanPriorApproval()`, `getDeleteInsurancePlanPriorApproval()`, `getDownloadInsurancePlanPriorApproval()`, `getEditInsurancePlanPriorApproval()`, `postEditInsurancePlanPriorApproval()`
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `PatientVisitServiceTestController` (`app/Http/Controllers/PatientVisitServiceTestController.php`)
  - **Action Methods**: `getviewpatientvisitservices()`, `viewpatientvisitservice()`, `getPatientSearch()`, `formPatientSearchList()`, `getPatientnameSearch()`, `getPatientvisitservicedetils()`, `viewPatientHeader()`, `getservicetemplateselectdetils()`
- **Controller**: `specialityDepartmentVisitServiceStatusValuesController` (`app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`)
  - **Action Methods**: `getspecialityDepartmentVisitServiceStatusValues()`, `alreadyExists()`, `getDownloadspecialityDepartmentVisitServiceStatusValues()`
- *(+52 more controllers handling PRIOR VISIT MODULE)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/addEMRSearchServicetoVisit` | `EMRServiceAdditionController` | `addEMRSearchServicetoVisit` | `web/api` |
| `GET` | `/addEMRSearchPendingServicetoVisit` | `EMRServiceAdditionController` | `addEMRSearchPendingServicetoVisit` | `web/api` |
| `GET` | `/tempEMRUserVisitList` | `EMRMainController` | `tempEMRUserVisitList` | `web/api` |
| `GET` | `/ viewInsMod/{id?}` | `InstalledModulesController` | `getInsMod` | `web/api` |
| `GET` | `/addInstalledModules` | `InstalledModulesController` | `getAddInstalledModules` | `web/api` |
| `POST` | `/addInstalledModules` | `InstalledModulesController` | `postAddInstalledModules` | `web/api` |
| `GET` | `/editInstalledModules/{ser_no}` | `InstalledModulesController` | `getEditInstalledModules` | `web/api` |
| `POST` | `/editInstalledModules` | `InstalledModulesController` | `postEditInstalledModules` | `web/api` |
| `GET` | `/deleteInstalledModules/{ser_no}` | `InstalledModulesController` | `getdeleteInstalledModules` | `web/api` |
| `GET` | `/status/{ser_no}/{status}` | `InstalledModulesController` | `getInstalledModulesStatusToChange` | `web/api` |
| *...* | *+1100 more routes mapped to PRIOR VISIT MODULE* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `OPReferralPAToClinicVisit` (`app/Services/OPReferralPAToClinicVisit.php`)
  - Methods: `loadPreviousApprPriorVisitPaymentDetails()`, `getOPReferralApprovedPAVisit()`
- **Service**: `OTModuleService` (`app/Services/OTModuleService.php`)
- **Service**: `VisitEncounterLinkService` (`app/Services/VisitEncounterLinkService.php`)
  - Methods: `saveVisitEncounterLink()`, `getVisitEncounterLinkdata()`, `getVisitEncounterTypedata()`, `changestatus()`, `VisitEncounterLinkDownload()`
- **Service**: `PatientVisitDischargeSummaryDetailService` (`app/Services/PatientVisitDischargeSummaryDetailService.php`)
  - Methods: `checkAndGetVisitDischargeSummary()`, `insertOrUpdateVisitDischargeSummary()`, `getPatientVisitDischargeSummary()`, `createUpdateBranchBaseDischarge()`, `StrQuoteReplace()`
- **Service**: `CreateOtherBranchOpReferralVisitService` (`app/Services/CreateOtherBranchOpReferralVisitService.php`)
  - Methods: `addPriorVisitFromOtherBranchToCurrentVisit()`, `addProirServicetoCurrentHimesVisit()`, `getPAServiceDetails()`, `getotherBranchServicetoCurrentBranchVisit()`, `getPAInsCardDetTOCurrBranchHAVisit()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: PURCHASE (ID: PUR)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PUR`
- **Module Name**: `PURCHASE`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Billing Shipment Details, PO Pricelist, PO User Approved Limit Amount, Procurement, Procurement Masters, Procurement Transactions, Purchase Analysis by Invoice / Item(s)., Purchase Installation Parameters, Purchase Invoice, Purchase Item Group General Ledger Link
- **Discovered Sub-functions & Action Page Links** (23 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `BILSHIPDET` | BILLING SHIPMENT DETAIL | `ViewBillingShipmentDetails` | Billing Shipment Details | - |
| `POUALM` | PO User Approved Limit Amount | `viewPOUserApproved` | PO User Approved Limit Amount | - |
| `PURANA` | PURCHASE ANALYSIS | `PurchaseAnalysis` | Purchase Analysis by Invoice / Item(s). | - |
| `PURINSPARA` | PURCHASE INSTALLATION PARAMETERS | `ViewPurchaseInstParam` | Purchase Installation Parameters | - |
| `PURINV` | PURCHASE INVOICE | `PurchaseInvoiceList` | Purchase Invoice | Create & View Invoices |
| `PURLEDGER` | PURCHASE ITEM GROUP GENERAL LEDGER LINK | `ViewPurchaseItemLedger` | Purchase Item Group General Ledger Link | - |
| `PURMASTR` | PURCHASE MASTER | `dashboard` | Procurement Masters | Procurement Setup & Configurations |
| `PURCHASE` | PURCHASE MENU | `dashboard` | Procurement | Procurement Management |
| `PURREQ` | PURCHASE MODULE REQUEST | `PurchaseModRequestList` | Purchase Request | Create & View Requests |
| `PURORD` | PURCHASE ORDER | `PurchaseOrderList` | Purchase Order | Create & View Orders |
| `PRPRICELST` | PURCHASE PRICE LIST | `PurchasePriceList` | PO Pricelist | Purchase Pricelist configuration |
| `PCHSTAXTYP` | PURCHASE TAX TYPE | `viewPurchaseTaxTypeItem` | Purchase Tax Type | Description of PURCHASE TAX TYPE |
| `PCTAXTYPIT` | PURCHASE TAX TYPE ITEM | `viewPurchaseTaxTypeItem` | Purchase Tax Type Items | Description of PURCHASE TAX TYPE ITEMS |
| `PCTXTYITSL` | PURCHASE TAX TYPE ITEMS STOCK LOCATION | `viewPurchaseTaxTypeItemStockLocation` | Purchase Tax Type Items Stock Location | Description of PURCHASE TAX TYPE STOCK LOCATION |
| `PURTRANS` | PURCHASE TRANSACTION | `dashboard` | Procurement Transactions | Process Requests, Orders, & Invoices |
| *...* | *+8 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Purchase_` (7 tables), `PurchaseReturn_` (1 tables)
- **Associated Tables Count**: 13 tables identified
- **Key Tables**: `Branch_Based_Purchase_Invoice`, `Branch_Based_Purchase_Order`, `Branch_Based_Purchase_Request`, `EMR_User_Dashboard`, `PurchaseReturn_QuickBook`, `Purchase_Installation_Parameters`, `Purchase_Item_Group_General_Ledger_Link`, `Purchase_Request_Detail`, `Purchase_Request_Header`, `Purchase_Tax_Type`, `Purchase_Tax_Type_Items`, `Purchase_Tax_Type_Items_Stock_Location`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
*(Shared Eloquent models utilized across modules via repository layer)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PurchaseTaxTypeController` (`app/Http/Controllers/PurchaseTaxTypeController.php`)
  - **Action Methods**: `viewPurchaseTaxType()`, `addPurchaseTaxType()`, `postAddPurchaseTaxType()`, `editPurchaseTaxType()`, `postEditPurchaseTaxType()`, `changeStatusPurchaseTaxType()`, `downloadPurchaseTaxType()`, `deletePurchaseTaxType()`
- **Controller**: `BranchBasedPurchaseInvoiceController` (`app/Http/Controllers/BranchBasedPurchaseInvoiceController.php`)
  - **Action Methods**: `viewBrnchBsePrchaseInv()`, `getdownloadPurchaseInv()`, `changeStatus()`, `getViewBrnchBsePrchaseInv()`, `getAddBrBsePurchaseInv()`, `GetCompany()`, `GetBranch()`, `postAddBrBsePurchaseInv()`
- **Controller**: `PurchaseItemGrpLegderLinkController` (`app/Http/Controllers/PurchaseItemGrpLegderLinkController.php`)
  - **Action Methods**: `getAddPurchaseItemGroupLedgerLink()`, `postAddPurchaseItemGroupLedgerLink()`, `getViewPurchaseItemLedger()`, `GetItemGroup()`, `DownloadPurchaseItemLedger()`, `getEditStatusPurchaseItemGrp()`, `DeletePurchaseItemGrpLedger()`, `getEditPurchaseItemGroupLedgerLink()`
- **Controller**: `BranchBasedPurchaseRequestController` (`app/Http/Controllers/BranchBasedPurchaseRequestController.php`)
  - **Action Methods**: `viewBrnchBsePrchaseReq()`, `getAddBrBsePurchaseReq()`, `GetCompany()`, `GetBranch()`, `postAddBrBsePurchaseReq()`, `geteditBrBsePurchaseReq()`, `posteditBrBsePurchaseReq()`, `getdownloadPurchaseReq()`
- **Controller**: `PurchaseRequestController` (`app/Http/Controllers/PurchaseRequestController.php`)
  - **Action Methods**: `getPurchaseRequestList()`, `PurhcaseRequestListHeader()`, `PurhcaseRequestListItems()`, `PurchaseRequestDownload()`, `PurchaseRequestPrint()`, `postPurchaseRequestAdd()`, `getPurchaseRequestEdit()`, `getPurchaseRequestCancel()`
- **Controller**: `PurchaseAnalysisController` (`app/Http/Controllers/PurchaseAnalysisController.php`)
  - **Action Methods**: `getPurchaseAnalysisList()`, `getPurchaseInvoiceNo()`, `getPurchaseOrderNo()`, `getPurchaseRequestNo()`, `PurchaseInvoiceList()`, `PurchaseInvoiceListItems()`, `PurchaseOrderItems()`, `PurhcaseRequestItems()`
- *(+18 more controllers handling PURCHASE)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/viewPOUserApproved/{id?}` | `POUserApprovedAmountController` | `getViewPOUserApproved` | `web/api` |
| `GET` | `/PurchaseRequestList/{id?}` | `PurchaseRequestController` | `getPurchaseRequestList` | `web/api` |
| `GET` | `/PurchaseRequestAdd` | `PurchaseRequestController` | `postPurchaseRequestAdd` | `web/api` |
| `GET` | `/PurchaseRequestEdit/{id}/{detailId?}` | `PurchaseRequestController` | `getPurchaseRequestEdit` | `web/api` |
| `GET` | `/PurchaseRequestCancel/{id}/{detailId?}` | `PurchaseRequestController` | `getPurchaseRequestCancel` | `web/api` |
| `POST` | `/getPurchaseRequestCounter` | `PurchaseRequestController` | `getPurchaseRequestCounter` | `web/api` |
| `POST` | `/PurchaseRequestItems` | `PurchaseRequestController` | `ProcessOnPurchaseRequestItems` | `web/api` |
| `POST` | `/AddPurchaseRequest` | `PurchaseRequestController` | `PostAddPurchaseRequest` | `web/api` |
| `POST` | `/PurhcaseRequestListHeader` | `PurchaseRequestController` | `PurhcaseRequestListHeader` | `web/api` |
| *...* | *+306 more routes mapped to PURCHASE* | | | |

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: RADIOLOGY INFORMATION SYSTEM (ID: RIS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `RIS`
- **Module Name**: `RADIOLOGY INFORMATION SYSTEM`
- **Database Active Status**: Active (`A`)
- **Associated Menus**:  SAMPLE AUDIT LOG, Body Site, MODALITY LIST LINK, Modality List, PACS VIEWER, RIS, RIS Installation Parameter, RIS Masters, RIS SCREENING SHORT CODE, RIS Worklist
- **Discovered Sub-functions & Action Page Links** (25 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `SERVICELOC` | Body Site | `viewServiceLocation` | Body Site | - |
| `MODALITYLI` | MODALITY LIST | `ViewModalityList` | Modality List | - |
| `MODLILINK` | MODALITY LIST LINK | `ViewModalityListLink` | MODALITY LIST LINK | - |
| `RISIPTP` | PACS VIEWER | `pacs-type-pages` | PACS VIEWER | - |
| `RIS` | RADIOLOGY INFORMATION SYSTEM | `dashboard` | - | - |
| `REDERTYL` | REPORT DEPARTMENT RESOURCE TYPE LINKS | `viewReportDeptResourcetypeslink` | Report Dept Resource Types Link | - |
| `REPORTTEMP` | REPORT TEMPLATE | `viewReportTemplate` | Report Template | - |
| `RETYORPRI` | RESOURCE TYPE ORDER PRIVILEGES | `viewResourceTypeorderprivileges` | Resource Type Order Privileges | - |
| `RETYREPRI` | RESOURCE TYPE REPORT PRIVILEGES | `viewResourceTypereportprivileges` | Resource Type Report Privileges | - |
| `RISCRTEMP` | RIS Custom Report Templates | `risCustomReportTemplates` | - | - |
| `RISINSPARA` | RIS INSTALLATION PARAMETER | `previous_value` | RIS Installation Parameter | - |
| `RISMSTR` | RIS MASTER | `#` | RIS Masters | RIS Setup & Configurations |
| `DOCDETRIS` | RIS Patient Document Details | `previous_value` | - | - |
| `RISHORTCOD` | RIS SCREENING SHORT CODE MASTER | `previous_value` | RIS SCREENING SHORT CODE | RIS SCREENING SHORT CODE MASTER |
| `RISEMSET` | RIS SERVICE EMAIL SETUP | `viewRisEmailSetup` | Ris Service Email Setup | - |
| *...* | *+10 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `RIS_` (15 tables), `ris_` (4 tables)
- **Associated Tables Count**: 229 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Type`, `Allergy_Type_Allergy_Name_Link`, `Allergy_Type_Parameter`, `Allergy_Values`, `Appointment_Status_Type`, `Appointment_Visit_Questionnaire_Types`, `Appointment_Visit_Questionnaire_Types_Services`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `Allergy_Type`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Allergy_Type_Serial_No` | `smallint` | - | NO | - |
| `Allergy_Type_Name` | `varchar` | 100 | NO | - |
| `Allergy_Type_Code` | `varchar` | 2 | NO | ('FO') |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

*Table: `Allergy_Type_Allergy_Name_Link`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Allergy_Type_Allergy_Name_Link_Serial_No` | `bigint` | - | NO | - |
| `Allergy_Type_Serial_No` | `smallint` | - | NO | - |
| `Allergy_Group_Serial_No` | `smallint` | - | YES | - |
| `Allergy_Machine_Test_Code_Serial_No` | `bigint` | - | NO | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| `Modified_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Modified_Date_Time` | `datetime` | - | NO | - |
| `Active_Status` | `nvarchar` | 1 | NO | ('A') |

### 3. Eloquent Models & Data Architecture
- **Model**: `RIS_Screening_Lock_Patient` (`app/Models/RIS_Screening_Lock_Patient.php`)
  - **Database Table**: `RIS_Screening_Lock_Patient` | **Primary Key**: `RIS_Screening_Lock_Patient_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No `, `Locked_Start_Date_Time`, `Locked_End_Date_Time`, `Locked_By_User_ID`, `Locked_By_Date_Time`, `Order_Sequence`, `Active_Status`...
- **Model**: `ItemType` (`app/Models/ItemType.php`)
  - **Database Table**: `Item_Type` | **Primary Key**: `Item_Type_Serial_No`
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `InventoryReasonType` (`app/Models/InventoryReasonType.php`)
  - **Database Table**: `Inventory_Reason_Type` | **Primary Key**: `Inventory_Reason_Type_Serial_No`
- **Model**: `Patient_Visit_PAC_Assessment_Information_Details` (`app/Models/Patient_Visit_PAC_Assessment_Information_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Assessment_Information_Details` | **Primary Key**: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Assessment_Anaesthesia_Type`], `hasMany(Patient_Visit_PAC_Previous_Anaesthesia_History_Details)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Plan_Of_Care)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Airway_Definition)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`], `hasMany(Patient_Visit_PAC_Drugs_List)` [Key/Pivot: `Patient_Visit_PAC_Assessment_Information_Details_Serial_No`]
- **Model**: `PAResubmission` (`app/Models/PAResubmission.php`)
  - **Database Table**: `PA_Patient_Visit_Resubmission_Type_Comments` | **Primary Key**: `PA_Patient_Visit_Resubmission_Type_Comments_Serial_No`
- *(+74 additional Eloquent models associated with RADIOLOGY INFORMATION SYSTEM)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PatientAssitanceTypesController` (`app/Http/Controllers/PatientAssitanceTypesController.php`)
  - **Action Methods**: `getViewPatientAssitanceTypes()`, `getAddPatientAssitanceTypes()`, `alreadyExists()`, `postAddPatientAssitanceTypes()`, `getPatientAssitanceTypesstatus()`, `getEditPatientAssitanceTypes()`, `postEditPatientAssitanceTypes()`, `getDeletePatientAssitanceTypes()`
- **Controller**: `PurchaseTaxTypeController` (`app/Http/Controllers/PurchaseTaxTypeController.php`)
  - **Action Methods**: `viewPurchaseTaxType()`, `addPurchaseTaxType()`, `postAddPurchaseTaxType()`, `editPurchaseTaxType()`, `postEditPurchaseTaxType()`, `changeStatusPurchaseTaxType()`, `downloadPurchaseTaxType()`, `deletePurchaseTaxType()`
- **Controller**: `AllergyTypeParameterController` (`app/Http/Controllers/AllergyTypeParameterController.php`)
  - **Action Methods**: `index()`, `ChangeStatus()`, `create()`, `store()`, `edit()`, `update()`, `show()`, `destroy()`
- **Controller**: `StockItemTaxTypeController` (`app/Http/Controllers/StockItemTaxTypeController.php`)
  - **Action Methods**: `viewStockItemTaxType()`, `addStockItemTaxType()`, `postAddStockItemTaxType()`, `editStockItemTaxType()`, `postEditStockItemTaxType()`, `changeStatusStockItemTaxType()`, `downloadStockItemTaxType()`, `deleteStockItemTaxType()`
- **Controller**: `EmrRadiologyReportController` (`app/Http/Controllers/EmrRadiologyReportController.php`)
  - **Action Methods**: `emrRadiologyReportgeneration()`, `getEmrRadiologyReportReviewed()`
- **Controller**: `RefDocTypeController` (`app/Http/Controllers/RefDocTypeController.php`)
  - **Action Methods**: `GetAddRefDocType()`, `PostAddRefDocType()`, `alreadyexitsArea()`, `alreadyExistsPostal()`, `getViewRefDocType()`, `EditStatusRefDocType()`, `DeleteRefDocType()`, `GetEditRefDocType()`
- *(+70 more controllers handling RADIOLOGY INFORMATION SYSTEM)*

### 5. Form Requests & Input Validation Rules
- **Form Request**: `StoreEMRCommonMastersTypeRequest` (`app/Http/Requests/StoreEMRCommonMastersTypeRequest.php`)
  - **Validation Rules**:
    - `//         EMR_Common_Type_Description => required|string|max:200`
    - `//         Order_Sequence => required|integer`
    - `//         Branch_Code => required|string|max:20|unique:EMR_Common_Masters_Type,Branch_Code`
    - `//         selectedData.*.EMR_Common_Description => required|string|max:200`
    - `//         selectedData.*.Textbox_Required => required|string|in:Y,N`
    - `//         selectedData.*.Score_Is_Applicable => required|string|in:Y,N`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/idntyTypebranExistsInDB` | `InstalledModulesController` | `postInstalledBranchExists` | `web/api` |
| `GET` | `/nationalityIDTypeMapping/{id?}` | `IdentificationTypeController` | `getnationalityIDTypeMapping` | `web/api` |
| `GET` | `/addIDNationalityMapping` | `IdentificationTypeController` | `addIDNationalityMapping` | `web/api` |
| `POST` | `/addIDentNatMapping` | `IdentificationTypeController` | `addIDentNatMapping` | `web/api` |
| `POST` | `/getIDentityType` | `NationalityController` | `getIDentityType` | `web/api` |
| `GET` | `/changeNatIdentTypeStatusToChange/{code}/{status}` | `IdentificationTypeController` | `getNationalIdentificationTypeStatusToChange` | `web/api` |
| `GET` | `/editNatIdentificationType/{code}` | `IdentificationTypeController` | `getNatIdentificationTypeToEdit` | `web/api` |
| `POST` | `/editNatIdentificationType` | `IdentificationTypeController` | `postEditedNatIdentificationType` | `web/api` |
| `GET` | `/deleteNatIdentificationType/{code}` | `IdentificationTypeController` | `getdeleteNatIdentificationType` | `web/api` |
| `GET` | `/downloadNatIdentificationType` | `IdentificationTypeController` | `downloadNatIdentificationTypeDetails` | `web/api` |
| *...* | *+1098 more routes mapped to RADIOLOGY INFORMATION SYSTEM* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `ClaimMandatoryObservationTypeService` (`app/Services/ClaimMandatoryObservationTypeService.php`)
  - Methods: `saveClaimMandatoryObservationType()`, `getClaimMandatoryObservationTypedata()`, `changestatus()`, `ClaimMandatoryObservationTypeDownload()`, `getBranchBasedModule()`
- **Service**: `RISWorkListService` (`app/Services/RISWorkListService.php`)
- **Service**: `ScheduleTypeDateRangeService` (`app/Services/ScheduleTypeDateRangeService.php`)
- **Service**: `Immuntype` (`app/Services/Immuntype.php`)
  - Methods: `immuntype()`
- **Service**: `CCHPITypeService` (`app/Services/CCHPITypeService.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: REGISTRATION (ID: REG)

### 1. Module Overview & Navigation Structure
- **Module ID**: `REG`
- **Module Name**: `REGISTRATION`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: BULK PATIENT REGISTRATION, Claim Mandatory Observation Type, Detailed Visit Registration, Eligibility Check, Emirates Member & Eligibility Check, Front Desk, Global View Of Registration, Global View of Certificate, Global view of Prior Authorization, Insurance Pre Approvals
- **Discovered Sub-functions & Action Page Links** (67 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `BULKREG` | BULK PATIENT REGISTRATION | `uploadPatientRegistration` | BULK PATIENT REGISTRATION | - |
| `CMOT` | Claim Mandatory Observation Type | `ClaimMandatoryObservationType` | Claim Mandatory Observation Type | - |
| `DOCACCESS` | DOCUMENT ACCESS | `#` | - | - |
| `DOCUPLOAD` | DOCUMENT UPLOAD | `VisitBasedDocumentUpload` | Patient Documents | Manage Patients Extenral Documents |
| `ELIGCHECK` | ELIGIBILITY CHECK | `redirectToEligibility` | Eligibility Check | ELIGIBILITY CHECK |
| `FRONTDESK` | FRONT DESK | `dashboard` | Front Desk | Registration With Patient Sidebar |
| `GLOBCERT` | GLOBAL VIEW OF CERTIFICATE | `certificateGlobalView` | Global View of Certificate | View & Manage Issued Certificates |
| `GLOBREGTRN` | GLOBAL VIEW OF REGISTRATION | `registrationGlobalView` | Global View Of Registration | View & Manage Registrations |
| `INSPREAPP` | Insurance Pre Approvals | `getInsurancePreApprovals` | Insurance Pre Approvals | - |
| `MNGREGIS` | MANAGE REGISTRATION | `patientRegistration` | Detailed Visit Registration | Registration With Patient Sidebar |
| `CERTIFTAB` | MANAGE TAB  CERTIFICATE | `patientRegistration#tabVisitCertificate` | - | - |
| `APPOINTMNT` | MANAGE TAB APPOINTMENT | `patientRegistration#tabAppointments` | - | - |
| `DEMOGRPICS` | MANAGE TAB DEMOGRAHPICS | `patientRegistration#tabDemographics` | - | - |
| `DOCUMENTS` | MANAGE TAB DOCUMENTS | `patientRegistration#tabDocuments` | - | - |
| `INJONDUTY` | MANAGE TAB INJURY ON DUTY | `patientRegistration#tabViewInjuryOnDuty` | - | MANAGE TAB INJURY ON DUTY |
| *...* | *+52 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Patient_` (622 tables), `patient_` (2 tables), `registration_` (2 tables), `Registration_` (1 tables)
- **Associated Tables Count**: 760 tables identified
- **Key Tables**: `Adm_AVP_PatientDB`, `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`, `Children_MH_Attribute_Values`, `Claim_Mandatory_Observation_Type`, `DDWC_Patient_Leave_Details`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `RIS_Screening_Lock_Patient` (`app/Models/RIS_Screening_Lock_Patient.php`)
  - **Database Table**: `RIS_Screening_Lock_Patient` | **Primary Key**: `RIS_Screening_Lock_Patient_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Services_Serial_No `, `Locked_Start_Date_Time`, `Locked_End_Date_Time`, `Locked_By_User_ID`, `Locked_By_Date_Time`, `Order_Sequence`, `Active_Status`...
- **Model**: `Patient_Visit_Anesthesia_Medications_Detailed_Result` (`app/Models/Patient_Visit_Anesthesia_Medications_Detailed_Result.php`)
  - **Database Table**: `Patient_Visit_Anesthesia_Medications_Detailed_Result` | **Primary Key**: `Patient_Visit_Anesthesia_Medications_Detailed_Result_Serial_No`
  - **Eloquent Relationships**: `belongsTo(Patient_Visit_Anesthesia_Medications_Result_Items)`
- **Model**: `SecondaryCardDetails` (`app/Models/SecondaryCardDetails.php`)
  - **Database Table**: `Patient_Visit_Secondary_Insurance_Card_Details` | **Primary Key**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Secondary_Insurance_Card_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `Patient_Insurance_Card_Details_Serial_No`, `Patient_Visit_Insurance_Remarks`, `Show_Remarks_Alert_In_Billing`, `Remarks_Read_In_Billing`, `Insurance_Plan_Serial_No`, `Insurance_Company_Serial_No`...
- **Model**: `PatientVisitDrugScheduleIVAdministrationLog` (`app/Models/PatientVisitDrugScheduleIVAdministrationLog.php`)
  - **Database Table**: `Patient_Visit_Drug_Schedule_IV_Administration_Log` | **Primary Key**: `Patient_Visit_Drug_Schedule_IV_Administration_Log_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`, `IV_Start_Resume_Time`, `IV_End_Pause_Time`, `Rate`, `Type`, `Started_By_User_Id`, `Paused_By_User_Id`, `Resume_By_User_Id`...
  - **Eloquent Relationships**: `belongsTo(PatientVisitDrugScheduleIVAdminstration)` [Key/Pivot: `Patient_Visit_Drug_Schedule_IV_Adminstration_Serial_No`]
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Patient_Visit_Physician_Assessment_Form` (`app/Models/Patient_Visit_Physician_Assessment_Form.php`)
  - **Database Table**: `Patient_Visit_Physician_Assessment_Form` | **Primary Key**: `Patient_Visit_Physician_Assessment_Form_Serial_No`
  - **Constants / Status Flags**: `SAVE_COMPLETE_OPTION_NO = "N"`, `SAVE_COMPLETE_OPTION_COMPLETED = "C"`
- *(+205 additional Eloquent models associated with REGISTRATION)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `PatientBillingBackendController` (`app/Http/Controllers/PatientBillingBackendController.php`)
  - **Action Methods**: `modifyInvoiceDate()`, `UPDInvoiceDate()`, `modifyInvoiceReceipt()`, `UPDInvoiceReceipt()`, `UPDInvoiceReceiptAmt()`, `getInvoiceVisitRegisteredDateTime()`
- **Controller**: `PatientAssitanceTypesController` (`app/Http/Controllers/PatientAssitanceTypesController.php`)
  - **Action Methods**: `getViewPatientAssitanceTypes()`, `getAddPatientAssitanceTypes()`, `alreadyExists()`, `postAddPatientAssitanceTypes()`, `getPatientAssitanceTypesstatus()`, `getEditPatientAssitanceTypes()`, `postEditPatientAssitanceTypes()`, `getDeletePatientAssitanceTypes()`
- **Controller**: `VisitEncounterLinkController` (`app/Http/Controllers/VisitEncounterLinkController.php`)
  - **Action Methods**: `index()`, `create()`, `store()`, `edit()`, `update()`, `show()`, `ChangeStatus()`, `Download()`
- **Controller**: `GlobalViewRegistrationController` (`app/Http/Controllers/GlobalViewRegistrationController.php`)
  - **Action Methods**: `StrQuoteReplace()`, `viewGlobalRegistration()`, `testglobalreg()`, `downloadglobal()`, `getgeneratePDF()`, `getgeneratePrint()`, `getPatientSearch()`, `temppatientsearchSession()`
- **Controller**: `PatientdbfieldsController` (`app/Http/Controllers/PatientdbfieldsController.php`)
  - **Action Methods**: `getviewpatientdbfields()`, `getaddpatientdbfields()`, `postaddpatientdbfields()`, `changepatientdbfieldstatus()`, `getdeletepatientdbfields()`, `geteditpatientdbfields()`, `posteditpatientdbfields()`, `downloadPatientdbfields()`
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- *(+104 more controllers handling REGISTRATION)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/removePatientRelatedSessionInfo` | `ConnectionsController` | `removePatientRelatedSessionInfo` | `web/api` |
| `GET` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `getEditOnlinePatient` | `web/api` |
| `POST` | `/editOnlinePatient` | `OnlineAppointmentSchedulerController` | `postEditOnlinePatient` | `web/api` |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/getPatientVisitInsuranceCount` | `InsurancecompanyController` | `getPatientVisitInsuranceCount` | `web/api` |
| `GET` | `/patientPaymentType/{id?}` | `PartnerPaymentTypeController` | `getIndex` | `web/api` |
| `GET` | `/patientPaymentTypeAdd` | `PartnerPaymentTypeController` | `getAddpatientPaymentType` | `web/api` |
| `POST` | `/patientPaymentTypeAdd` | `PartnerPaymentTypeController` | `postAddpatientPaymentType` | `web/api` |
| `POST` | `/patientpaymentcodeexitsts` | `PartnerPaymentTypeController` | `PatientPaymentExitstsCode` | `web/api` |
| `GET` | `/changePatientPaymentTypestatus/{id}/{status}` | `PartnerPaymentTypeController` | `getchangePaymentStatus` | `web/api` |
| *...* | *+1686 more routes mapped to REGISTRATION* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `ClaimMandatoryObservationTypeService` (`app/Services/ClaimMandatoryObservationTypeService.php`)
  - Methods: `saveClaimMandatoryObservationType()`, `getClaimMandatoryObservationTypedata()`, `changestatus()`, `ClaimMandatoryObservationTypeDownload()`, `getBranchBasedModule()`
- **Service**: `EMRPatientHealthQuestionnaireService` (`app/Services/EMRPatientHealthQuestionnaireService.php`)
  - Methods: `viewEMRPatientHealthQuestionnaireDetails()`, `getEMRCommonMasterDetails()`, `currentVisitData()`, `getPatVisiEMHumptDumptySno()`, `GenAnxDisdrFallPrvntnDatas()`
- **Service**: `VisitEncounterLinkService` (`app/Services/VisitEncounterLinkService.php`)
  - Methods: `saveVisitEncounterLink()`, `getVisitEncounterLinkdata()`, `getVisitEncounterTypedata()`, `changestatus()`, `VisitEncounterLinkDownload()`
- **Service**: `PatientVisitDischargeSummaryDetailService` (`app/Services/PatientVisitDischargeSummaryDetailService.php`)
  - Methods: `checkAndGetVisitDischargeSummary()`, `insertOrUpdateVisitDischargeSummary()`, `getPatientVisitDischargeSummary()`, `createUpdateBranchBaseDischarge()`, `StrQuoteReplace()`
- **Service**: `PatientVisitResourceService` (`app/Services/PatientVisitResourceService.php`)
  - Methods: `getPatientVisitResourceNameAndID()`, `getPAPatientVisitResourceUserId()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: REPORTS (ID: RPT)

### 1. Module Overview & Navigation Structure
- **Module ID**: `RPT`
- **Module Name**: `REPORTS`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: BI Reports, Bill Register, By Appointment, By Status, Deposit Report, Kool Reports, Receipt, Refund Report, Registration By Insurance, Registration By Payment
- **Discovered Sub-functions & Action Page Links** (23 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ANLREP` | Analytics Report | `byAnalyticsReport` | - | - |
| `APPSTSRPT` | APPOINTMENT STATUS REPORT | `globalviewappointmentbystatus` | By Status | - |
| `NEXTRPT` | BI - Reports | `viewNewReports` | Report | View & Extract Reports |
| `BIRPT` | BI Reports | `previous_value` | BI Reports | Description of BI report |
| `BILREGRPT` | BILL REGISTER REPORT | `viewBillRegisterReport` | Bill Register | - |
| `DEPRPT` | DEPOSIT REPORT | `viewDepositReport` | Deposit Report | - |
| `GLOAPPRPT` | GLOBAL VIEW APPOINTMENT | `viewglobalviewappointment` | By Appointment | - |
| `KOOLRPT` | KOOL Reports | `previous_value` | Kool Reports | Description of Kool report |
| `KOOLRPT` | KOOL Reports | `previous_value` | Reports New | Description of Kool report |
| `RECRPT` | RECEIPT REPORT | `viewReceiptReport` | Receipt | - |
| `REFRPT` | REFUND REPORT | `refundreport` | Refund Report | - |
| `REGINSRPT` | REGISTRATION BY INSURANCE | `insurancecpyvisitreport` | Registration By Insurance | - |
| `REGPAYRPT` | REGISTRATION BY PAYMENT | `paymentWisevisitreport` | Registration By Payment | - |
| `REGREFRPT` | REGISTRATION BY REFERRAL | `referalclinicwisevisitdetail` | Registration By Referral Clinic | - |
| `REGRESRPT` | REGISTRATION BY RESOURCE | `resourceWisevisitreport` | Registration By Resource | - |
| *...* | *+8 more sub-functions* | | | |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Report_` (11 tables), `Reporting_` (1 tables)
- **Associated Tables Count**: 135 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Branch_Based_EMR_Panel_Report`, `Branch_Based_EMR_Panel_Report_Sub_Details`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`, `Children_MH_Attribute_Values`, `DHA_Report_Code`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `HimesReportsScheduleDetailsLogs` (`app/Models/HimesReportsScheduleDetailsLogs.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details_Logs` | **Primary Key**: `Himes_Reports_Schedule_Details_Logs_Serial_No`
- **Model**: `ReportBasedBranch` (`app/Models/ReportBasedBranch.php`)
  - **Database Table**: `Report_Based_Branch_Details` | **Primary Key**: `Report_Based_Branch_User_Details_Serial_No`
- **Model**: `HimesReportsScheduleDetails` (`app/Models/HimesReportsScheduleDetails.php`)
  - **Database Table**: `Himes_Reports_Schedule_Details` | **Primary Key**: `Himes_Reports_Schedule_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(ReportFunctionURL)` [Key/Pivot: `Report_Function_URL_Serial_No`]
- **Model**: `ReportFunctionURL` (`app/Models/ReportFunctionURL.php`)
  - **Database Table**: `Report_Function_URL` | **Primary Key**: `Report_Function_URL_Serial_No`
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- *(+11 additional Eloquent models associated with REPORTS)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `UserTestResultReportingConroller` (`app/Http/Controllers/UserTestResultReportingConroller.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getviewusertestresultreprting()`, `getaddusertestresultreprting()`
- **Controller**: `UserTestResultReportingController` (`app/Http/Controllers/UserTestResultReportingController.php`)
  - **Action Methods**: `getviewusertestresultreporting()`, `getspacilityvalues()`, `Postimagedata()`, `gettemplatevalues()`, `getViewUserTestResultReportingprivilages()`, `getAddUserTestResultReporting()`, `getservicevalues()`, `gettemplatedetails()`
- **Controller**: `EmrRadiologyReportController` (`app/Http/Controllers/EmrRadiologyReportController.php`)
  - **Action Methods**: `emrRadiologyReportgeneration()`, `getEmrRadiologyReportReviewed()`
- **Controller**: `NewReportTemplateController` (`app/Http/Controllers/NewReportTemplateController.php`)
  - **Action Methods**: `NewaddReportTemplate()`, `Ristemlateeditor()`, `getriseditorval()`, `PatientvisitpayemtdetailsPanel()`, `viewPatientHeader()`, `patientpaymentdetailpanel()`, `newpatientpaymentdetailpanel()`, `MultipletemplateEdit()`
- **Controller**: `reportJRSController1` (`app/Http/Controllers/reportJRSController1.php`)
  - **Action Methods**: `reportJRS()`, `reportdownJRS1()`, `reportdownJRS2()`
- **Controller**: `EmrLabReportController` (`app/Http/Controllers/EmrLabReportController.php`)
  - **Action Methods**: `getemrlabreportparameter()`, `labReviewDetailsupdate()`, `viewHeaderforemrlisReport()`
- *(+79 more controllers handling REPORTS)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/testReport` | `TestReportController` | `gettestReportDetails` | `web/api` |
| `GET` | `/Reportpdfgeneration` | `TestReportController` | `getreportpdfgeneration` | `web/api` |
| `GET` | `/generatePDFreport` | `TestReportController` | `viewgeneratipdf` | `web/api` |
| `GET` | `/reportpdfgenetationtest` | `TestReportController` | `postreportpdfgeneration` | `web/api` |
| `GET` | `/dashboard/{id?}/{parentId?}` | `MenuController` | `getIndex` | `web/api` |
| `GET` | `/viewReportSchedule/{id?}` | `ReportScheduleController` | `getListReportSchedule` | `web/api` |
| `GET` | `/editReportSchedule/{id?}` | `ReportScheduleController` | `getEditReportSchedule` | `web/api` |
| `GET` | `/runScheduleJob/{id?}` | `ReportScheduleController` | `runScheduleJob` | `web/api` |
| `GET` | `/editStatusReportSchedule/{id?}` | `ReportScheduleController` | `getEditStatusReportSchedule` | `web/api` |
| `GET` | `/deleteReportSchedule/{id?}` | `ReportScheduleController` | `getDeleteReportSchedule` | `web/api` |
| *...* | *+869 more routes mapped to REPORTS* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `JasperReportDownloadForftp` (`app/Services/JasperReportDownloadForftp.php`)
  - Methods: `ReportDownloadForftp()`
- **Service**: `ReportGeneratorService` (`app/Services/ReportGeneratorService.php`)
  - Methods: `generateAndSend()`
- **Service**: `HimesReportService` (`app/Services/HimesReportService.php`)

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: THERAPY (ID: PHY)

### 1. Module Overview & Navigation Structure
- **Module ID**: `PHY`
- **Module Name**: `THERAPY`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: THERAPY, THERAPY WORKLIST, Therapy Template, WORKFLOW SERVICE
- **Discovered Sub-functions & Action Page Links** (5 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `PHYTP` | THERAPY | `previous_value` | THERAPY | - |
| `PHYTPMS` | THERAPY MASTER | `previous_value` | - | - |
| `THPYTEPMA` | Therapy Template Master | `previous_value` | Therapy Template | Therapy Template Master |
| `PHYSIOWLIS` | THERAPY WORK LIST | `getViewPhysioWorklist` | THERAPY WORKLIST | THERAPY WORK LIST |
| `WKFLSER` | Workflow Service | `previous_value` | WORKFLOW SERVICE | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Physio_` (7 tables)
- **Associated Tables Count**: 107 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`, `Children_MH_Attribute_Values`, `DSR_All_Attribute_Values`, `Demographic_Attribute_Age_Values`, `Demographic_Attribute_DOB_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Physio_Order_Details` (`app/Models/Physio_Order_Details.php`)
  - **Database Table**: `Physio_Order_Details` | **Primary Key**: `Physio_Order_Details_Serial_No`
  - **Fillable Attributes**: `Patient_Basic_Details_Serial_No`, `Patient_Visit_Basic_Details_Serial_No`, `No_Of_Remaining_Sessions`, `Total_No_Of_Session`, `Branch_Code`, `Physio_Order_Deleted`, `Ordered_Notes`, `Remarks`...
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `Physio_Order_Details_Diagnosis` (`app/Models/Physio_Order_Details_Diagnosis.php`)
  - **Database Table**: `Physio_Order_Details_Diagnosis` | **Primary Key**: `Physio_Order_Details_Diagonsis_Serial_No`
  - **Fillable Attributes**: `Physio_Order_Details_Serial_No`, `ICD_Code_Serial_No`, `Patient_Visit_ICD_Codes_Serial_No`, `Total_No_Of_Sessions`, `Total_No_Of_Sessions_Remaining`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
- **Model**: `Physio_Order_Details_Services` (`app/Models/Physio_Order_Details_Services.php`)
  - **Database Table**: `Physio_Order_Details_Services` | **Primary Key**: `Physio_Order_Details_Services_Serial_No`
  - **Fillable Attributes**: `Physio_Order_Details_Serial_No`, `Service_USSDB_Serial_No`, `Total_No_Of_Sessions`, `Total_No_Of_Sessions_Remaining`, `Physio_Order_Workflow_Services_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`...
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- **Model**: `PatientVisitLISServicesParameterStatusValues` (`app/Models/PatientVisitLISServicesParameterStatusValues.php`)
  - **Database Table**: `Patient_Visit_LIS_Services_Parameter_Status_Values` | **Primary Key**: `Patient_Visit_LIS_Services_Parameter_Status_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_LIS_Services_Parameter_Serial_No`, `Visit_Service_Level_Status_Type_Code`, `Updated_By_User_Id`, `Updated_Date_Time`, `Reason_Code`, `Remarks`, `Created_By_User_Id`, `Created_Date_Time`...
- *(+18 additional Eloquent models associated with THERAPY)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `TherapyRegistrationPaymentController` (`app/Http/Controllers/TherapyRegistrationPaymentController.php`)
  - **Action Methods**: `PhysioOrderRegistrationAutoComp()`, `CarryForwardTherapyPaymentandServiceDetails()`, `LoadRegistrationServices()`, `getVisitBasedTemplateDetails()`, `getVisitBasedOrderTemplate()`
- **Controller**: `EMRPhysiotherapyController` (`app/Http/Controllers/EMRPhysiotherapyController.php`)
  - **Action Methods**: `getVisitencounterType()`, `getPhysiotherapy()`, `getPhysioInitialEvalutaionResltByUserRunnSno()`, `getPhysioCommonFieldsDetailsResltByUserRunnSno()`, `getBrandenSkinAssessment()`, `getAddSkipAssessmentDetFuncUrl()`, `getAddRecordReferralDetFuncUrl()`, `deleteRecordReferralDetails()`
- **Controller**: `specialityDepartmentVisitServiceStatusValuesController` (`app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`)
  - **Action Methods**: `getspecialityDepartmentVisitServiceStatusValues()`, `alreadyExists()`, `getDownloadspecialityDepartmentVisitServiceStatusValues()`
- **Controller**: `GlobalViewOfUniversalCodeGroupsValuesController` (`app/Http/Controllers/GlobalViewOfUniversalCodeGroupsValuesController.php`)
  - **Action Methods**: `ViewGlobalViewOfUniversalCodeGroupsValues()`, `LoadOptionForUniversalCodeGroupsValuesField()`
- **Controller**: `TherapyWorklistController` (`app/Http/Controllers/TherapyWorklistController.php`)
  - **Action Methods**: `getGlobalFilterPhysioDetails()`, `pendingOrdersScrollRows()`, `ongoingPhysioOrders()`, `ongoingOrdersScrollRows()`, `completedOrders()`, `completedOrdersScrollRows()`, `todayTherapyOrders()`, `getSubgridForTodaysOrder()`
- *(+6 more controllers handling THERAPY)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/universalCodeGroupsValues/{id?}` | `UniversalCodeGroupsValuesController` | `getIndex` | `web/api` |
| `GET` | `/loadUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `loadUniversalCodeGroupValues` | `web/api` |
| `GET` | `/CheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `CheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/EditCheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `EditCheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `getAddUniversalCodeGroupValues` | `web/api` |
| `POST` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `postAddUniversalCodeGroupValues` | `web/api` |
| `GET` | `/changeUniversalCodeGroupValuestatus/{id}/{status}` | `UniversalCodeGroupsValuesController` | `getChangeUniversalCodeGroupValuestatus` | `web/api` |
| `GET` | `/deletUniversalCodeGroupValue/{id}` | `UniversalCodeGroupsValuesController` | `getDeletUniversalCodeGroupValue` | `web/api` |
| `GET` | `/downloadUniversalcodeGroupValues` | `UniversalCodeGroupsValuesController` | `downloadUniversalcodeGroupValues` | `web/api` |
| `GET` | `/editUniversalcodeGroupValue/{id}` | `UniversalCodeGroupsValuesController` | `getEditUniversalcodeGroupValue` | `web/api` |
| *...* | *+231 more routes mapped to THERAPY* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `PhysioTherapyWorkList` (`app/Services/PhysioTherapyWorkList.php`)
  - Methods: `globalViewOfPhysioWorklist()`, `globalViewOfPhysioWorklist_Bk()`, `viewPhysioServiceSubgrid()`, `TherapistAutocomplete()`, `IsPhysioOrderCreatedOrNot()`
- **Service**: `GlobalViewOfTherapyWorklistService` (`app/Services/GlobalViewOfTherapyWorklistService.php`)
- **Service**: `TheraphyRegistrationService` (`app/Services/physioOrder/TheraphyRegistrationService.php`)
  - Methods: `checkTherapyOrder()`, `VisitPhysioOrderval()`, `PhysioOrderAutoComplete()`, `TherapyPaymentDet()`, `checkExistingPaymentType()`
- **Service**: `physiotherapyOrder` (`app/Services/physioOrder/physiotherapyOrder.php`)
  - Methods: `getphysioOrderdata()`, `diagnosisAutocomplete()`, `serviceAutocomplete()`, `ResourceAutocomplete()`, `insertDiagnosisTopatientVisit()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: Transaction Posting (ID: TRP)

### 1. Module Overview & Navigation Structure
- **Module ID**: `TRP`
- **Module Name**: `Transaction Posting`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: Auto Eclaim Posting, Eclaim auto posting, Insurance Installation Parameter, InvoicePost, Post Invoice, Transaction Posting
- **Discovered Sub-functions & Action Page Links** (6 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `AUTOECPOST` | AUTO ECLAIM POST | `viewAutoEclaim` | Eclaim auto posting | Eclaim auto posting mater |
| `AUTOECLMP` | Auto Eclaim Post Close | `viewAutoEclaimPost` | Auto Eclaim Posting | Eclaim auto posting mater |
| `GLBPOSTINV` | GLOBAL POST INVOICE | `#` | InvoicePost | Close Invoices & Post to Eclaims |
| `IINSTPARAM` | Insurance Installation Parameter | `viewInsuranceInstallationParameter` | Insurance Installation Parameter | - |
| `GLBPSTCLM` | INVOICE POSTING | `viewGlobalPostEclaim` | Post Invoice | Close Invoices & Post to Eclaims |
| `TRANPOS` | Transaction Posting | `#` | Transaction Posting | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Associated Tables Count**: 18 tables identified
- **Key Tables**: `Claim_Posting_Reposting_Log_Details`, `Ledger_Posting_Batch`, `Ledger_Posting_Batch_Invoice`, `RA_Files_Downloaded_Transaction_Log`, `Stock_Outward_Transactions_log`, `Stock_Transaction_Header_Reference_Document`, `Stock_Transaction_Header_Referred_Stock_Transaction`, `Stock_Transaction_Series_Counter`, `Stock_Transaction_Type`, `Stock_Transaction_UOM_Details`, `Stock_Transactions_Batch_Detail`, `Stock_Transactions_Detail`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `StockTransactionsDetail` (`app/Models/StockTransactionsDetail.php`)
  - **Database Table**: `Stock_Transactions_Detail` | **Primary Key**: `Stock_Transactions_Detail_Serial_No`
- **Model**: `StockTransactionHeaderReferenceDocument` (`app/Models/StockTransactionHeaderReferenceDocument.php`)
  - **Database Table**: `Stock_Transaction_Header_Reference_Document` | **Primary Key**: `Stock_Transaction_Header_Reference_Document_Serial_No`
- **Model**: `StockTransactionSeriesCounter` (`app/Models/StockTransactionSeriesCounter.php`)
  - **Database Table**: `Stock_Transaction_Series_Counter` | **Primary Key**: `Stock_Transaction_Series_Counter_Serial_No`
- **Model**: `StockTransactionType` (`app/Models/StockTransactionType.php`)
  - **Database Table**: `Stock_Transaction_Type` | **Primary Key**: `Stock_Transaction_Type_Serial_No`
- **Model**: `StockTransactionHeader` (`app/Models/StockTransactionHeader.php`)
  - **Database Table**: `Stock_Transactions_Header` | **Primary Key**: `Stock_Transactions_Header_Serial_No`
- **Model**: `StockTransactionsBatchDetail` (`app/Models/StockTransactionsBatchDetail.php`)
  - **Database Table**: `Stock_Transactions_Batch_Detail` | **Primary Key**: `Stock_Transactions_Batch_Detail_Serial_No`

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `InsuranceClaimSearchTransactionController` (`app/Http/Controllers/INS/InsuranceClaimSearchTransactionController.php`)
  - **Action Methods**: `viewGlobalSearchTransaction()`, `getPaymentTypeSearchFilter()`, `loadINSSearchInsuranceCompany()`, `getDirectionSearch()`, `getTransactionTypeSearch()`, `getStatusSearch()`, `getFileIdSearch()`, `searchTransactionsFileIns()`
- **Controller**: `AutoInvoicePostingController` (`app/Http/Controllers/AutoPost/AutoInvoicePostingController.php`)
  - **Action Methods**: `bulkPostingInvoicesToTempInvoiceTable()`, `bulkPostingInvoicesToTempClaimTable()`, `bulkPostingTempClaimToClaimDetailTable()`, `getConvertedQuantityByMultiUOM()`

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/StockIssueTransList/{id?}` | `StockIssueTransController` | `getStockIssueTransactionList` | `web/api` |
| `GET` | `/StockIssueTransAdd` | `StockIssueTransController` | `getAddStockIssueTransaction` | `web/api` |
| `POST` | `/StockIssueTransAdd` | `StockIssueTransController` | `postAddStockIssueTransaction` | `web/api` |
| `GET` | `/StockIssueTransEdit/{id}/{detailId?}` | `StockIssueTransController` | `getEditStockIssueTransaction` | `web/api` |
| `GET` | `/StockIssueTransCancel/{id}/{detailId?}` | `StockIssueTransController` | `getCancelStockIssueTransaction` | `web/api` |
| `GET` | `/StockIssueTransactionsDownload/{id}` | `StockIssueTransController` | `StockIssueTransactionsDownload` | `web/api` |
| `GET` | `/StockIssueTransactionsPrint/{id}` | `StockIssueTransController` | `StockIssueTransactionsPrint` | `web/api` |
| `GET` | `/getStockIssueTrans` | `StockIssueTransController` | `getStockIssueTransactions` | `web/api` |
| `GET` | `/getStockIssueTransItems` | `StockIssueTransController` | `getStockIssueTransactionItems` | `web/api` |
| `POST` | `/getStockIssueTransItems` | `StockIssueTransController` | `getStockIssueTransactionItems` | `web/api` |
| *...* | *+116 more routes mapped to Transaction Posting* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `PostingMergeClaim` (`app/Services/PostingMergeClaim.php`)
  - Methods: `postMergeClaim()`, `insertMergeClaim()`, `mergeClaimIcdDiagnosis()`, `getAutoPostClaimApp()`, `getLISRISServiceStatus()`
- **Service**: `StockTransaction` (`app/Services/InventoryServices/StockTransaction.php`)
  - Methods: `getTransactionTypeSerialNo()`, `getInstallParamSerialNo()`, `getTransactionSeriesCounter()`, `addHeader()`, `getInventryReasonSerialNo()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: URGENT CARE (ID: URC)

### 1. Module Overview & Navigation Structure
- **Module ID**: `URC`
- **Module Name**: `URGENT CARE`
- **Database Active Status**: Active (`A`)
- **Associated Menus**: URC MASTERS, URC ROOM Installation Parameters, URC ROOM MASTER, URC ROOM TYPE, URGENT CARE, URGENT CARE ROOM MANAGEMENT, URGENT CARE WORKLIST
- **Discovered Sub-functions & Action Page Links** (7 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `URCMSTR` | URC Masters | `#` | URC MASTERS | - |
| `URCROOM` | URC ROOM | `viewURCRoom` | URC ROOM MASTER | - |
| `URCROOMIPA` | URC ROOM INSTALLATION PARAMETERS | `viewURCRoomInstallationParameters` | URC ROOM Installation Parameters | - |
| `URCROOMTYP` | URC ROOM TYPE | `viewURCRoomType` | URC ROOM TYPE | - |
| `URC` | URGENT CARE | `#` | URGENT CARE | - |
| `URCROOMMNG` | URGENT CARE ROOM MANAGEMENT | `ViewUrgentCareRoomManagement` | URGENT CARE ROOM MANAGEMENT | - |
| `URGCARWLST` | URGENT CARE WORK LIST | `ViewUrgentCareWorkList` | URGENT CARE WORKLIST | - |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `URC_` (7 tables)
- **Associated Tables Count**: 10 tables identified
- **Key Tables**: `Patient_Primary_Care_Details`, `Patient_Visit_Anasthesia_Plan_Of_Care`, `Patient_Visit_Caregiver_Education`, `Patient_Visit_Line_Care_Bundle_IV_Cannulation`, `Patient_Visit_Line_Care_Bundle_Insertion`, `Patient_Visit_Line_Care_Bundle_Insertion_Other_Details`, `Patient_Visit_Line_Care_Bundle_Removal`, `Patient_Visit_Line_Care_Bundle_Removal_Other_Details`, `Patient_Visit_PAC_Plan_Of_Care`, `Temp_Pricelist_Nextcare`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

*Table: `Patient_Primary_Care_Details`*
| Column Name | Data Type | Max Length | Nullable | Default |
| :--- | :--- | :--- | :--- | :--- |
| `Patient_Primary_Care_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Visit_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Patient_Basic_Details_Serial_No` | `bigint` | - | NO | - |
| `Branch_Code` | `nvarchar` | 20 | NO | - |
| `Resource_Parent_Serial_No` | `int` | - | YES | - |
| `Primary_Care_Selected` | `varchar` | 1 | NO | ('N') |
| `Sent_To_Mallafi` | `varchar` | 1 | NO | ('N') |
| `This_Is_Deactivated` | `varchar` | 1 | NO | ('N') |
| `Deactivated_User_Id` | `nvarchar` | 40 | YES | - |
| `Deactivated_Date_Time` | `datetime` | - | YES | - |
| `Created_By_User_Id` | `nvarchar` | 40 | NO | - |
| `Created_Date_Time` | `datetime` | - | NO | - |
| *...* | *+16 more columns* | | | |

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Plan_Of_Care` (`app/Models/Patient_Visit_PAC_Plan_Of_Care.php`)
  - **Database Table**: `Patient_Visit_PAC_Plan_Of_Care` | **Primary Key**: `Patient_Visit_PAC_Plan_Of_Care_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRCommonMasters)` [Key/Pivot: `Plan_Of_Care_EMR_Common_Masters_Serial_No`]
- **Model**: `PatientPrimaryCareDetails` (`app/Models/PatientPrimaryCareDetails.php`)
  - **Database Table**: `Patient_Primary_Care_Details` | **Primary Key**: `Patient_Primary_Care_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(ResourceParent)` [Key/Pivot: `Resource_Parent_Serial_No`]

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `UrgentCareRoomManagementController` (`app/Http/Controllers/UrgentCareRoomManagementController.php`)
  - **Action Methods**: `ViewUrgentCareRoomManagement()`, `FilterUrgentCareWaitList()`, `getURCPatientDetailsNotifications()`, `urcRoomDivReload()`, `URCRoomStatusupdate()`, `physicianChangeinURCRoom()`, `changephysicianForVisit()`, `notificationreadedUpdate()`
- **Controller**: `UrgentCareWorkListController` (`app/Http/Controllers/UrgentCareWorkListController.php`)
  - **Action Methods**: `ViewUrgentCareWorkList()`, `FilterUrgentCareWorkList()`, `GetUrgentCareWorkListColumnOrder()`, `UpdateURCPatientTriageCompleted()`, `GetUrgentCareInstParamDet()`, `UrgentCareWorkListCommonAction()`
- **Controller**: `AnaesthesiaCareUnitNursingRecordController` (`app/Http/Controllers/AnaesthesiaCareUnitNursingRecordController.php`)
  - **Action Methods**: RESTful defaults
- **Controller**: `UrgentCareRoomController` (`app/Http/Controllers/UrgentCareRoomController.php`)
  - **Action Methods**: `viewURCRoom()`, `addURCRoom()`, `postURCRoom()`, `editURCRoom()`, `postEditURCRoom()`, `changeStatusURCRoomName()`, `downloadURCRoomName()`, `ProgressNotesTypeNamealreadyExists()`
- **Controller**: `UrgentCareRoomInstallationParametersController` (`app/Http/Controllers/UrgentCareRoomInstallationParametersController.php`)
  - **Action Methods**: `viewURCRoomInstallationParameters()`, `addURCRoomInstallationParameters()`, `postURCRoomInstallationParameters()`, `editURCRoomInstallationParameters()`, `postEditURCRoomInstallationParameters()`, `changeStatusURCRoomInstallationParameters()`, `downloadURCRoomInstallationParameters()`, `getURCRoomInstallationParametersToDelete()`
- **Controller**: `UrgentCareRoomAutoAllocationController` (`app/Http/Controllers/UrgentCareRoomAutoAllocationController.php`)
  - **Action Methods**: `RoomAutoAllocationProcess()`
- *(+3 more controllers handling URGENT CARE)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/emrInitialDayCareSurgery` | `EMRInitialDayCareSurgeryController` | `emrInitialDayCareSurgery` | `web/api` |
| `GET` | `/ViewUrgentCareWorkList/{id?}` | `UrgentCareWorkListController` | `ViewUrgentCareWorkList` | `web/api` |
| `POST` | `/FilterUrgentCareWorkList` | `UrgentCareWorkListController` | `FilterUrgentCareWorkList` | `web/api` |
| `GET` | `/GetUrgentCareWorkListColumnOrder` | `UrgentCareWorkListController` | `GetUrgentCareWorkListColumnOrder` | `web/api` |
| `POST` | `/UrgentCareWorkListCommonAction` | `UrgentCareWorkListController` | `UrgentCareWorkListCommonAction` | `web/api` |
| `GET` | `/RoomAutoAllocationProcessCronTestUrl` | `UrgentCareRoomAutoAllocationController` | `RoomAutoAllocationProcess` | `web/api` |
| `GET` | `/ViewUrgentCareRoomManagement/{id?}` | `UrgentCareRoomManagementController` | `ViewUrgentCareRoomManagement` | `web/api` |
| `POST` | `/FilterUrgentCareWaitList` | `UrgentCareRoomManagementController` | `FilterUrgentCareWaitList` | `web/api` |
| `GET` | `/getURCPatientDetailsNotifications` | `UrgentCareRoomManagementController` | `getURCPatientDetailsNotifications` | `web/api` |
| `GET` | `/urcRoomDivReload` | `UrgentCareRoomManagementController` | `urcRoomDivReload` | `web/api` |
| *...* | *+44 more routes mapped to URGENT CARE* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `PrimarycareService` (`app/Services/PrimarycareService.php`)
  - Methods: `getBranchBasedPrimaryCare()`, `getdemographicMandfield()`, `getInsMethod()`, `getResourceInPrimaryCare()`, `addPrimaryCareDetails()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## 📌 Module: WASEEL INTEGRATION (ID: WAS)

### 1. Module Overview & Navigation Structure
- **Module ID**: `WAS`
- **Module Name**: `WASEEL INTEGRATION`
- **Database Active Status**: Active (`A`)
- **Discovered Sub-functions & Action Page Links** (1 total):
| Function ID | Function Name | Action URL / Page Link | Menu Name | Description |
| :--- | :--- | :--- | :--- | :--- |
| `WASEELING` | WASEEL INTEGRATION | `previous_value` | - | Description of Waseel |

### 2. Associated Database Tables & Prefixes (Deep Data Layer)
- **Dynamic Table Prefixes**: `Waseel_` (1 tables)
- **Associated Tables Count**: 79 tables identified
- **Key Tables**: `Alcohol_Attribute_Values`, `Allergy_Attribute_Values`, `Allergy_Values`, `Bulk_Previous_Day_Visit_SMS`, `CPT_Attribute_Values`, `CSSD_Integration_Details`, `Caffeine_Attribute_Values`, `Chief_Complaint_Attribute_Values`, `Childhood_Illness_Attribute_Values`, `Children_MH_Attribute_Values`, `DSR_All_Attribute_Values`, `Demographic_Attribute_Age_Values`

**Deep Column Schema Details (Data Types, Nullability & Primary Keys):**

### 3. Eloquent Models & Data Architecture
- **Model**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` (`app/Models/Patient_Visit_PAC_Previous_Anaesthesia_History_Details.php`)
  - **Database Table**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details` | **Primary Key**: `Patient_Visit_PAC_Previous_Anaesthesia_History_Details_Serial_No`
  - **Eloquent Relationships**: `belongsTo(EMRSurgeryBookingDetails)` [Key/Pivot: `Surgery_Anaesthesia_Type`]
- **Model**: `PatientVisitServicesStatusValues` (`app/Models/PatientVisitServicesStatusValues.php`)
  - **Database Table**: `Patient_Visit_Services_Status_Values` | **Primary Key**: `Patient_Visit_Services_Status_Values_Serial_No`
- **Model**: `PatientVisitLISServicesParameterStatusValues` (`app/Models/PatientVisitLISServicesParameterStatusValues.php`)
  - **Database Table**: `Patient_Visit_LIS_Services_Parameter_Status_Values` | **Primary Key**: `Patient_Visit_LIS_Services_Parameter_Status_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_LIS_Services_Parameter_Serial_No`, `Visit_Service_Level_Status_Type_Code`, `Updated_By_User_Id`, `Updated_Date_Time`, `Reason_Code`, `Remarks`, `Created_By_User_Id`, `Created_Date_Time`...
- **Model**: `PatientVisitServicesUniversalGroupsCodeValues` (`app/Models/UniversalGroup/PatientVisitServicesUniversalGroupsCodeValues.php`)
  - **Database Table**: `Patient_Visit_Services_Universal_Groups_Code_Values` | **Primary Key**: `Patient_Visit_Services_Universal_Groups_Code_Values_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_Services_Serial_No`, `Universal_Code_Groups_Values_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- **Model**: `EMRCCHPIPreviousTreatmentUsersLink` (`app/Models/CCHPITypes/EMRCCHPIPreviousTreatmentUsersLink.php`)
  - **Database Table**: `EMR_CC_HPI_Previous_Treatment_Users_Link` | **Primary Key**: `EMR_CC_HPI_Previous_Treatment_Users_Link_Serial_No`
  - **Fillable Attributes**: `User_Id`, `EMR_CC_HPI_Previous_Treatment_Serial_No`, `Usage_Frequency`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- **Model**: `PatientVisitCCHPIPreviousTreatment` (`app/Models/CCHPITypes/PatientVisitCCHPIPreviousTreatment.php`)
  - **Database Table**: `Patient_Visit_CC_HPI_Previous_Treatment` | **Primary Key**: `Patient_Visit_CC_HPI_Previous_Treatment_Serial_No`
  - **Fillable Attributes**: `Patient_Visit_CC_HPI_Details_Serial_No`, `EMR_CC_HPI_Previous_Treatment_Serial_No`, `Created_By_User_Id`, `Created_Date_Time`, `Modified_By_User_Id`, `Modified_Date_Time`, `Active_Status`...
- *(+6 additional Eloquent models associated with WASEEL INTEGRATION)*

### 4. Controllers & Action Methods (Business Rules Layer)
- **Controller**: `DefaultTblValuesController` (`app/Http/Controllers/DefaultTblValuesController.php`)
  - **Action Methods**: `defaultValues()`
- **Controller**: `specialityDepartmentVisitServiceStatusValuesController` (`app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`)
  - **Action Methods**: `getspecialityDepartmentVisitServiceStatusValues()`, `alreadyExists()`, `getDownloadspecialityDepartmentVisitServiceStatusValues()`
- **Controller**: `GlobalViewOfUniversalCodeGroupsValuesController` (`app/Http/Controllers/GlobalViewOfUniversalCodeGroupsValuesController.php`)
  - **Action Methods**: `ViewGlobalViewOfUniversalCodeGroupsValues()`, `LoadOptionForUniversalCodeGroupsValuesField()`
- **Controller**: `CSSDIntegrationDetailController` (`app/Http/Controllers/CSSDIntegrationDetailController.php`)
  - **Action Methods**: `ViewCSSDIntegrationDetailPanel()`, `loadCSSDBarCodeSearch()`, `InsertCSSDBarCodeSearchData()`, `AddFavCSSDBarCode()`, `ReportContent()`, `VisSumDocContentCSSD()`, `addCSSDIntegration()`
- **Controller**: `UniversalCodeGroupsValuesController` (`app/Http/Controllers/UniversalCodeGroupsValuesController.php`)
  - **Action Methods**: `getIndex()`, `loadUniversalCodeGroupValues()`, `getAddUniversalCodeGroupValues()`, `CheckSpecialityDepartmentData()`, `EditCheckSpecialityDepartmentData()`, `postAddUniversalCodeGroupValues()`, `getChangeUniversalCodeGroupValuestatus()`, `getDeletUniversalCodeGroupValue()`
- **Controller**: `UniversalCodeValuesController` (`app/Http/Controllers/UniversalCodeValuesController.php`)
  - **Action Methods**: `addUniversalcodeType()`, `postUniversalcodeTypeValues()`, `getUniversalcodeValues()`, `getchangeUniversalcodetypevaluestatus()`, `getDeleteUniversalcodevalues()`, `getEditUniversalCodeValue()`, `downloadUniversalCodeValuesDetails()`, `postEditUniversalcodeValue()`
- *(+4 more controllers handling WASEEL INTEGRATION)*

### 6. Web & API Route URLs
| HTTP Method | Route URI Path | Target Controller | Action Method | Middlewares |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/universalCodeGroupsValues/{id?}` | `UniversalCodeGroupsValuesController` | `getIndex` | `web/api` |
| `GET` | `/loadUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `loadUniversalCodeGroupValues` | `web/api` |
| `GET` | `/CheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `CheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/EditCheckSpecialityDepartmentData` | `UniversalCodeGroupsValuesController` | `EditCheckSpecialityDepartmentData` | `web/api` |
| `GET` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `getAddUniversalCodeGroupValues` | `web/api` |
| `POST` | `/addUniversalCodeGroupValues` | `UniversalCodeGroupsValuesController` | `postAddUniversalCodeGroupValues` | `web/api` |
| `GET` | `/changeUniversalCodeGroupValuestatus/{id}/{status}` | `UniversalCodeGroupsValuesController` | `getChangeUniversalCodeGroupValuestatus` | `web/api` |
| `GET` | `/deletUniversalCodeGroupValue/{id}` | `UniversalCodeGroupsValuesController` | `getDeletUniversalCodeGroupValue` | `web/api` |
| `GET` | `/downloadUniversalcodeGroupValues` | `UniversalCodeGroupsValuesController` | `downloadUniversalcodeGroupValues` | `web/api` |
| `GET` | `/editUniversalcodeGroupValue/{id}` | `UniversalCodeGroupsValuesController` | `getEditUniversalcodeGroupValue` | `web/api` |
| *...* | *+153 more routes mapped to WASEEL INTEGRATION* | | | |

### 7. Services, Repositories & External Integrations
- **Service**: `CAFGeneration` (`app/Services/Waseel/CAFGeneration.php`)
  - Methods: `getClaimCAF()`
- **Service**: `PharmacyEclaim` (`app/Services/Waseel/PharmacyEclaim.php`)
  - Methods: `send()`, `sendBeneficiary()`, `sendCoverage()`, `sendClaimInfo()`, `sendClaimItem()`
- **Service**: `ClaimProcessing` (`app/Services/Waseel/ClaimProcessing.php`)
  - Methods: `ClaimToBeProcess()`, `getReportDetails()`
- **Service**: `WaseelDB` (`app/Services/Waseel/WaseelDB.php`)
  - Methods: `send()`
- **Service**: `Eclaim` (`app/Services/Waseel/Eclaim.php`)
  - Methods: `send()`, `sendBeneficiary()`, `sendCoverage()`, `sendClaimInfo()`, `sendClaimPreAuthDetails()`

### 8. Workflow Architecture & Common Log Patterns
- **Recent Active Error Patterns**: No active critical exceptions logged in `laravel.log` for this module.

---

## ⚙️ Global Workflow Layer (Middlewares, Events & Background Jobs)
### Active Middlewares
- `ValidateSignature` (`app/Http/Middleware/ValidateSignature.php`)
- `VerifyCsrfToken` (`app/Http/Middleware/VerifyCsrfToken.php`)
- `LogActivityMiddleware` (`app/Http/Middleware/LogActivityMiddleware.php`)
- `Authenticate` (`app/Http/Middleware/Authenticate.php`)
- `EncryptCookies` (`app/Http/Middleware/EncryptCookies.php`)
- `RedisFailoverMiddleware` (`app/Http/Middleware/RedisFailoverMiddleware.php`)
- `RedirectIfAuthenticated` (`app/Http/Middleware/RedirectIfAuthenticated.php`)
- `DynamicCors` (`app/Http/Middleware/DynamicCors.php`)
- `LogApiRequestResponse` (`app/Http/Middleware/LogApiRequestResponse.php`)
- `WebApiMiddleware` (`app/Http/Middleware/WebApiMiddleware.php`)
- `SwitchDatabase` (`app/Http/Middleware/SwitchDatabase.php`)
- `PreventBackHistory` (`app/Http/Middleware/PreventBackHistory.php`)
- `OTPCheck` (`app/Http/Middleware/OTPCheck.php`)
- `VerifyReportApi` (`app/Http/Middleware/VerifyReportApi.php`)
- `VerifyXSS` (`app/Http/Middleware/VerifyXSS.php`)
- `TrustProxies` (`app/Http/Middleware/TrustProxies.php`)
- `ValidateApiKeyToken` (`app/Http/Middleware/ValidateApiKeyToken.php`)
- `SkipConvertEmptyMiddleware` (`app/Http/Middleware/SkipConvertEmptyMiddleware.php`)
- `TrustHosts` (`app/Http/Middleware/TrustHosts.php`)
- `PreventRequestsDuringMaintenance` (`app/Http/Middleware/PreventRequestsDuringMaintenance.php`)
- `SecureHeaders` (`app/Http/Middleware/SecureHeaders.php`)
- `TrimStrings` (`app/Http/Middleware/TrimStrings.php`)
- `EncryptPayload` (`app/Http/Middleware/EncryptPayload.php`)

### Events & Listeners Pipeline
- **Event**: `ObservationScheduleChanged` (`app/Events/ObservationScheduleChanged.php`)
- **Event**: `EligibilityStatusChanged` (`app/Events/EligibilityStatusChanged.php`)
- **Event**: `DrugUploadStatusChanged` (`app/Events/DrugUploadStatusChanged.php`)
- **Listener**: `StoreDrugUploadStatusNotification` (`app/Listeners/StoreDrugUploadStatusNotification.php`)
- **Background Job**: `MantysEligibilityCheckStatusCronJob` (`app/Jobs/MantysEligibilityCheckStatusCronJob.php`)
- **Background Job**: `ResourceSpecialitySubDeptInsertion` (`app/Jobs/ResourceSpecialitySubDeptInsertion.php`)
- **Background Job**: `ProcessSchedulerJob` (`app/Jobs/ProcessSchedulerJob.php`)
- **Background Job**: `AppointmentPriorVisitCreateSchedulerJob` (`app/Jobs/AppointmentPriorVisitCreateSchedulerJob.php`)

### Recent Storage Error Patterns (`storage/logs/laravel.log`)
- `[2026-10-08 08:05:42] laravel.EMERGENCY: Unable to create configured logger. Using emergency logger. {"exception":"[object] (Inval`
- `[2026-10-08 08:04:41] laravel.ERROR: The "/var/www/html/himes2/vendor/laravel/framework/src/Illuminate/Foundation/Bootstrap/../../`
- `[2026-10-08 08:05:42] laravel.ERROR: The "/var/www/html/himes2/vendor/laravel/framework/src/Illuminate/Foundation/Bootstrap/../../`
- `[2026-10-08 08:04:57] laravel.ERROR: The "/var/www/html/himes2/vendor/laravel/framework/src/Illuminate/Foundation/Bootstrap/../../`
- `[2026-10-08 08:05:40] laravel.ERROR: The "/var/www/html/himes2/vendor/laravel/framework/src/Illuminate/Foundation/Bootstrap/../../`
- `[2026-10-08 08:05:41] laravel.ERROR: The "/var/www/html/himes2/vendor/laravel/framework/src/Illuminate/Foundation/Bootstrap/../../`
- `[2026-10-08 08:05:41] laravel.EMERGENCY: Unable to create configured logger. Using emergency logger. {"exception":"[object] (Inval`
- `[2026-10-08 08:05:40] laravel.EMERGENCY: Unable to create configured logger. Using emergency logger. {"exception":"[object] (Inval`