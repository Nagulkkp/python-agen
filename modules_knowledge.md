# HIMES Laravel Application Modules Knowledge Base

> Auto-extracted on demand from `/L9/nagul/himes-ai`. Contains verified Controllers, Models, Routes, and Database Table Schemas.

---

## 📌 Module: Appointment

### 1. Controllers
- `app/Http/Controllers/PatientMultiAppointmentController.php`
- `app/Http/Controllers/RegistrationAppointmentController.php`
- `app/Http/Controllers/GlobalViewAppointmentController.php`
- `app/Http/Controllers/AppointmentQstnTypeController.php`
- `app/Http/Controllers/AppointmentDefaultSpecialityController.php`
- `app/Http/Controllers/AppointmentQuestionaryController.php`
- `app/Http/Controllers/RegistrationAppointmentPostController.php`
- `app/Http/Controllers/RegistrationAppointmentPartOneController.php`

### 2. Models & Services
**Models:**
- `app/Models/Appointment.php`
- `app/Models/Patient/PatientVisitAppointment.php`
- `app/Models/Appointment/PatientAppointment.php`
- `app/Models/PatientAppointmentWhatsappNotification.php`
**Services:**
- `app/Services/AppointmentService/RecurringAppointmentService.php`
- `app/Services/AppointmentService/ResourceService.php`
- `app/Services/AppointmentSMS.php`
- `app/Services/AppointmentSMS/PatientPortalAppointmentSMS.php`

### 3. Mapped Web / API Routes
- `routes/controllers/RegistrationAppointment.php:3:Route::get('getSpecialityDepartmentDetails','RegistrationAppointmentPartOneController@getSpecialityDepartmentDetails');`
- `routes/controllers/RegistrationAppointment.php:4:Route::get('getResourceServiceDupParaRecords','RegistrationAppointmentPartOneController@getResourceServiceDupParaRecords');`
- `routes/controllers/RegistrationAppointment.php:5:Route::post('cancelVisitForAppointment/{id?}','RegistrationAppointmentPostController@cancelVisitForAppointment');`
- `routes/controllers/RegistrationAppointment.php:6:Route::get('cancelVisitForAppointmentModal','RegistrationAppointmentPartOneController@cancelVisitForAppointmentModal');`
- `routes/controllers/RegistrationAppointment.php:7:Route::get('loadReferralClinicId','RegistrationAppointmentPartOneController@loadReferralClinicId');`
- `routes/controllers/RegistrationAppointment.php:8:Route::get('loadReferralDoctorId','RegistrationAppointmentPartOneController@loadReferralDoctorId');`
- `routes/controllers/RegistrationAppointment.php:9:Route::get('loadReferralResource','RegistrationAppointmentPartOneController@loadReferralResource');`
- `routes/controllers/RegistrationAppointment.php:10:Route::get('loadReferralClinicResource','RegistrationAppointmentPartOneController@loadReferralClinicResource');`
- `routes/controllers/RegistrationAppointment.php:11:Route::get('removeNewBookedServiceAppointment','RegistrationAppointmentPartOneController@removeNewBookedServiceAppointment');`
- `routes/controllers/RegistrationAppointment.php:12:Route::get('removeAddedService','RegistrationAppointmentPartOneController@removeAddedService');`
- `routes/controllers/RegistrationAppointment.php:13:Route::get('addToVisitBookedAppt','RegistrationAppointmentPostController@addToVisitBookedAppt');`
- `routes/controllers/RegistrationAppointment.php:14:Route::get('getlisdetailsusedornot','RegistrationAppointmentPartOneController@getlisparameterstatuscancelservice');`
- `routes/controllers/RegistrationAppointment.php:15:Route::get('cancelBookedServiceAppointment','RegistrationAppointmentPartOneController@cancelBookedServiceAppointment');`
- `routes/controllers/RegistrationAppointment.php:16:Route::get('loadPartnerCompany','RegistrationAppointmentPartOneController@loadPartnerCompany');`
- `routes/controllers/RegistrationAppointment.php:17:Route::get('getApptDoctors', 'RegistrationAppointmentPartOneController@getDoctors');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `Appointment_Default_Speciality`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Speciality_Code` | nvarchar | YES |
| `Branch_Code` | nvarchar | YES |
| `Is_Specilaity_Default` | nvarchar | YES |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | YES |

#### Table: `Appointment_Merge_Counter`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Appointment_Merge_Counter_Serial_No` | bigint | NO |
| `Patient_Basic_Details_Serial_No` | bigint | NO |
| `Merge_Appointment_Start_Date` | date | NO |
| `Merge_Appointment_End_Date` | date | NO |
| `Merge_Appointment_Start_Time` | time | NO |
| `Merge_Appointment_End_Time` | time | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |

#### Table: `appointment_sources`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `appointment_source_serial_no` | bigint | NO |
| `appointment_source_code` | nvarchar | NO |
| `appointment_source_name` | nvarchar | YES |
| `appointment_type` | nvarchar | NO |
| `created_at` | datetime | YES |
| `updated_at` | datetime | YES |
| `Active_Status` | varchar | YES |

#### Table: `Appointment_Status_Type`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Appointment_Status_Type_Code` | nvarchar | NO |
| `Appointment_Status_Type_Name` | nvarchar | NO |
| `Max_Appointments_Per_Day` | smallint | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |

---

## 📌 Module: Registration

### 1. Controllers
- `app/Http/Controllers/GlobalViewRegistrationController.php`
- `app/Http/Controllers/DRP/QuickRegistrationOperationController.php`
- `app/Http/Controllers/DRP/QuickRegistrationController.php`
- `app/Http/Controllers/ZEO/ZeoRegistrationController.php`
- `app/Http/Controllers/TherapyRegistrationPaymentController.php`
- `app/Http/Controllers/RegistrationPackageController.php`
- `app/Http/Controllers/RegistrationAppointmentController.php`
- `app/Http/Controllers/PatientRegistrationImportController.php`

### 2. Models & Services
**Models:**
- `app/Models/Registration_Common_Masters.php`
- `app/Models/Registration/PatientVisitInsuranceCardDetail.php`
- `app/Models/Registration/PatientVisitResources.php`
- `app/Models/Registration/PatientVisitIODDetails.php`
- `app/Models/Registration/PatientVisitAdmissionFormDetails.php`
- `app/Models/Registration/PatientInsuranceCardDetail.php`
**Services:**
- `app/Services/PODRegistrationService.php`
- `app/Services/physioOrder/TheraphyRegistrationService.php`
- `app/Services/RegistrationCommonMasterService.php`
- `app/Services/Registration/MRNVisitGenerationService.php`

