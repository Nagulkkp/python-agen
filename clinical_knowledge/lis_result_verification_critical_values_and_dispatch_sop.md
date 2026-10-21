# LIS Result Verification, Critical/Panic Values Notification & Report Dispatch SOP

## 1. Post-Analytical Phase Standard
The post-analytical phase encompasses result review, delta checking, technical verification, pathologist clinical authorization, panic value escalation, report formatting, and secure multi-channel delivery.

## 2. Multi-Tier Verification Workflow
1. **Automated Validation / Delta Checking**: LIS flags abnormal parameters (High $\uparrow$, Low $\downarrow$) and critical triggers ($\ast\ast\text{CRITICAL}\ast\ast$). Auto-flags any delta check deviation exceeding lookback variance thresholds (e.g., Creatinine change $>0.5\text{ mg/dL}$ or $>50\%$ within 48 hours; Hemoglobin drop $>2.0\text{ g/dL}$ in 24 hours).
2. **Technical Verification (Medical Laboratory Technologist)**: MLT reviews raw analyzer curves, QC status of the testing batch, slide morphology, and confirms absence of pre-analytical artifacts (hemolysis, clots, IV fluid dilution).
3. **Pathologist / Clinical Authorization (`LISResultApprovalController`)**: Senior Pathologist / Laboratory Director reviews complex profiles, abnormal smears, malignant cytology, critical biopsies, and signs off digitally.

---

## 3. Authoritative Critical / Panic Values Master Table

When any laboratory parameter breaches the following life-threatening thresholds, immediate verbal notification and electronic escalation must occur within **15 minutes**:

| Department | Analyte / Parameter | Low Critical Threshold | High Critical Threshold | Clinical Significance / Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Biochemistry** | **Potassium ($K^+$)** | **$< 2.8\text{ mmol/L}$** | **$> 6.0\text{ mmol/L}$** | Fatal cardiac arrhythmias, ventricular fibrillation, asystole |
| **Biochemistry** | **Sodium ($Na^+$)** | **$< 120\text{ mmol/L}$** | **$> 160\text{ mmol/L}$** | Cerebral edema, seizures, brain herniation, coma |
| **Biochemistry** | **Total Calcium** | **$< 6.5\text{ mg/dL}$** ($1.63\text{ mmol/L}$) | **$> 13.0\text{ mg/dL}$** ($3.25\text{ mmol/L}$) | Tetany, laryngospasm, hypercalcemic crisis, cardiac arrest |
| **Biochemistry** | **Ionized Calcium** | **$< 0.80\text{ mmol/L}$** | **$> 1.60\text{ mmol/L}$** | Neuromuscular irritability vs. cardiac arrhythmia |
| **Biochemistry** | **Blood Glucose** | **$< 50\text{ mg/dL}$** ($2.8\text{ mmol/L}$) | **$> 400\text{ mg/dL}$** ($22.2\text{ mmol/L}$) | Neuroglycopenic coma / brain injury vs. DKA / HHS crisis |
| **Biochemistry** | **Magnesium** | **$< 1.0\text{ mg/dL}$** ($0.4\text{ mmol/L}$) | **$> 4.5\text{ mg/dL}$** ($1.85\text{ mmol/L}$) | Torsades de pointes vs. respiratory depression, heart block |
| **Biochemistry** | **Phosphorus** | **$< 1.0\text{ mg/dL}$** ($0.32\text{ mmol/L}$) | **$> 8.0\text{ mg/dL}$** ($2.58\text{ mmol/L}$) | Diaphragmatic weakness, hemolysis vs. metastatic calcification |
| **Biochemistry** | **Cardiac Troponin I/T** | N/A | **$\ge \text{99th percentile cutoff}$** (Positive) | Acute Myocardial Infarction / Acute Coronary Syndrome |
| **Biochemistry** | **Arterial Blood Gas pH** | **$< 7.20$** | **$> 7.60$** | Severe metabolic/respiratory acidosis vs. alkalosis |
| **Biochemistry** | **$pCO_2$ (Arterial)** | **$< 20\text{ mmHg}$** | **$> 65\text{ mmHg}$** | Severe respiratory failure / hypercapnic arrest risk |
| **Biochemistry** | **$pO_2$ (Arterial)** | **$< 50\text{ mmHg}$** | N/A | Refractory hypoxemia, acute respiratory failure |
| **Biochemistry** | **Blood Lactate** | N/A | **$> 4.0\text{ mmol/L}$** | Severe tissue hypoperfusion, septic shock |
| **Hematology** | **Hemoglobin (Hb)** | **$< 6.5\text{ g/dL}$** | **$> 20.0\text{ g/dL}$** | Critical tissue hypoxia / shock vs. hyperviscosity stroke |
| **Hematology** | **Platelet Count** | **$< 20,000\text{ /µL}$** | **$> 1,000,000\text{ /µL}$** | Spontaneous fatal hemorrhage (intracranial/GI) vs. thrombosis |
| **Hematology** | **Total WBC Count** | **$< 1,500\text{ /µL}$** | **$> 50,000\text{ /µL}$** | Severe immunocompromise vs. leukostasis / acute leukemia |
| **Hematology** | **Absolute Neutrophils (ANC)** | **$< 500\text{ /µL}$** | N/A | Life-threatening Febrile Neutropenia risk |
| **Hematology** | **Peripheral Blood Smear** | N/A | Presence of **Blasts / Schistocytes / Sickle cells** | Acute leukemia, TTP / HUS, Sickle cell crisis |
| **Coagulation** | **Prothrombin Time INR** | N/A | **$> 5.0$** | Imminent major hemorrhage risk |
| **Coagulation** | **APTT** | N/A | **$> 100\text{ seconds}$** | Spontaneous bleeding risk |
| **Coagulation** | **Fibrinogen** | **$< 100\text{ mg/dL}$** | N/A | Severe Disseminated Intravascular Coagulation (DIC) |
| **Microbiology** | **Blood Culture** | N/A | **Positive Gram stain / growth** | Sepsis / Bacteremia |
| **Microbiology** | **CSF Examination** | N/A | **Positive Gram stain, AFB, or Cryptococcus** | Acute Bacterial / Tuberculous / Cryptococcal Meningitis |
| **Microbiology** | **Sterile Body Fluid Culture** | N/A | **Positive Growth (Synovial, Pleural, Peritoneal)** | Septic arthritis, empyema, spontaneous bacterial peritonitis |

