# Specimen Collection, Phlebotomy & Pre-Analytical Standard Operating Procedure

## 1. Pre-Analytical Quality Standard
Up to 70% of diagnostic laboratory errors occur in the pre-analytical phase (specimen collection, handling, labeling, and accessioning). This SOP mandates strict compliance across all HIMES collection centers, outpatient phlebotomy stations, inpatient wards, and emergency departments.

## 2. Patient Identification & Verification Protocol
- Phlebotomists and nursing staff must verify **at least two unique patient identifiers** before drawing any sample:
  1. Patient Full Legal Name.
  2. Permanent Medical Record Number (MRN) / Barcode on patient wristband.
- For unconscious or pediatric patients, identity must be confirmed with the accompanying guardian or primary nurse against the electronic bed chart.

## 3. Patient Preparation & Timing Requirements
- **Fasting Blood Glucose (FBS) & Lipid Profile**: 10 - 12 hours overnight fasting (water permitted). No alcohol 24h prior.
- **Post-Prandial Blood Glucose (PPBS)**: Exactly 2 hours after commencing the meal.
- **Serum Cortisol**: Morning sample (8:00 AM - 9:00 AM) or evening sample (4:00 PM - 5:00 PM) due to diurnal variation.
- **Therapeutic Drug Monitoring (TDM - Vancomycin, Digoxin, Lithium, Phenytoin)**:
  * *Trough Level*: Draw 30 minutes immediately prior to the next scheduled dose.
  * *Peak Level*: Draw 1-2 hours post-infusion or oral administration as per specific drug protocol.
- **24-Hour Urine Collection**: Discard first morning void on Day 1. Collect all subsequent urine for 24 hours including the first morning void of Day 2 in designated preservative container (e.g., Boric acid, 6N HCl, or plain container as per test requirement). Keep refrigerated.

## 4. Phlebotomy Technique & Mandatory Order of Draw (CLSI GP41)
To prevent cross-contamination of tube additives, blood samples must strictly be drawn in the following sequence:
1. **Blood Culture Bottles (Yellow/Silver & Blue/Maroon tops)**: Clean venipuncture site with 2% chlorhexidine gluconate in 70% isopropyl alcohol for 30s; allow to dry completely for 30s. Inoculate 8-10 mL blood per adult bottle (1-3 mL for pediatric bottle). Draw Aerobic bottle first, then Anaerobic.
2. **Coagulation Tube (Light Blue Top - 3.2% Sodium Citrate)**: Fill precisely to the nominal fill indicator line (1:9 ratio). Invert gently 3-4 times. If using a butterfly needle, draw a discard tube first to clear line dead-space.
3. **Serum / Clot Activator Tubes (Gold / Red Top - SST Gel)**: Invert gently 5 times.
4. **Heparin Tubes (Green Top - Lithium / Sodium Heparin)**: Invert gently 8-10 times.
5. **EDTA Tubes (Lavender / Purple Top - K2/K3 EDTA)**: Invert thoroughly 8-10 times to prevent micro-clot formation.
6. **Glycolysis Inhibitor Tubes (Gray Top - Sodium Fluoride / Potassium Oxalate)**: Invert gently 8-10 times.

> [!CAUTION]
> NEVER draw blood proximal to or from an active intravenous (IV) infusion line. If an arm with an IV line must be used, turn off IV infusion for at least 5 minutes, and draw distal to the IV site. Note IV draw on the requisition.

## 5. Barcoding, Labeling & Specimen Accessioning (`LISBarcodeGenerationController`)
- Every primary tube must be labeled at the patient's bedside immediately after phlebotomy.
- Barcode labels contain: Patient MRN, Full Name, Visit ID, Specimen ID, Container Type, Collection Date/Time, and Collector User ID.
- Labels must be affixed vertically, leaving the specimen viewing window clear.

## 6. Specimen Rejection Criteria & Indices
Specimens failing any of the following criteria must be rejected at the accessioning desk with immediate electronic notification and redraw request:
- **Hemolysis (H-Index > Threshold)**: Ruptured RBCs release intracellular contents, causing false elevation of Potassium ($K^+$), AST, LDH, Magnesium, Phosphate, and false decrease in Troponin T or Bilirubin. Reject for Potassium, Coagulation, and Cardiac enzymes.
- **Lipemia (L-Index > Threshold)**: High turbidity from triglycerides interferes with spectrophotometric/optical assays.
- **Icterus (I-Index > Threshold)**: Severe bilirubinemia causing optical interference.
- **Clotted Specimen in Anticoagulated Tubes**: Any clot in EDTA (Lavender) or Citrate (Blue) invalidates CBC, Platelet count, ESR, and PT/APTT.
- **Quantity Not Sufficient (QNS)**: Underfilled tube; especially critical for Citrate (Blue top) where >10% underfill falsely prolongs PT and APTT.
- **Incorrect Tube / Additive**: E.g., drawing Calcium or Potassium in EDTA (causes zero Calcium and fatal pseudo-hyperkalemia).
- **Mismatched / Unlabeled Container**: Incomplete or contradictory patient identifiers.
- **Delayed Transport**: Exceeding sample stability (e.g., uncentrifuged serum standing >2 hours causes glycolysis and potassium leakage from RBCs).

## 7. Specimen Rejection & Redraw Workflow
1. Accession technician logs rejection reason code in HIMES LIS.
2. System sends instant critical task alert to ordering physician and nursing station.
3. Redraw request is prioritized with high urgency tag (`LIS_Redraw_Pending`).