### 3. Mapped Web / API Routes
- `routes/controllers/RegistrationAppointment.php:3:Route::get('getSpecialityDepartmentDetails','RegistrationAppointmentPartOneController@getSpecialityDepartmentDetails');`
- `routes/controllers/RegistrationAppointment.php:4:Route::get('getResourceServiceDupParaRecords','RegistrationAppointmentPartOneController@getResourceServiceDupParaRecords');`
- `routes/controllers/RegistrationAppointment.php:5:Route::post('cancelVisitForAppointment/{id?}','RegistrationAppointmentPostController@cancelVisitForAppointment');`
- `routes/controllers/RegistrationAppointment.php:6:Route::get('cancelVisitForAppointmentModal','RegistrationAppointmentPartOneController@cancelVisitForAppointmentModal');`
- `routes/controllers/RegistrationAppointment.php:7:Route::get('loadReferralClinicId','RegistrationAppointmentPartOneController@loadReferralClinicId');`
- `routes/controllers/RegistrationAppointment.php:8:Route::get('loadReferralDoctorId','RegistrationAppointmentPartOneController@loadReferralDoctorId');`
- `routes/controllers/RegistrationAppointment.php:9:Route::get('loadReferralResource','RegistrationAppointmentPartOneController@loadReferralResource');`
- `routes/controllers/RegistrationAppointment.php:10:Route::get('loadReferralClinicResource','RegistrationAppointmentPartOneController@loadReferralClinicResource');`
- `routes/controllers/RegistrationAppointment.php:11:Route::get('removeNewBookedServiceAppointment','RegistrationAppointmentPartOneController@removeNewBookedServiceAppointment');`
- `routes/controllers/RegistrationAppointment.php:12:Route::get('removeAddedService','RegistrationAppointmentPartOneController@removeAddedService');`
- `routes/controllers/RegistrationAppointment.php:13:Route::get('addToVisitBookedAppt','RegistrationAppointmentPostController@addToVisitBookedAppt');`
- `routes/controllers/RegistrationAppointment.php:14:Route::get('getlisdetailsusedornot','RegistrationAppointmentPartOneController@getlisparameterstatuscancelservice');`
- `routes/controllers/RegistrationAppointment.php:15:Route::get('cancelBookedServiceAppointment','RegistrationAppointmentPartOneController@cancelBookedServiceAppointment');`
- `routes/controllers/RegistrationAppointment.php:16:Route::get('loadPartnerCompany','RegistrationAppointmentPartOneController@loadPartnerCompany');`
- `routes/controllers/RegistrationAppointment.php:17:Route::get('getApptDoctors', 'RegistrationAppointmentPartOneController@getDoctors');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `PA_Patient_Basic_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `PA_Patient_Basic_Details_Serial_No` | bigint | NO |
| `Salutation_Code` | nvarchar | NO |
| `Patient_First_Name` | nvarchar | NO |
| `Patient_Middle_Name` | nvarchar | YES |
| `Patient_Last_Name` | nvarchar | YES |
| `Patient_DOB` | date | YES |
| `Age_Category` | nvarchar | YES |
| `Patient_Age_Days` | smallint | YES |
| `Patient_Age_Months` | smallint | YES |
| `Patient_Age_Years` | smallint | YES |

#### Table: `Paitent_Registration_Module_Details_Update`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Paitent_Registration_Module_Details_Update_Serial_No` | bigint | NO |
| `Patient_Basic_Details_Serial_No` | bigint | NO |
| `JSON_Data` | varchar | YES |
| `Authorize_My_Registration` | varchar | NO |
| `Regulations` | varchar | NO |
| `Appointment_Reminder` | varchar | NO |
| `Patient_Signature` | varchar | YES |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |

#### Table: `Patient_Basic_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Patient_Basic_Details_Serial_No` | bigint | NO |
| `Salutation_Code` | nvarchar | NO |
| `Patient_First_Name` | nvarchar | NO |
| `Patient_Middle_Name` | nvarchar | YES |
| `Patient_Last_Name` | nvarchar | YES |
| `Patient_DOB` | date | YES |
| `Age_Category` | nvarchar | YES |
| `Patient_Age_Days` | smallint | YES |
| `Patient_Age_Months` | smallint | YES |
| `Patient_Age_Years` | smallint | NO |

#### Table: `patient_basic_details_21052021`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Patient_Basic_Details_Serial_No` | bigint | NO |
| `Salutation_Code` | nvarchar | NO |
| `Patient_First_Name` | nvarchar | NO |
| `Patient_Middle_Name` | nvarchar | YES |
| `Patient_Last_Name` | nvarchar | YES |
| `Patient_DOB` | date | YES |
| `Age_Category` | nvarchar | YES |
| `Patient_Age_Days` | smallint | YES |
| `Patient_Age_Months` | smallint | YES |
| `Patient_Age_Years` | smallint | NO |

---

## 📌 Module: Billing

### 1. Controllers
- `app/Http/Controllers/PatientBillingBackendController.php`
- `app/Http/Controllers/BranchBasedPurchaseInvoiceController.php`
- `app/Http/Controllers/GlobalViewRefundBillingController.php`
- `app/Http/Controllers/BranchPriceListManagementController.php`
- `app/Http/Controllers/PackageInvoiceController.php`
- `app/Http/Controllers/PatientBillingGetController.php`
- `app/Http/Controllers/GlobalViewPatientBillingController.php`
- `app/Http/Controllers/PatientBillreceiptcounterController.php`

### 2. Models & Services
**Models:**
- `app/Models/PatientVisitInventoryBilling.php`
- `app/Models/Patient/PatientBillHeader.php`
- `app/Models/Billing/BillingDeletedLog.php`
**Services:**
- `app/Services/InvoiceService.php`
- `app/Services/PatientBillingServices.php`
- `app/Services/GlobalViewBillingService.php`
- `app/Services/GenerateInvoiceClosedPostedStatus.php`

