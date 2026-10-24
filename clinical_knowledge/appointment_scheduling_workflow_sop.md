# HIMES Appointment Scheduling & Patient Journey SOP

This knowledge document outlines the end-to-end appointment scheduling, resource allocation, and patient visit conversion workflow in HIMES.

## 1. 8 Appointment Booking Entry Points
1. **ASM Calendar Scheduler** (`/appointmentScheduler`): FullCalendar interactive grid for visual slot booking, drag/drop, and resizing (`appointmentSchedularController.php`).
2. **Patient Appointment Screen** (`/patientAppointment`): Standard form-based modal appointment creation (`PatientAppointmentController.php`).
3. **Global View of Appointments** (`/viewGlobalAppointment`): Enterprise multi-doctor/branch view with bulk confirm and register filters (`GlobalViewAppointmentController.php`).
4. **Front Desk / Quick Registration** (`/quickRegistration` & `/regBookedAppointment`): Converts booked appointments into live OP visits on arrival (`RegistrationAppointmentPostController.php`).
5. **Doctor Consultation / EMR Caseload**: Follow-up booking directly from Doctor Consultation screen or treatment plan.
6. **OT Scheduler** (`/OTScheduler`): Surgical booking by Building -> Floor -> Unit -> Room -> Bed/Table (`OTSchedularController.php`).
7. **Prior Visit Module** (`/viewPriorVisit`): Converts insurance prior authorization approvals into appointments (`PriorVisitController.php`).
8. **Patient Portal & Mobile APIs** (`/api/patientPortal/...` & `/Okadoc/...`): Web portal, WhatsApp bot, and Okadoc integration.

## 2. Resource & Speciality Master Hierarchy
- Hierarchy: `Branch -> Department -> Sub-Department -> Speciality -> Resource_Parent (Doctor) -> Resource`.
- Operating Hours: Defined in `Resource_Parent_Operating_Hours` (doctor hours) and `Resource_Service_Operating_Hours` (slot intervals, e.g. 15, 20, 30 mins).
- Leaves & Breaks: Tracked in `Resource_Non_Availability` (leaves block calendar slots).

## 3. Free vs Paid Follow-Up Rules
- Master Table: `Branch_Free_Paid_Followup_Services` mapped by `Branch_Code`, `Speciality_Code`, and `Paid_Free_Service_Status` (`'F'` = Free, `'P'` = Paid, `'R'` = Revisit).
- Limits: `Free_Follow_Up_Days_For_Cash_Patients`, `No_Of_Free_Follow_Up_Visits_For_Cash_Patients`, and Insurance counterparts in `Branch` & `Insurance_Company_Followup`.

## 4. Status Lifecycle & Color Codes
- `CF` (#2BD790 - Mint Green): Confirmed appointment.
- `PD` (#92BDF9 - Sky Blue): Pending appointment.
- `WF` (#E1C8E1 - Lavender): Waiting list (auto-promotes to CF upon cancellation).
- `NS` (#EDB917 - Amber): No-show after grace period.
- `CX` (#F6DCAB - Sand): Cancelled.
- `REG` (#948e79 - Grey): Registered and converted to live hospital visit in `Patient_Visit_Appointments`.
- `REF` (#C8EB02 - Lime Green): Reference secondary resource linked.

## 5. Validations Engine
- Single slot collision prevention (`Appointment_Required_Single_Slot = 'Y'`).
- Max daily appointment capacity quota (`Max_Appointments_Per_Day`).
- Doctor non-availability / leaves (`Resource_Non_Availability`).
- Duplicate same-day doctor booking prevention (`getExistingPatientDuplicateSameDaySameRes`).
- Follow-up date expiry validation.
