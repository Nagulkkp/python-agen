"""
seed_appointment_skill_to_valkey_and_chroma.py
==============================================
Loads the complete 12-section HIMES Appointment Workflow from SKILL.md into:
1. Valkey In-Memory Cache (RAM sub-millisecond fast-path key: 'himes:flow:appointment_workflow')
2. Valkey In-Memory Key ('himes:appointment:full_spec')
3. ChromaDB Persistent Vector Collection ('agent_knowledge_base')
"""

import os
import sys
import re
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from memory_manager import add_to_knowledge_base
from valkey_himes_manager import valkey_manager

SKILL_FILE = os.path.join(BASE_DIR, ".agents", "skills", "appointment-workflow", "SKILL.md")

def parse_and_seed():
    print("=" * 60)
    print("INDEXING FULL APPOINTMENT WORKFLOW INTO VALKEY & CHROMADB")
    print("=" * 60)

    if not os.path.exists(SKILL_FILE):
        print(f"Error: {SKILL_FILE} not found!")
        return

    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Store Full Document in Valkey
    valkey_manager.set_cached_data("himes:appointment:full_spec", content, ttl_seconds=86400 * 30)
    print("  ✓ Stored full document in Valkey under 'himes:appointment:full_spec' (30-day TTL)")

    # 2. Update 'himes:flow:appointment_workflow'
    flow_data = {
        "module": "appointment_workflow",
        "description": "HIMES Appointment Scheduling Module (ASM) & Patient Journey Architecture",
        "entry_points": [
            "1. ASM Calendar Scheduler (/appointmentScheduler - FullCalendar drag/drop/resize)",
            "2. Patient Appointment Screen (/patientAppointment - single modal form)",
            "3. Global View (/viewGlobalAppointment - enterprise multi-resource queue)",
            "4. Front Desk Registration (/quickRegistration & /regBookedAppointment - OP visit conversion)",
            "5. Doctor Consultation / EMR Caseload (followup booking from treatment plan)",
            "6. OT Scheduler (/OTScheduler - surgical theatre scheduling)",
            "7. Prior Visit Module (/viewPriorVisit - insurance PA conversion)",
            "8. Patient Portal & Okadoc APIs (/api/patientPortal/... - web/mobile/bot bookings)"
        ],
        "master_hierarchy": "Branch -> Department -> Sub-Department -> Speciality -> Resource_Parent (Doctor) -> Resource",
        "operating_hours": "Doctor: Resource_Parent_Operating_Hours & WeekDay; Slot duration: Resource_Service_Operating_Hours (15/20/30 mins); Fallback: Branch operational hours",
        "leaves_and_breaks": "Resource_Non_Availability blocks slots during leave/break intervals",
        "followup_rules": "Branch_Free_Paid_Followup_Services (F=Free, P=Paid, R=Revisit) + Branch limits (Free_Follow_Up_Days/Visits)",
        "status_lifecycle": {
            "CF": "Confirmed (#2BD790 - Mint Green)",
            "PD": "Pending (#92BDF9 - Sky Blue)",
            "WF": "Waiting List (#E1C8E1 - Lavender - auto-promotes to CF upon cancellation)",
            "NS": "No Show (#EDB917 - Amber)",
            "CX": "Cancelled (#F6DCAB - Sand)",
            "REG": "Registered (#948e79 - Grey - converted to live visit)",
            "REF": "Reference Resource (#C8EB02 - Lime Green)"
        },
        "visit_linking": "RegistrationAppointmentPostController inserts into Patient_Visit_Appointments (Patient_Appointment_Serial_No <-> Patient_Visit_Basic_Details_Serial_No)",
        "validations": [
            "Single slot collision prevention (Appointment_Required_Single_Slot = 'Y')",
            "Max daily quota check (Max_Appointments_Per_Day)",
            "Doctor leaves/breaks (Resource_Non_Availability)",
            "Same-day duplicate booking guard (getExistingPatientDuplicateSameDaySameRes)",
            "Followup expiry validity check"
        ]
    }
    valkey_manager.cache_himes_flow("appointment_workflow", flow_data, ttl=86400 * 30)
    print("  ✓ Updated 'himes:flow:appointment_workflow' in Valkey (30-day TTL)")

    # 3. Chunk Sections into ChromaDB
    sections = re.split(r'\n##\s+', content)
    chroma_docs = []
    
    # First chunk is header / overview
    header_chunk = sections[0].strip()
    chroma_docs.append({
        "text": header_chunk,
        "metadata": {
            "source": "appointment_workflow_skill.md",
            "module": "appointment_workflow",
            "section": "Overview & Architecture",
            "type": "appointment_architecture"
        }
    })

    for sec in sections[1:]:
        lines = sec.split("\n", 1)
        sec_title = lines[0].strip()
        sec_body = lines[1].strip() if len(lines) > 1 else ""
        
        full_chunk = f"## {sec_title}\n\n{sec_body}"
        chroma_docs.append({
            "text": full_chunk,
            "metadata": {
                "source": "appointment_workflow_skill.md",
                "module": "appointment_workflow",
                "section": sec_title[:60],
                "type": "appointment_section"
            }
        })

    print(f"\nAdding {len(chroma_docs)} detailed appointment workflow sections into ChromaDB...")
    added_ids = add_to_knowledge_base(chroma_docs)
    print(f"  ✓ Successfully indexed {len(added_ids)} appointment sections into ChromaDB!")

    print("\n" + "=" * 60)
    print("INDEXING COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    parse_and_seed()