### 3. Mapped Web / API Routes
- `routes/controllers/EMRInventoryConsumption.php:27:Route::get('InventoyBillingVisitPatientSearch','EMRInventoryConsumptionController@InventoyBillingVisitPatientSearch');`
- `routes/controllers/EMRInventoryConsumption.php:28:Route::get('fetchInvBillDetailBasedOnVisit','EMRInventoryConsumptionController@fetchInvBillDetailBasedOnVisit');`
- `routes/controllers/EMRInventoryConsumption.php:29:Route::get('InventoyBillingInvoicePatientSearch','EMRInventoryConsumptionController@InventoyBillingInvoicePatientSearch');`
- `routes/controllers/EMRInventoryConsumption.php:30:Route::get('getInvoiceClosedPostedStatus','EMRInventoryConsumptionController@getInvoiceClosedPostedStatus');`
- `routes/controllers/RegistrationAppointment.php:51:Route::get('CheckServiceToCurrentVisitbillinggrid','RegistrationAppointmentPartOneController@CheckServiceToCurrentVisitbillinggrid');`
- `routes/controllers/PurchaseCommon.php:13:Route::post('getBillingShipmentDetail','PurchaseCommonController@getBillingShipmentDetail');`
- `routes/controllers/PurchaseCommon.php:14:Route::post('getBillingShipmentDetailById','PurchaseCommonController@getBillingShipmentDetailById');`
- `routes/controllers/BillDeposite.php:3:Route::get('billingDeposit/{id?}','BillDepositeController@getIndex');`
- `routes/controllers/BillDeposite.php:4:Route::get('billdepositepatientsearchname','BillDepositeController@getBillDepositepatientsearchname');`
- `routes/controllers/BillDeposite.php:5:Route::get('billdepositepatientsearchdetails','BillDepositeController@getBillDepositePatientSearch');`
- `routes/controllers/BillDeposite.php:6:Route::get('billdepositepatientvisitdetails','BillDepositeController@getbilldepositepatientvisitdetails');`
- `routes/controllers/BillDeposite.php:7:Route::get('billAddRowMore','BillDepositeController@getbillAddRowMore');`
- `routes/controllers/BillDeposite.php:8:Route::get('EditbillAddRowMore','BillDepositeController@getEditbillAddRowMore');`
- `routes/controllers/BillDeposite.php:9:Route::get('addBillDeposit','BillDepositeController@getAddBillDeposite');`
- `routes/controllers/BillDeposite.php:10:Route::get('addBillDeposit/{pbdno}/{pvbdno}','BillDepositeController@getAddBillDeposite');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `Interim_Patient_Bill_Header`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Interim_Patient_Bill_Header_Serial_No` | bigint | NO |
| `Branch_Code` | nvarchar | NO |
| `Patient_Visit_Basic_Details_Serial_No` | bigint | NO |
| `Interim_Permanent_Invoice_No` | bigint | NO |
| `Interim_Bill_Cancellation_Flag` | nvarchar | NO |
| `Interim_Bill_Cancellation_User_Id` | nvarchar | YES |
| `Interim_Bill_Cancellation_Date_Time` | datetime | YES |
| `Interim_Bill_Is_Finalized` | nvarchar | NO |
| `Interim_Bill_Gross_Value` | decimal | NO |
| `Interim_Bill_Net_Value` | decimal | NO |

#### Table: `Interim_Patient_Bill_Header_Detail`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Interim_Patient_Bill_Header_Detail_Serial_No` | bigint | NO |
| `Interim_Patient_Bill_Header_Serial_No` | bigint | NO |
| `Bill_Service_Type` | nvarchar | NO |
| `Patient_Visit_Services_Serial_No` | bigint | YES |
| `Patient_Visit_Resource_Serial_No` | bigint | YES |
| `Item_Master_Serial_No` | bigint | YES |
| `Item_UOM_Serial_No` | int | YES |
| `Service_USSDB_Serial_No` | bigint | YES |
| `Service_Serial_No` | bigint | YES |
| `Resource_Serial_No` | bigint | YES |

#### Table: `PA_Patient_Visit_Services`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `PA_Patient_Visit_Services_Serial_No` | bigint | NO |
| `PA_Patient_Visit_Basic_Details_Serial_No` | bigint | NO |
| `Service_USSDB_Serial_No` | bigint | NO |
| `Service_Cancellation_Flag` | nvarchar | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |
| `Service_Insurance_Remarks` | nvarchar | YES |

#### Table: `PA_Patient_Visit_Services_Universal_Code_Values`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `PA_Patient_Visit_Services_Universal_Code_Values_Serial_No` | bigint | NO |
| `PA_Patient_Visit_Services_Serial_No` | bigint | NO |
| `Universal_Code_Groups_Serial_No` | bigint | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |

---

## 📌 Module: Prior Approval

### 1. Controllers
- `app/Http/Controllers/InsurancePlanPriorApprovalController.php`
- `app/Http/Controllers/priorVisit/PriorVisitPriorApprovalLogController.php`

### 2. Models & Services
**Models:**
- `app/Models/Insurance/PatientVisitInsurancePlanExcludedPriorApprovalServices.php`
**Services:**
- `app/Services/PharmacyOrder/PharmacyPriorApprovalService.php`

### 3. Mapped Web / API Routes
- `routes/controllers/RegistrationInsurance.php:8:Route::get('getPlanPriorApprovalServiceDetails','RegistrationInsuranceController@getPlanPriorApprovalServiceDetails');`
- `routes/controllers/PriorAuthorizationGlobalViewNew.php:27:Route::get('getInsPriorApprovalStatus','PriorAuthorizationGlobalViewNewController@getInsPriorApprovalStatus');`
- `routes/routes.php:2154:Route::get('addInsurancePlanPriorApproval', 'InsurancePlanPriorApprovalController@getAddInsurancePlanPriorApproval');`
- `routes/routes.php:2155:Route::post('addInsurancePlanPriorApproval', 'InsurancePlanPriorApprovalController@postAddInsurancePlanPriorApproval');`
- `routes/routes.php:2156:Route::get('insuranceplanExcludedApprovalServices/{id?}', 'InsurancePlanPriorApprovalController@getViewInsurancePlanPriorApproval');`
- `routes/routes.php:2157:Route::get('editStatusInsurancePlanPriorApproval/{id?}', 'InsurancePlanPriorApprovalController@getEditStatusInsurancePlanPriorApproval');`
- `routes/routes.php:2158:Route::get('deleteInsurancePlanPriorApproval/{id?}', 'InsurancePlanPriorApprovalController@getDeleteInsurancePlanPriorApproval');`
- `routes/routes.php:2159:Route::get('editInsurancePlanPriorApproval/{id?}', 'InsurancePlanPriorApprovalController@getEditInsurancePlanPriorApproval');`
- `routes/routes.php:2160:Route::get('viewDetailInsurancePlanPriorApproval/{id?}', 'InsurancePlanPriorApprovalController@getViewDetailInsurancePlanPriorApproval');`
- `routes/routes.php:2161:Route::post('editInsurancePlanPriorApproval', 'InsurancePlanPriorApprovalController@postEditInsurancePlanPriorApproval');`
- `routes/routes.php:2162:Route::get('downloadInsurancePlanPriorApproval', 'InsurancePlanPriorApprovalController@getDownloadInsurancePlanPriorApproval');`
- `routes/routes.php:10600:Route::get('checkPriorApprovalVisitForPhysio','physiotherapyOrderController@checkPriorApprovalVisitForPhysio');`
- `routes/routes.php:10870:Route::get('createPriorApprovalForTherapy', 'PTWorkflowServiceController@createPriorApprovalForTherapy');`
- `routes/priorVisit/priorVisitModule.php:86:Route::get('checkServicePriorApprovalStatus','priorVisit\PriorVisitController@checkServicePriorApprovalStatus');`
- `routes/priorVisit/priorVisitModule.php:108:Route::get('getPVPASubmissionHistoryDetails', 'priorVisit\PriorVisitPriorApprovalLogController@getPVPASubmissionHistoryDetails');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `Insurance_Plan_Excluded_Prior_Approval_Services`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Insurance_Plan_Excluded_Prior_Approval_Services_Serial_No` | bigint | NO |
| `Insurance_Plan_Department_CoverSerial_No` | bigint | NO |
| `Is_It_Service_Resource_Drug` | nvarchar | NO |
| `Service_Serial_No` | bigint | YES |
| `Resource_Serial_No` | bigint | YES |
| `Resource_Type_Code` | nvarchar | YES |
| `Item_Drug_Link_Serial_No` | bigint | YES |
| `Is_Excluded_Prior_Approval_Required` | nvarchar | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |

#### Table: `Patient_Visit_Insurance_Plan_Excluded_Prior_Approval_Services`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Patient_Visit_Insurance_Plan_Excluded_Prior_Approval_Services_Serial_No` | bigint | NO |
| `Patient_Visit_Insurance_Plan_Department_Cover_Serial_No` | bigint | NO |
| `Is_It_Service_Resource_Drug` | nvarchar | NO |
| `Service_Serial_No` | bigint | YES |
| `Resource_Serial_No` | bigint | YES |
| `Resource_Type_Code` | nvarchar | YES |
| `Item_Drug_Link_Serial_No` | bigint | YES |
| `Is_Excluded_Prior_Approval_Required` | nvarchar | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |

---

## 📌 Module: Prior Visit

### 1. Controllers
- `app/Http/Controllers/EMRVisitEntryController.php`
- `app/Http/Controllers/VisitEncounterLinkController.php`
- `app/Http/Controllers/PatientVisitServiceTestController.php`
- `app/Http/Controllers/specialityDepartmentVisitServiceStatusValuesController.php`
- `app/Http/Controllers/EMRPanelPAServiceMovedCurrentVisitController.php`
- `app/Http/Controllers/EMRVisitEntryPanelController.php`
- `app/Http/Controllers/VisitServiceLevelStatusTypeController.php`
- `app/Http/Controllers/ConsentFormPatientVisitController.php`

### 2. Models & Services
**Models:**
- `app/Models/UniversalGroup/PatientVisitServicesUniversalGroupsCodeValues.php`
- `app/Models/CCHPITypes/PatientVisitCCHPILocations.php`
- `app/Models/CCHPITypes/PatientVisitCCHPIOnset.php`
- `app/Models/CCHPITypes/PatientVisitCCHPISeverity.php`
- `app/Models/CCHPITypes/PatientVisitCCHPIChiefComplaintFavourites.php`
- `app/Models/CCHPITypes/PatientVisitCCHPIPreviousTreatment.php`
**Services:**
- `app/Services/OPReferralPAToClinicVisit.php`
- `app/Services/VisitEncounterLinkService.php`
- `app/Services/PatientVisitDischargeSummaryDetailService.php`
- `app/Services/CreateOtherBranchOpReferralVisitService.php`

### 3. Mapped Web / API Routes
- `routes/controllers/EMRInventoryConsumption.php:27:Route::get('InventoyBillingVisitPatientSearch','EMRInventoryConsumptionController@InventoyBillingVisitPatientSearch');`
- `routes/controllers/EMRInventoryConsumption.php:28:Route::get('fetchInvBillDetailBasedOnVisit','EMRInventoryConsumptionController@fetchInvBillDetailBasedOnVisit');`
- `routes/controllers/RegistrationAppointment.php:5:Route::post('cancelVisitForAppointment/{id?}','RegistrationAppointmentPostController@cancelVisitForAppointment');`
- `routes/controllers/RegistrationAppointment.php:6:Route::get('cancelVisitForAppointmentModal','RegistrationAppointmentPartOneController@cancelVisitForAppointmentModal');`
- `routes/controllers/RegistrationAppointment.php:13:Route::get('addToVisitBookedAppt','RegistrationAppointmentPostController@addToVisitBookedAppt');`
- `routes/controllers/RegistrationAppointment.php:31:Route::post('appointQuesVisitServices', 'RegistrationAppointmentPostController@appointQuesVisitServices');`
- `routes/controllers/RegistrationAppointment.php:39:Route::get('checkAppointmentServiceForCurVisit','RegistrationAppointmentPostController@checkAppointmentServiceForCurVisit');`
- `routes/controllers/RegistrationAppointment.php:41:Route::post('UpdateVisitDoctorType','RegistrationAppointmentPostController@UpdateVisitDoctorType');`
- `routes/controllers/RegistrationAppointment.php:42:Route::post('cancelVisit','RegistrationAppointmentPostController@cancelVisit');`
- `routes/controllers/RegistrationAppointment.php:45:Route::post('addAppointmentServiceToVisit','RegistrationAppointmentPostController@addAppointmentServiceToVisit');`
- `routes/controllers/RegistrationAppointment.php:46:Route::post('addAppointmentServiceToVisitQck','RegistrationAppointmentPostController@addAppointmentServiceToVisitQck');`
- `routes/controllers/RegistrationAppointment.php:47:Route::get('addToVisitBookedApptQCK','RegistrationAppointmentPostController@addToVisitBookedApptQCK');`
- `routes/controllers/RegistrationAppointment.php:51:Route::get('CheckServiceToCurrentVisitbillinggrid','RegistrationAppointmentPartOneController@CheckServiceToCurrentVisitbillinggrid');`
- `routes/controllers/RisWorkList.php:32:Route::get('refEntityNotesByVisitIdRIS', 'RisWorkListController@refEntityNotesByVisitris');`
- `routes/controllers/PatientAppointment.php:20:Route::get('PriorVisitAppointmentDetails','PatientAppointmentController@PriorVisitAppointmentDetails');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `PA_Patient_Visit_Basic_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `PA_Patient_Visit_Basic_Details_Serial_No` | bigint | NO |
| `PA_Patient_Basic_Details_Serial_No` | bigint | NO |
| `PA_Permanent_Visit_No` | bigint | NO |
| `Patient_Payment_Type_Serial_No` | bigint | YES |
| `Visit_Encounter_Type_Serial_No` | int | YES |
| `Has_Patient_Checked_In` | nvarchar | NO |
| `Patient_Checked_In_Date_Time` | datetime | YES |
| `Is_Patient_Visit_Registered` | nvarchar | NO |
| `Patient_Visit_Registered_Date_Time` | datetime | YES |
| `Branch_Code` | nvarchar | NO |

#### Table: `PA_Patient_Visit_Insurance_Card_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `PA_Patient_Visit_Insurance_Card_Details_Serial_No` | bigint | NO |
| `PA_Patient_Visit_Basic_Details_Serial_No` | bigint | NO |
| `Insurance_Card_No` | nvarchar | NO |
| `Insurance_Card_Effective_Date` | date | YES |
| `Insurance_Card_Expire_Date` | date | YES |
| `Insurance_Card_Front_Image_Path` | nvarchar | YES |
| `Insurance_Card_Back_Image_Path` | nvarchar | YES |
| `Insurance_Company_Branch_Serial_No` | int | NO |
| `Insurance_Plan_Serial_No` | int | NO |
| `Insurance_Associate_Company_Serial_No` | int | YES |

