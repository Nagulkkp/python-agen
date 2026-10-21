"""
seed_clinical_knowledge.py
===========================
Synchronizes the 10 HIMES Hospital Clinical Standard Operating Procedures (SOPs)
and Critical/Panic Value thresholds into ChromaDB and Valkey.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from memory_manager import add_to_knowledge_base, chroma_client
from valkey_himes_manager import valkey_manager

KB_DIR = os.path.join(BASE_DIR, "clinical_knowledge")

# Authoritative Critical / Panic Values Master Table (extracted from LIS SOP)
PANIC_VALUES_MASTER = {
    "potassium": {
        "analyte": "Potassium (K+)",
        "department": "Biochemistry",
        "low_critical": 2.8,
        "high_critical": 6.0,
        "unit": "mmol/L",
        "clinical_significance": "Fatal cardiac arrhythmias, ventricular fibrillation, asystole"
    },
    "sodium": {
        "analyte": "Sodium (Na+)",
        "department": "Biochemistry",
        "low_critical": 120.0,
        "high_critical": 160.0,
        "unit": "mmol/L",
        "clinical_significance": "Cerebral edema, seizures, brain herniation, coma"
    },
    "total_calcium": {
        "analyte": "Total Calcium",
        "department": "Biochemistry",
        "low_critical": 6.5,
        "high_critical": 13.0,
        "unit": "mg/dL",
        "clinical_significance": "Tetany, laryngospasm, hypercalcemic crisis, cardiac arrest"
    },
    "ionized_calcium": {
        "analyte": "Ionized Calcium",
        "department": "Biochemistry",
        "low_critical": 0.80,
        "high_critical": 1.60,
        "unit": "mmol/L",
        "clinical_significance": "Neuromuscular irritability vs. cardiac arrhythmia"
    },
    "glucose": {
        "analyte": "Blood Glucose",
        "department": "Biochemistry",
        "low_critical": 50.0,
        "high_critical": 400.0,
        "unit": "mg/dL",
        "clinical_significance": "Neuroglycopenic coma / brain injury vs. DKA / HHS crisis"
    },
    "magnesium": {
        "analyte": "Magnesium",
        "department": "Biochemistry",
        "low_critical": 1.0,
        "high_critical": 4.5,
        "unit": "mg/dL",
        "clinical_significance": "Torsades de pointes vs. respiratory depression, heart block"
    },
    "phosphorus": {
        "analyte": "Phosphorus",
        "department": "Biochemistry",
        "low_critical": 1.0,
        "high_critical": 8.0,
        "unit": "mg/dL",
        "clinical_significance": "Diaphragmatic weakness, hemolysis vs. metastatic calcification"
    },
    "troponin": {
        "analyte": "Cardiac Troponin I/T",
        "department": "Biochemistry",
        "high_critical": "Positive / >= 99th percentile cutoff",
        "unit": "ng/mL",
        "clinical_significance": "Acute Myocardial Infarction / Acute Coronary Syndrome"
    },
    "abg_ph": {
        "analyte": "Arterial Blood Gas pH",
        "department": "Biochemistry",
        "low_critical": 7.20,
        "high_critical": 7.60,
        "unit": "pH",
        "clinical_significance": "Severe metabolic/respiratory acidosis vs. alkalosis"
    },
    "pco2": {
        "analyte": "pCO2 (Arterial)",
        "department": "Biochemistry",
        "low_critical": 20.0,
        "high_critical": 65.0,
        "unit": "mmHg",
        "clinical_significance": "Severe respiratory failure / hypercapnic arrest risk"
    },
    "po2": {
        "analyte": "pO2 (Arterial)",
        "department": "Biochemistry",
        "low_critical": 50.0,
        "unit": "mmHg",
        "clinical_significance": "Refractory hypoxemia, acute respiratory failure"
    },
    "lactate": {
        "analyte": "Blood Lactate",
        "department": "Biochemistry",
        "high_critical": 4.0,
        "unit": "mmol/L",
        "clinical_significance": "Severe tissue hypoperfusion, septic shock"
    },
    "hemoglobin": {
        "analyte": "Hemoglobin (Hb)",
        "department": "Hematology",
        "low_critical": 6.5,
        "high_critical": 20.0,
        "unit": "g/dL",
        "clinical_significance": "Critical tissue hypoxia / shock vs. hyperviscosity stroke"
    },
    "platelets": {
        "analyte": "Platelet Count",
        "department": "Hematology",
        "low_critical": 20000,
        "high_critical": 1000000,
        "unit": "/µL",
        "clinical_significance": "Spontaneous fatal hemorrhage (intracranial/GI) vs. thrombosis"
    },
    "wbc": {
        "analyte": "Total WBC Count",
        "department": "Hematology",
        "low_critical": 1500,
        "high_critical": 50000,
        "unit": "/µL",
        "clinical_significance": "Severe immunocompromise vs. leukostasis / acute leukemia"
    },
    "anc": {
        "analyte": "Absolute Neutrophils (ANC)",
        "department": "Hematology",
        "low_critical": 500,
        "unit": "/µL",
        "clinical_significance": "Life-threatening Febrile Neutropenia risk"
    },
    "inr": {
        "analyte": "Prothrombin Time INR",
        "department": "Coagulation",
        "high_critical": 5.0,
        "unit": "INR",
        "clinical_significance": "Imminent major hemorrhage risk"
    },
    "aptt": {
        "analyte": "APTT",
        "department": "Coagulation",
        "high_critical": 100.0,
        "unit": "seconds",
        "clinical_significance": "Spontaneous bleeding risk"
    },
    "fibrinogen": {
        "analyte": "Fibrinogen",
        "department": "Coagulation",
        "low_critical": 100.0,
        "unit": "mg/dL",
        "clinical_significance": "Severe Disseminated Intravascular Coagulation (DIC)"
    }
}

# Specimen Collection & Vacutainer Color Coding (from LIS SOP)
VACUTAINER_GUIDE = {
    "lavender_purple": {
        "additive": "K2-EDTA",
        "department": "Hematology & Molecular",
        "tests": ["CBC (Complete Blood Count)", "ESR", "HbA1c", "Blood Smear", "Malaria Smear", "Blood Grouping"],
        "inversions": "8-10 times",
        "rules": "Fill to indicator line; never shake vigorously to prevent hemolysis."
    },
    "light_blue": {
        "additive": "3.2% Sodium Citrate (1:9 ratio)",
        "department": "Coagulation",
        "tests": ["PT / INR", "APTT", "D-Dimer", "Fibrinogen"],
        "inversions": "3-4 times",
        "rules": "Strict 9:1 blood-to-anticoagulant ratio required. Underfilling invalidates clotting time."
    },
    "gold_yellow_sst": {
        "additive": "Clot Activator and Gel Separator (SST)",
        "department": "Biochemistry, Serology & Immunology",
        "tests": ["LFT", "RFT / Renal Panel", "Lipid Profile", "Electrolytes", "Hormones", "Cardiac Enzymes", "Infectious Serology"],
        "inversions": "5 times",
        "rules": "Allow 30 minutes clotting prior to centrifugation."
    },
    "green": {
        "additive": "Lithium Heparin",
        "department": "STAT Biochemistry",
        "tests": ["STAT Troponin", "STAT Electrolytes", "STAT ABG / Blood Gas"],
        "inversions": "8-10 times",
        "rules": "Centrifuge immediately for rapid turnaround."
    },
    "grey": {
        "additive": "Sodium Fluoride / Potassium Oxalate",
        "department": "Biochemistry",
        "tests": ["Plasma Fasting / Postprandial Glucose", "Lactate"],
        "inversions": "8-10 times",
        "rules": "Inhibits glycolysis for up to 24 hours."
    }
}

def seed_clinical_knowledge():
    print("=" * 65)
    print(" SEEDING CLINICAL SOPS & PANIC VALUES INTO CHROMADB & VALKEY")
    print("=" * 65)

    if not os.path.exists(KB_DIR):
        print(f"Error: {KB_DIR} does not exist.")
        return

    files = [f for f in os.listdir(KB_DIR) if f.endswith(".md")]
    print(f"Found {len(files)} SOP files to index:")

    chroma_docs = []
    sop_list_summary = []

    for f in sorted(files):
        path = os.path.join(KB_DIR, f)
        with open(path, "r", encoding="utf-8", errors="replace") as fp:
            content = fp.read()

        slug = f.replace(".md", "")
        # Extract title from first markdown header
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else slug.replace("_", " ").title()

        # Generate a clean summary
        first_p = ""
        paragraphs = content.split("\n\n")
        for p in paragraphs:
            clean_p = p.strip()
            if clean_p and not clean_p.startswith("#"):
                first_p = clean_p[:400]
                break

        sop_info = {
            "slug": slug,
            "filename": f,
            "title": title,
            "summary": first_p
        }
        sop_list_summary.append(sop_info)

        # 1. Cache full SOP into Valkey
        valkey_sop_key = f"himes:clinical:sop:{slug}"
        valkey_manager.set_cached_data(valkey_sop_key, {
            "slug": slug,
            "title": title,
            "content": content,
            "summary": first_p
        }, ttl_seconds=86400 * 30)  # 30 days
        print(f"  ✓ Cached in Valkey: {valkey_sop_key}")

        # 2. Prepare chunks for ChromaDB
        # Add the document overview
        chroma_docs.append({
            "text": f"HIMES Hospital Clinical Policy / Protocol: {title}\n\n{content[:2500]}",
            "metadata": {
                "source": f,
                "slug": slug,
                "title": title,
                "type": "clinical_sop_overview",
                "department": "Clinical Operations"
            }
        })

        # Chunk sections by header ##
        sections = re.split(r"\n(?=##\s+)", content)
        for s in sections:
            s_clean = s.strip()
            if len(s_clean) > 80:
                h_match = re.search(r"^##\s+(.+)$", s_clean, re.MULTILINE)
                sec_title = h_match.group(1).strip() if h_match else title
                chroma_docs.append({
                    "text": f"{title} - Section: {sec_title}\n\n{s_clean}",
                    "metadata": {
                        "source": f,
                        "slug": slug,
                        "title": title,
                        "section": sec_title,
                        "type": "clinical_sop_section"
                    }
                })

    # 3. Store Panic Values Master & Vacutainer Guide into Valkey
    valkey_manager.set_cached_data("himes:clinical:panic_values", PANIC_VALUES_MASTER, ttl_seconds=86400 * 30)
    valkey_manager.set_cached_data("himes:clinical:vacutainer_guide", VACUTAINER_GUIDE, ttl_seconds=86400 * 30)
    valkey_manager.set_cached_data("himes:clinical:protocols_list", sop_list_summary, ttl_seconds=86400 * 30)
    print("  ✓ Stored 'himes:clinical:panic_values' in Valkey")
    print("  ✓ Stored 'himes:clinical:vacutainer_guide' in Valkey")
    print("  ✓ Stored 'himes:clinical:protocols_list' in Valkey")

    # 4. Insert into ChromaDB
    print(f"\nAdding {len(chroma_docs)} clinical chunks into ChromaDB knowledge base...")
    try:
        ids = add_to_knowledge_base(chroma_docs)
        print(f"  ✓ Successfully indexed {len(ids)} chunks in ChromaDB!")
    except Exception as e:
        print(f"  ❌ Error indexing into ChromaDB: {e}")

    print("\n" + "=" * 65)
    print(" CLINICAL KNOWLEDGE SEEDING COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    seed_clinical_knowledge()
