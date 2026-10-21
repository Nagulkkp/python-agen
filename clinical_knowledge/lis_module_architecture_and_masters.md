# Laboratory Information System (LIS) Module Architecture & Master Configurations

## 1. Overview and Core Purpose
The HIMES Laboratory Information System (LIS) module manages the entire lifecycle of diagnostic pathology testing across Inpatient (IPD), Outpatient (OPD), and Emergency (ED) departments. It coordinates test ordering (CPOE), phlebotomy, barcode generation, specimen accessioning, automated analyzer interfacing, technical verification, pathologist clinical approval, critical/panic values notification, and multichannel report dispatch adhering to ISO 15189 and CAP accreditation standards.

## 2. Laboratory Sub-Departments & Specialties
The HIMES LIS is structured into eight core sub-departments:
- **Clinical Biochemistry**: High-throughput automated routine chemistry (LFT, RFT, Lipid, Glucose, Cardiac biomarkers, Electrolytes) and immunochemistry (Hormones, Tumor markers, Vitamins, Therapeutic Drug Monitoring).
- **Hematology & Coagulation**: Complete blood count (CBC/FBC), 5-part differential, reticulocyte count, ESR, peripheral blood smear, and coagulation assays (PT/INR, APTT, D-Dimer, Fibrinogen).
- **Microbiology & Serology**: Bacteriology cultures, direct microscopy (Gram stain, AFB/ZN stain, KOH mount), automated organism identification (VITEK/MALDI-TOF), Antibiotic Susceptibility Testing (AST), and infectious serology (HIV, Hepatitis B/C, Syphilis, Dengue, COVID-19).
- **Clinical Pathology & Urinalysis**: Physical, chemical, and microscopic examination of urine, stool routine and occult blood (FOBT), semen analysis, and body fluid analysis (CSF, pleural, peritoneal, synovial).
- **Histopathology & Cytopathology**: Tissue biopsies, gross description, microscopic examination, special histochemical stains, immunohistochemistry (IHC), Pap smears, and fine-needle aspiration cytology (FNAC).
- **Molecular Diagnostics**: Real-time PCR assays, viral load quantification (HIV/HCV), genetic mutation analysis, and respiratory/gastrointestinal pathogen multiplex panels.
- **Blood Bank & Transfusion Services**: Blood grouping (ABO & Rh typing), antibody screening, crossmatching, blood component preparation (PRBC, FFP, Platelets, Cryoprecipitate), and transfusion reaction logging.
- **Point-of-Care Testing (POCT)**: Bedside blood gas (ABG), POCT glucose, and cardiac rapid tests linked to central LIS.

## 3. LIS Master Configurations & Data Architecture
The HIMES database schema models laboratory services and parameters through normalized relationships:
- **Service Master (`Service_LIS`, `Service`)**: Defines the billable laboratory test or panel (e.g., Complete Blood Count, Liver Function Test, Serum Potassium) with CPT code, department, and default turnaround time.
- **Parameter Master (`Parameters`, `Service_Parameter_Mapping`)**: Defines individual reportable analytes within a service (e.g., AST, ALT, Total Bilirubin within LFT; WBC, Hb, Platelets within CBC).
- **Parameter Types**:
  1. *Numeric*: Quantitative numerical results with defined decimal precision, measurement units, and reference intervals.
  2. *Calculated / Formula*: Auto-computed parameters (e.g., eGFR via CKD-EPI, LDL Cholesterol via Friedewald equation, Anion Gap, Globulin, Albumin/Globulin ratio).
  3. *Textual / Free Text*: Qualitative observations and descriptive interpretations.
  4. *Predefined Dropdown / Picklist (`DropDownListParameter`)*: Standardized qualitative options (e.g., Negative/Positive, Clear/Turbid, Nil/Trace/+1/+2/+3).
  5. *Antibiotic Sensitivity Matrix (`LISMicrobiology`)*: Grid mapping isolated organisms to antimicrobial panels with Zone Diameters / MICs and S/I/R interpretations.
  6. *Rich-Text Template (`LISReportTemplate`)*: Formatted narrative reports for histopathology, cytology, and bone marrow aspirations.