#### Table: `PA_Patient_Visit_Referral_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `PA_Patient_Visit_Referral_Details_Serial_No` | bigint | NO |
| `PA_Patient_Visit_Basic_Details_Serial_No` | bigint | NO |
| `Referral_Entity_Serial_No` | bigint | YES |
| `Referral_Entity_Resource_Serial_No` | bigint | YES |
| `Referral_Entity_Patient_ID` | varchar | YES |
| `Referral_Entity_Resource_Note` | varchar | YES |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |

#### Table: `Patient_Visit_Basic_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Patient_Visit_Basic_Details_Serial_No` | bigint | NO |
| `Patient_Basic_Details_Serial_No` | bigint | NO |
| `Patient_Payment_Type_Serial_No` | bigint | NO |
| `Visit_Encounter_Type_Serial_No` | int | YES |
| `Visit_Start_Encounter_Type_Serial_No` | int | YES |
| `Installation_Parameters_Serial_No` | int | NO |
| `Is_It_Walk_In_Patient_Visit` | nvarchar | NO |
| `Is_It_Emergency_Patient_Visit` | nvarchar | NO |
| `Visible_Identification_Marks` | nvarchar | YES |
| `Is_Patient_Pregnant` | nvarchar | NO |

---

## 📌 Module: EMR

### 1. Controllers
- `app/Http/Controllers/EMRVisitEntryController.php`
- `app/Http/Controllers/EMRServiceAdditionController.php`
- `app/Http/Controllers/EMRPprescriptionController.php`
- `app/Http/Controllers/EMRCaseLoadColorIdentificationController.php`
- `app/Http/Controllers/EmrRadiologyReportController.php`
- `app/Http/Controllers/EmrVitalSwallowingController.php`
- `app/Http/Controllers/EMRVaccineDetailsController.php`
- `app/Http/Controllers/EMRQuestionnaireAssessmentController.php`

### 2. Models & Services
**Models:**
- `app/Models/CCHPITypes/EMRCCHPIDuration.php`
- `app/Models/CCHPITypes/EMRCCHPIPreviousTreatmentUsersLink.php`
- `app/Models/CCHPITypes/EMRCCHPIAssociatedSymptoms.php`
- `app/Models/CCHPITypes/EMRCCHPIQuality.php`
- `app/Models/CCHPITypes/EMRCCHPIContextUsersLink.php`
- `app/Models/CCHPITypes/EMRCCHPISeverityUsersLink.php`
**Services:**
- `app/Services/EMRPatientHealthQuestionnaireService.php`
- `app/Services/EMRDiagnosisFilterService.php`
- `app/Services/EMRFormAssemblyService.php`
- `app/Services/CommonEMRService.php`

### 3. Mapped Web / API Routes
- `routes/controllers/EMRInventoryConsumption.php:3:Route::get('viewEMRInventoryConsumption/{id?}/{type?}','EMRInventoryConsumptionController@getviewEMRInventoryConsumption');`
- `routes/controllers/EMRInventoryConsumption.php:4:Route::get('Department/{id?}','EMRInventoryConsumptionController@getDepartment'); `
- `routes/controllers/EMRInventoryConsumption.php:5:Route::get('SubDepartment/{id?}','EMRInventoryConsumptionController@getSubDept');`
- `routes/controllers/EMRInventoryConsumption.php:6:Route::get('StockLoct/{id?}','EMRInventoryConsumptionController@getStockLoct');`
- `routes/controllers/EMRInventoryConsumption.php:7:Route::get('Resources/{id?}','EMRInventoryConsumptionController@getResources');`
- `routes/controllers/EMRInventoryConsumption.php:8:Route::get('Speciality/{id?}','EMRInventoryConsumptionController@getSpeciality');`
- `routes/controllers/EMRInventoryConsumption.php:9:Route::get('ConServices/{id?}','EMRInventoryConsumptionController@getServices');`
- `routes/controllers/EMRInventoryConsumption.php:10:Route::post('ItemDescription','EMRInventoryConsumptionController@getItemDescription');`
- `routes/controllers/EMRInventoryConsumption.php:11:Route::post('Barcode','EMRInventoryConsumptionController@getBarcode');`
- `routes/controllers/EMRInventoryConsumption.php:12:Route::post('ConsumptionItems','EMRInventoryConsumptionController@ProcessOnConsumptionItems');`
- `routes/controllers/EMRInventoryConsumption.php:13:Route::post('AddInvConsumptionItems','EMRInventoryConsumptionController@PostConsumptionItems');`
- `routes/controllers/EMRInventoryConsumption.php:14:Route::post('RemarkPopup/{id?}','EMRInventoryConsumptionController@RemarkPopup');`
- `routes/controllers/EMRInventoryConsumption.php:15:Route::post('DeletePopup/{sNo?}','EMRInventoryConsumptionController@DeletePopup');`
- `routes/controllers/EMRInventoryConsumption.php:16:Route::post('DeleteConsumption/{sNo?}','EMRInventoryConsumptionController@PostDeleteInvConsumption');`
- `routes/controllers/EMRInventoryConsumption.php:17:Route::post('ReasonByConsumption','EMRInventoryConsumptionController@getConsumptionCancelReason');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `Branch_Based_EMR_Ordered_Settings`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Branch_Based_EMR_Ordered_Settings_Serial_No` | int | NO |
| `Branch_Code` | nvarchar | NO |
| `Department_Code` | nvarchar | NO |
| `To_Be_Ordered` | nvarchar | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |

#### Table: `Branch_Based_EMR_Panel_Report`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Branch_Code` | nvarchar | NO |
| `Panel_Serial_No` | smallint | NO |
| `Order_Sequence` | smallint | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |
| `Branch_Based_EMR_Panel_Report_Serial_No` | bigint | NO |
| `Notes_Required` | nvarchar | NO |

#### Table: `Branch_Based_EMR_Panel_Report_Sub_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Branch_Based_EMR_Panel_Report_Sub_Details_Serial_No` | bigint | NO |
| `Branch_Based_EMR_Panel_Report_Serial_No` | bigint | NO |
| `Sub_Panels_Serial_No` | smallint | NO |
| `Order_Sequence` | smallint | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |

#### Table: `Claim_EMR_Detail`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Claim_EMR_Detail_ID` | int | NO |
| `Visit_ID` | int | NO |
| `Bill_ID` | int | NO |
| `Chief_Complaint` | nvarchar | YES |
| `BP_Systolic` | varchar | YES |
| `BP_Diastolic` | varchar | YES |
| `Deleted` | char | YES |
| `Created_By` | nvarchar | YES |
| `Created_DateTime` | datetime | YES |
| `Modified_By` | nvarchar | YES |

---

## 📌 Module: Credit Note