---

## 4. Critical Alert Escalation & Read-Back Protocol
- **Timeframe**: Must be communicated verbally to responsible clinician within **15 minutes** of result generation.
- **Recipient Priority**:
  1. Ordering Attending Physician.
  2. On-duty Resident / Medical Officer in charge of patient.
  3. Primary Nurse / Charge Nurse at the Inpatient Unit / ICU / ED.
- **Mandatory Closed-Loop Read-Back**:
  1. Lab caller provides: Patient Full Name, MRN, Bed/Ward, Test Name, Exact Critical Value, and Units.
  2. Clinical receiver must repeat the exact information back word-for-word.
  3. Lab caller documents in HIMES LIS: Receiver Name, Receiver Designation, Date/Time of Call, Read-Back Confirmation ("Y"), and Caller User ID.

---

## 5. Turnaround Time (TAT) Standards & Benchmarks

Turnaround time is measured from the timestamp of specimen receipt at the laboratory accessioning desk to final result authorization:

- **STAT / Emergency Orders (ED / ICU / Code Blue)**:
  * Blood Gas (ABG), Electrolytes, Glucose, hs-Troponin: **$\le 45\text{ minutes}$**.
  * STAT CBC, Coagulation (PT/INR), Crossmatch: **$\le 45 - 60\text{ minutes}$**.
- **Routine Inpatient & Outpatient Chemistry / Hematology**:
  * Routine CBC, LFT, RFT, Lipid, Urinalysis: **$\le 2 - 4\text{ hours}$**.
- **Specialized Immunoassays & Endocrinology**:
  * Thyroid (TSH, FT4), Vitamin D, B12, Beta-hCG, Tumor Markers: **$\le 6 - 24\text{ hours}$** (Same day).
- **Microbiology**:
  * Direct Smear / Gram Stain: **$\le 1 - 2\text{ hours}$**.
  * Preliminary Culture Report: **$24 - 48\text{ hours}$**.
  * Final Culture Identification & AST: **$48 - 72\text{ hours}$**.
  * AFB Smear: $\le 24\text{ hours}$; AFB Culture (MGIT): Up to 6 weeks.
- **Histopathology & Biopsies**:
  * Intraoperative Frozen Section: **$\le 20\text{ minutes}$**.
  * Small Endoscopic / Core Biopsies: **$48 - 72\text{ hours}$**.
  * Complex Surgical Resection Specimens: **$5 - 7\text{ business days}$**.

---

## 6. Report Dispatch & Distribution Channels (`LISDispatchController`)
- **EMR Integration**: Real-time push to Doctor Consultation workbench, Nursing Electronic Kardex, and Inpatient Ward charts upon pathologist authorization.
- **Cumulative Result Trending**: Graphical and tabular historical view comparing current result with previous 5 encounters for vital trend analysis.
- **Patient Mobile App & Web Portal (`PatientMobileAppWebServiceLISReportController`)**: Secure release of digitally signed PDF reports with encrypted 2D QR code for external authenticity verification.
- **SMS / WhatsApp Automated Link**: Patient receives encrypted direct download link upon final report authorization.