## 4. Specimen Container & Tube Color-Coding Standards
Standard tube additives, stoppers, and clinical indications:
- **Lavender / Purple Top (K2/K3 EDTA)**: Complete Blood Count (CBC), ESR, HbA1c, Blood grouping, Peripheral smear, Molecular PCR. Inversion: 8-10 times.
- **Gold / Red Top (SST / Serum Gel with Clot Activator)**: Routine Biochemistry (LFT, RFT, Lipid, Cardiac enzymes), Serology, Immunology, Thyroid, Tumor markers. Inversion: 5 times. Allow 30 mins to clot before centrifugation.
- **Light Blue Top (3.2% Buffered Sodium Citrate, 9:1 blood-to-anticoagulant ratio)**: Coagulation profile (PT/INR, APTT, D-Dimer, Fibrinogen). Crucial: Must be filled precisely to indicator line. Inversion: 3-4 times.
- **Green Top (Lithium / Sodium Heparin)**: STAT Biochemistry, Blood gas, Ammonia, Cytogenetics. Inversion: 8-10 times.
- **Gray Top (Sodium Fluoride / Potassium Oxalate)**: Blood Glucose, Oral Glucose Tolerance Test (OGTT), Lactate. Prevents glycolysis. Inversion: 8-10 times.
- **Sterile Container / Swab**: Microbiological cultures, Urine culture, Sputum, Body fluids, Pus aspirates.
- **Blood Culture Bottles (Aerobic / Anaerobic)**: Suspected bacteremia/sepsis. Collect prior to antimicrobial therapy.

## 5. Reference Intervals, Panic Thresholds & Delta Checks
- **Reference Intervals**: Specific to patient age group (Neonate 0-28d, Infant 1-12m, Child 1-12y, Adolescent 13-18y, Adult 19-64y, Geriatric >=65y) and biological sex (Male, Female).
- **Panic / Critical Thresholds**: Life-threatening boundaries triggering immediate urgent clinical alerts (e.g., Potassium <2.8 or >6.0 mmol/L, Platelets <20,000 /µL, Glucose <50 or >400 mg/dL).
- **Delta Checks**: Automatic comparison of the current result against the patient's previous historical result within a configurable lookback window (default: 72 hours to 30 days). Percentage or absolute deviations exceeding delta thresholds flag potential specimen misidentification, IV fluid contamination, or acute clinical deterioration.

## 6. Analyzer Interfacing & Automation
- **Communication Protocols**: Bi-directional and uni-directional ASTM 1394 and HL7 v2.x (ORU_R01 messages) over TCP/IP or RS-232 serial interfaces (`HL7LisBackLogController`, `LISAnalyzerController`).
- **Workflow**: Analyzer scans specimen barcode -> sends query (HL7 QRY/QBP) to LIS -> LIS returns work order with requested tests -> Analyzer performs testing -> Analyzer transmits raw results (HL7 ORU_R01) -> LIS parses and populates `Patient_Visit_LIS_Service_Parameter_Result` -> Flags abnormal/delta triggers for technician verification.
- **Supported Platforms**: Roche Cobas, Sysmex XN series, Abbott Architect/Alinity, Beckman Coulter Access/AU, Mindray, bioMérieux VITEK-2.

## 7. Outsource Reference Laboratory Management
- For specialized/rare tests not performed in-house (e.g., esoteric genetics, specialized toxicology, rare autoimmune panels), tests are mapped to certified external reference labs (`OutsourceLabDetailsController`).
- Workflow: Order creation -> Outsource batch manifest generation -> Specimen packaging under chain of custody & cold chain preservation -> External lab result reception -> Pathologist review -> Report attachment and EMR integration.