### 1. Controllers
- `app/Http/Controllers/GlobalViewRefundBillingController.php`
- `app/Http/Controllers/RefundReportController.php`
- `app/Http/Controllers/SupplierDebitCreditNoteController.php`
- `app/Http/Controllers/DebitCreditNoteController.php`
- `app/Http/Controllers/PharmacyRefundBillController.php`
- `app/Http/Controllers/GlobalViewCreditNoteController.php`
- `app/Http/Controllers/BranchBasedCreditNoteController.php`
- `app/Http/Controllers/refundbillingController.php`

### 2. Models & Services
**Services:**
- `app/Services/CreditNote.php`
- `app/Services/CreditNoteServices/CreditNoteDetails.php`

### 3. Mapped Web / API Routes
- `routes/controllers/DebitCreditNote.php:3:Route::get('getAllPatientSearchdebcredit','DebitCreditNoteController@searchPatientDetails');`
- `routes/controllers/DebitCreditNote.php:4:Route::get('debitcreditAddRowMore','DebitCreditNoteController@getdebitcreditAddRowMore');`
- `routes/controllers/DebitCreditNote.php:5:Route::get('adddebitCreditNote', 'DebitCreditNoteController@getDebitCreditNote');`
- `routes/controllers/DebitCreditNote.php:6:Route::get('debitCreditNote/{id?}','DebitCreditNoteController@getdbnote');`
- `routes/controllers/DebitCreditNote.php:7:Route::get('billdebitcreditpatientvisitdetails','DebitCreditNoteController@getPatientdepositepatientvisitdetails');`
- `routes/controllers/DebitCreditNote.php:8:Route::get('billdebitcreditpatientinvoicedetails','DebitCreditNoteController@getPatientdepositepatientinvoicedetails');`
- `routes/controllers/DebitCreditNote.php:9:Route::get('billdebitcreditservicevisitdetails','DebitCreditNoteController@getPatientservicevisitdetails');`
- `routes/controllers/DebitCreditNote.php:10:Route::get('editbilldebitcreditservicevisitdetails','DebitCreditNoteController@getPatienteditservicevisitdetail');`
- `routes/controllers/DebitCreditNote.php:11:Route::get('debitadd','DebitCreditNoteController@getdebitcreditadd');`
- `routes/controllers/DebitCreditNote.php:12:Route::get('editdebitCreditNote/{id?}','DebitCreditNoteController@getEditDebitCredit');`
- `routes/controllers/DebitCreditNote.php:13:Route::get('ebilldebitcreditpatientvisitdetails','DebitCreditNoteController@geteditPatientdebcreditpatientvisitdetails');`
- `routes/controllers/DebitCreditNote.php:14:Route::get('ebilldebitcreditpatientinvoicedetails','DebitCreditNoteController@geteditPatientdepositepatientinvoicedetails');`
- `routes/controllers/DebitCreditNote.php:15:Route::get('ebilldebitcreditservicevisitdetails','DebitCreditNoteController@geteditPatientservicevisitdetails');`
- `routes/controllers/DebitCreditNote.php:16:Route::get('editappenddebitcreditservicevisitdetails','DebitCreditNoteController@geteditappendservicevisitdetails');`
- `routes/controllers/DebitCreditNote.php:17:Route::get('addrowdebitcreditappend','DebitCreditNoteController@getaddrowdebitcreditappend');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `Branch_Based_Credit_Note`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Group_Code` | nvarchar | YES |
| `Company_Code` | nvarchar | YES |
| `Branch_Code` | nvarchar | NO |
| `Credit_Note_Invoice_Invoice_No` | bigint | NO |
| `Credit_Note_Invoice_No_Range_Start` | bigint | NO |
| `Credit_Note_Invoice_No_Range_End` | bigint | NO |
| `Credit_Note_Invoice_Prefix_Name` | varchar | YES |
| `Created_By_User_ID` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_ID` | nvarchar | NO |

#### Table: `Paitent_Package_Credit_Note_Bill_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Paitent_Package_Credit_Note_Bill_Details_Serial_No` | bigint | NO |
| `Paitent_Credit_Note_Bill_Details_Serial_No` | bigint | NO |
| `Patient_Packaged_Avail_Serial_No` | bigint | NO |
| `Package_Credit_Amount_From_Bill_Details` | decimal | YES |
| `Package_Credit_Tax_Amount` | decimal | YES |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |

#### Table: `Patient_Credit_Note_Bill_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Paitent_Credit_Note_Bill_Details_Serial_No` | bigint | NO |
| `Patient_Credit_Note_Details_Serial_No` | bigint | YES |
| `Patient_Basic_Details_Serial_No` | bigint | YES |
| `Patient_Bill_Header_Serial_No` | bigint | YES |
| `Patient_Share_Bill_Header_From_Invoice` | decimal | YES |
| `Credit_Amount_From_Invoice` | decimal | YES |
| `Balance_Credit_Amount_From_Invoice` | decimal | YES |
| `Bill_Header_Remarks` | nvarchar | YES |
| `Patient_Bill_Detail_Services_Packages_Resources_Drugs_Serial_No` | bigint | YES |
| `Patient_Share_Bill_Header_Details_From_Bill_Details` | decimal | YES |

#### Table: `Patient_Credit_Note_Details`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Patient_Credit_Note_Details_Serial_No` | bigint | NO |
| `Patient_Basic_Details_Serial_No` | bigint | YES |
| `Patient_Bill_Header_Serial_No` | bigint | YES |
| `Permanent_Credit_Note_Invoice_No` | bigint | YES |
| `Created_By_User_ID` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_ID` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | char | NO |
| `Type` | char | YES |

---

## 📌 Module: Masters

### 1. Controllers
- `app/Http/Controllers/ServiceTestController.php`
- `app/Http/Controllers/EMRServiceAdditionController.php`
- `app/Http/Controllers/ServiceOperatingController.php`
- `app/Http/Controllers/ServiceDiscountController.php`
- `app/Http/Controllers/ServicesFormGroupingElementsController.php`
- `app/Http/Controllers/PlanMasterController.php`
- `app/Http/Controllers/Incentive/IncentiveServiceIncludeExcludeController.php`
- `app/Http/Controllers/Incentive/IncentiveDepartmentController.php`

### 2. Models & Services
**Models:**
- `app/Models/UniversalGroup/PatientVisitServicesUniversalGroupsCodeValues.php`
- `app/Models/WebServiceLogDetail.php`
- `app/Models/ItemMaster.php`
- `app/Models/User/UserRoleSpecialitySubDepartmentBranch.php`
- `app/Models/Flexibility/Master_Flexibility.php`
- `app/Models/PhysioTherapy/WorkflowServices.php`
**Services:**
- `app/Services/ServiceDeliveryPanel/ServiceDelivery.php`
- `app/Services/Mantys/MantysEligibilityService.php`
- `app/Services/Mantys/MantysApiService.php`
- `app/Services/Vital/VitalReferenceRangeService.php`

### 3. Mapped Web / API Routes
- `routes/controllers/PackageDetails.php:8:Route::get('getServiceDataDetails','PACKAGE\PackageDetailsController@getServiceDataDetails');`
- `routes/controllers/PackageDetails.php:18:Route::get('addservicesForCompDet/{id}', 'PACKAGE\PackageDetailsController@addservicesForCompDet');`
- `routes/controllers/PackageDetails.php:21:Route::get('getallservicesCompdetails', 'PACKAGE\PackageDetailsController@getautoservicePackCompdetails');`
- `routes/controllers/PackageDetails.php:25:Route::get('getAllPackageMasterForPackComponentDetail', 'PACKAGE\PackageDetailsController@getAllPackageMasterForPackComponentDetail');`
- `routes/controllers/PackageDetails.php:26:Route::get('getFetchPackageBasedServiceforComponentDetails', 'PACKAGE\PackageDetailsController@getFetchPackageBasedServiceforComponentDetails');`
- `routes/controllers/PackageDetails.php:29:Route::get('GetServicenameDetailsvalidation', 'PACKAGE\PackageDetailsController@GetServicenameDetailsvalidation');`
- `routes/controllers/SpecimenMangagement.php:6:Route::post('insertlisservicecomments', 'SpecimenMangagementController@insertlisservicecomments');`
- `routes/controllers/SpecimenMangagement.php:15:Route::post('filterdepartmentbasedcon', 'SpecimenMangagementController@filterdepartmentbasedcon');`
- `routes/controllers/SpecimenMangagement.php:16:Route::post('filterdepartmentbasedspecimen', 'SpecimenMangagementController@filterdepartmentbasedspecimen');`
- `routes/controllers/SpecimenMangagement.php:23:Route::post('editlisservicecomments', 'SpecimenMangagementController@editlisservicecomments');`
- `routes/controllers/SpecimenMangagement.php:43:Route::get('getLISServiceInstruction','SpecimenMangagementController@getLISServiceInstruction');`
- `routes/controllers/EMRInventoryConsumption.php:4:Route::get('Department/{id?}','EMRInventoryConsumptionController@getDepartment'); `
- `routes/controllers/EMRInventoryConsumption.php:5:Route::get('SubDepartment/{id?}','EMRInventoryConsumptionController@getSubDept');`
- `routes/controllers/EMRInventoryConsumption.php:9:Route::get('ConServices/{id?}','EMRInventoryConsumptionController@getServices');`
- `routes/controllers/RegistrationAppointment.php:3:Route::get('getSpecialityDepartmentDetails','RegistrationAppointmentPartOneController@getSpecialityDepartmentDetails');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `AAA_New_Service_Master`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `CPT_Code` | varchar | NO |
| `Service_Name` | varchar | NO |

#### Table: `Tmp_AVH_Service_Master`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `SErvice_DEscription` | nvarchar | NO |
| `Universal_Code_Value` | nvarchar | NO |
| `DEpartment_Code` | nvarchar | NO |
| `Department_Name` | nvarchar | NO |
| `Sub_DEpartment_Code` | nvarchar | NO |
| `Sub_Department_Name` | nvarchar | NO |
| `Universal_Code_Type` | nvarchar | NO |
| `Consulting_Non_Consulting_Service_Indicator` | nvarchar | NO |

---

## 📌 Module: Insurance

### 1. Controllers
- `app/Http/Controllers/PolicyInsuranceCompanyAndPlanController.php`
- `app/Http/Controllers/InsuranceassociatecompanyController.php`
- `app/Http/Controllers/InsurancePlanPriorApprovalController.php`
- `app/Http/Controllers/CompanyBasedInventoryInsuranceController.php`
- `app/Http/Controllers/AutoEclaimPostController.php`
- `app/Http/Controllers/DropDownListParameterController.php`
- `app/Http/Controllers/WHOChecklistPanelController.php`
- `app/Http/Controllers/InsurancePlansDepartmentCoverController.php`

### 2. Models & Services
**Models:**
- `app/Models/StockItemInsurancePrice.php`
- `app/Models/EncounterBasedClaimTime.php`
- `app/Models/Package/PatientPackagedAvail.php`
- `app/Models/Package/PatientPackageComponentComments.php`
- `app/Models/ClaimRemittanceDetailsNotMatchedClaim.php`
- `app/Models/BranchEClaimLink.php`
**Services:**
- `app/Services/ClaimMandatoryObservationTypeService.php`
- `app/Services/PharmacyEclaimValidationService.php`
- `app/Services/PostingMergeClaim.php`
- `app/Services/InsuranceEligibilityCheckRPAService.php`

### 3. Mapped Web / API Routes
- `routes/controllers/PackageDetails.php:3:Route::get('packageDetails','PACKAGE\PackageDetailsController@getPackageDetails');`
- `routes/controllers/PackageDetails.php:4:Route::get('packageSearch','PACKAGE\PackageDetailsController@getPackageSearch');`
- `routes/controllers/PackageDetails.php:10:Route::get('GetPackageDetailsAdd','PACKAGE\PackageDetailsController@GetPackageDetailsAdd');`
- `routes/controllers/PackageDetails.php:12:Route::get('getPackCompDetActiceStatusDetails/{id?}/{status}','PACKAGE\PackageDetailsController@getPackCompDetActiceStatusDetails');`
- `routes/controllers/PackageDetails.php:13:Route::post('GetPackageDetailsInsert', 'PACKAGE\PackageDetailsController@GetPackageDetailsInsert');`
- `routes/controllers/PackageDetails.php:15:Route::get('viewPackageComponentsDetail/{id?}', 'PACKAGE\PackageDetailsController@getPackCompDetails');`
- `routes/controllers/PackageDetails.php:16:Route::get('viewEditPackageCompDetails/{id}', 'PACKAGE\PackageDetailsController@getEditPackageComponentDetails');`
- `routes/controllers/PackageDetails.php:22:Route::get('GetpackanameDetailsvalidation', 'PACKAGE\PackageDetailsController@GetpackanameDetailsvalidation');`
- `routes/controllers/EMRInventoryConsumption.php:27:Route::get('InventoyBillingVisitPatientSearch','EMRInventoryConsumptionController@InventoyBillingVisitPatientSearch');`
- `routes/controllers/RegistrationAppointment.php:3:Route::get('getSpecialityDepartmentDetails','RegistrationAppointmentPartOneController@getSpecialityDepartmentDetails');`
- `routes/controllers/RegistrationAppointment.php:4:Route::get('getResourceServiceDupParaRecords','RegistrationAppointmentPartOneController@getResourceServiceDupParaRecords');`
- `routes/controllers/RegistrationAppointment.php:6:Route::get('cancelVisitForAppointmentModal','RegistrationAppointmentPartOneController@cancelVisitForAppointmentModal');`
- `routes/controllers/RegistrationAppointment.php:7:Route::get('loadReferralClinicId','RegistrationAppointmentPartOneController@loadReferralClinicId');`
- `routes/controllers/RegistrationAppointment.php:8:Route::get('loadReferralDoctorId','RegistrationAppointmentPartOneController@loadReferralDoctorId');`
- `routes/controllers/RegistrationAppointment.php:9:Route::get('loadReferralResource','RegistrationAppointmentPartOneController@loadReferralResource');`

### 4. Database Tables & Columns (MSSQL)
#### Table: `Insurance_Associate_Company_Insurance_Company`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Insurance_Associate_Company_Insurance_Company_Serial_No` | int | NO |
| `Insurance_Associate_Company_Serial_No` | int | NO |
| `Insurance_Company_Serial_No` | int | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |

#### Table: `Insurance_Company`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Insurance_Company_Serial_No` | int | NO |
| `Insurance_Company_Name` | nvarchar | NO |
| `Insurance_Company_Address_Line1` | nvarchar | NO |
| `Insurance_Company_Address_Line2` | nvarchar | YES |
| `Insurance_Company_Address_Line3` | nvarchar | YES |
| `Po_Box` | nvarchar | YES |
| `Area_Code` | nvarchar | NO |
| `Contact_Email` | nvarchar | YES |
| `Contact_Phone_Landline` | decimal | YES |
| `Contact_Phone_Mobile` | decimal | YES |

#### Table: `Insurance_Company_Based_Internal_Code`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Insurance_Company_Based_Internal_Code_Serial_No` | bigint | NO |
| `Insurance_Company_Serial_No` | int | NO |
| `Service_USSDB_Serial_No` | bigint | NO |
| `Internal_Code` | varchar | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |
| `Company_Service_Description` | nvarchar | YES |

#### Table: `Insurance_Company_Branch`
| Column Name | Data Type | Nullable |
| :--- | :--- | :--- |
| `Insurance_Company_Branch_Serial_No` | int | NO |
| `Insurance_Company_Serial_No` | int | NO |
| `Branch_Code` | nvarchar | NO |
| `Created_By_User_Id` | nvarchar | NO |
| `Created_Date_Time` | datetime | NO |
| `Modified_By_User_Id` | nvarchar | NO |
| `Modified_Date_Time` | datetime | NO |
| `Active_Status` | nvarchar | NO |
| `Service_Tax_Type_Code` | nvarchar | YES |
| `Default_Consuample_Value` | decimal | NO |

---

## 📌 Module: HIMES Pricing Architecture & Effective Date Protocols

> **Standard Billing Protocol (`addPatientBilling` / `PatientBillingGetController` / `BillingQueryController`)**
> All prices in HIMES (Services, Inventory Items, and Bed Management) have historical versions over time. The system ALWAYS resolves prices dynamically by picking `TOP 1` ordered by `Effective/Start Date DESC` where `CAST(Date AS DATE) <= CAST(GETDATE() AS DATE)`.

### 1. Services Pricing
- **Cash / Non-Insurance**:
  - Table: `Service_Rate_For_Non_Insurance` (`SRFNI`)
  - Rate: `SRFNI.Service_Base_Rate`
  - Effective Date: `CAST(SRFNI.Service_Rate_For_Non_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE) ORDER BY SRFNI.Service_Rate_For_Non_Insurance_Start_Date DESC` -> `TOP 1`
  - Filter: `SRFNI.Service_USSDB_Serial_No = ? AND SRFNI.Active_Status = 'A' AND SRFNI.Partner_Company_Serial_No IS NULL AND SRFNI.Is_It_Service_Resource_Drug = 'S'`
- **Insurance**:
  - Table: `Service_Rate_For_Insurance` (`SRFNI`)
  - Rate: `SRFNI.Service_Base_Rate`
  - Effective Date: `CAST(SRFNI.Service_Rate_For_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE) ORDER BY SRFNI.Service_Rate_For_Insurance_Start_Date DESC` -> `TOP 1`
  - Filter: `SRFNI.Insurance_Company_Serial_No = ? AND SRFNI.Patient_Income_Network_Universal_Groups_Serial_No = ? AND SRFNI.Patient_Payment_Type_Serial_No = ? AND SRFNI.Active_Status = 'A' AND SRFNI.Partner_Company_Serial_No IS NULL`
- **Doctor / Resource Specific**:
  - Table: `Resource_rate_For_Insurance` (`Resource_Base_Rate`, latest `Start_Date <= GETDATE()`)

### 2. Inventory Items Pricing (Pharmacy Drugs & Consumables)
- **Cash / Non-Insurance**:
  - Table: `Stock_Item_Price` (`sip`)
  - Rate: `sip.Selling_Price`
  - Effective Date: `CAST(sip.Stock_Item_Price_Effective_Date AS DATE) <= CAST(GETDATE() AS DATE) ORDER BY sip.Stock_Item_Price_Effective_Date DESC` -> `TOP 1`
  - Filter: `sip.Item_Master_Serial_No = ? AND sip.Active_Status = 'A'`
- **Insurance**:
  - Table: `Stock_Item_Insurance_Price` (`siip`) / `Company_Based_Inventory_Insurance_Item_Price`
  - Rate: `siip.Insurance_Gross_Amount`
  - Effective Date: `CAST(siip.Effective_Date AS DATE) <= CAST(GETDATE() AS DATE) ORDER BY siip.Effective_Date DESC` -> `TOP 1`
  - Filter: `siip.Item_Master_Serial_No = ? AND siip.Active_Status = 'A'`

### 3. Bed Management Pricing (IPD Rooms & Beds)
- **Bed Tracking**:
  - Table: `Patient_Visit_Resources` (`pvr`), Active: `pvr.Active_Status = 'A' AND pvr.Resource_Allocation_Cancellation_Flag = 'N'`
  - Join: `Resource_Service rs ON rs.Resource_Serial_No = pvr.Resource_Serial_No`, `Service s ON s.Service_Serial_No = rs.Service_Serial_No`, `Service_USSDB sussdb ON sussdb.Service_Serial_No = s.Service_Serial_No`
  - Rules: `Price_Rule_For_Resources` (`Resource_Type_Category_Flag = 'B'`, `Effective_Start_Date <= GETDATE()`)
- **Cash Bed Rate**:
  - Table: `Service_Rate_For_Non_Insurance` via Bed's `Service_USSDB_Serial_No`
  - Rate: `Service_Base_Rate`, latest `Start_Date <= GETDATE() ORDER BY Start_Date DESC` -> `TOP 1`
- **Insurance Bed Rate**:
  - Table: `Resource_Rate_For_Insurance` (or `Service_Rate_For_Insurance`)
  - Rate: `Resource_Base_Rate` / `Service_Base_Rate`, latest `Start_Date <= GETDATE() ORDER BY Start_Date DESC` -> `TOP 1`
  - Filter: Matching `Insurance_Company_Serial_No` and `Patient_Income_Network_Universal_Groups_Serial_No`

---

