import os
import sys
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

load_dotenv(override=True)

from memory_manager import add_to_knowledge_base, search_knowledge_base
from ssh_sandbox import sandboxed_ssh

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_RULES_FILE = os.path.join(BASE_DIR, "project_rules.txt")
MODULES_KNOWLEDGE_FILE = os.path.join(BASE_DIR, "modules_knowledge.md")
LOCAL_LOG_FILE = os.path.join(BASE_DIR, "storage", "logs", "laravel.log")
REMOTE_LOG_PATH = "/L9/nagul/himes-ai/storage/logs/laravel.log"


def load_modules_knowledge(file_path: str = MODULES_KNOWLEDGE_FILE) -> List[Dict[str, Any]]:
    """
    Reads the extracted modules_knowledge.md documentation and splits each
    module's controllers, routes, models, and schemas into structured ChromaDB chunks.
    """
    if not os.path.exists(file_path):
        print(f"[WARNING] Modules knowledge file not found at: {file_path}")
        return []

    print(f"Reading extracted modules knowledge from: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by module header: ## 📌 Module: ...
    raw_modules = re.split(r"(?=##\s+📌\s+Module:)", content)
    documents = []

    for mod_text in raw_modules:
        clean_text = mod_text.strip()
        if not clean_text or not clean_text.startswith("##"):
            continue

        header_match = re.search(r"##\s+📌\s+Module:\s+([^\n\r]+)", clean_text)
        mod_name = header_match.group(1).strip() if header_match else "Unknown Module"

        # Further chunk module if too large into Subsections (Controllers, Routes, Tables)
        subsections = re.split(r"(?=###\s+\d+\.)", clean_text)
        for sub in subsections:
            sub_clean = sub.strip()
            if not sub_clean:
                continue
            
            sub_header = re.search(r"###\s+(\d+\.\s+[^\n\r]+)", sub_clean)
            sub_title = sub_header.group(1).strip() if sub_header else "Overview"

            full_chunk_text = f"HIMES Module [{mod_name}] - {sub_title}:\n\n{sub_clean}"

            documents.append({
                "text": full_chunk_text,
                "metadata": {
                    "source": "modules_knowledge.md",
                    "module": mod_name,
                    "section": sub_title,
                    "category": "module_architecture_and_schema"
                }
            })

    print(f"   Parsed {len(documents)} module knowledge section(s).")
    return documents


def load_project_rules(file_path: str = PROJECT_RULES_FILE) -> List[Dict[str, Any]]:
    """
    Reads the project structure & rules text file, and chunks it into
    structured knowledge entries for ChromaDB.
    """
    if not os.path.exists(file_path):
        print(f"[WARNING] Project rules file not found at: {file_path}")
        return []

    print(f"Reading project rules from: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    raw_sections = re.split(r"(?=\[MODULE\s+\d+:)", content)
    documents = []

    for section in raw_sections:
        clean_text = section.strip()
        if not clean_text or clean_text.startswith("#"):
            continue

        header_match = re.search(r"\[(MODULE\s+\d+:[^\]]+)\]", clean_text)
        section_name = header_match.group(1) if header_match else "General Rules"

        documents.append({
            "text": clean_text,
            "metadata": {
                "source": "project_rules.txt",
                "section": section_name,
                "category": "architecture_and_safety"
            }
        })

    print(f"   Parsed {len(documents)} rule module(s).")
    return documents


def load_laravel_logs(max_lines: int = 150) -> List[Dict[str, Any]]:
    """
    Reads the most recent entries from Laravel storage/logs/laravel.log.
    Supports either local log file or fetches live from remote server via SSH.
    """
    raw_log = ""

    # 1. Try local file if present
    if os.path.exists(LOCAL_LOG_FILE):
        print(f"📋 Reading local Laravel log: {LOCAL_LOG_FILE}")
        try:
            with open(LOCAL_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                raw_log = "".join(lines[-max_lines:])
        except Exception as e:
            print(f"⚠️ Could not read local log: {e}")

    # 2. Otherwise fetch the latest lines from remote server via SSH
    if not raw_log.strip():
        print(f"📋 Fetching latest {max_lines} log lines from remote server ({REMOTE_LOG_PATH})...")
        try:
            raw_log = sandboxed_ssh.execute_sandboxed_command(
                f"tail -n {max_lines} {REMOTE_LOG_PATH}",
                working_dir="/L9/nagul/himes-ai"
            )
        except Exception as e:
            print(f"⚠️ Could not fetch remote logs: {e}")

    if not raw_log.strip():
        print("   No log entries found.")
        return []

    # Extract distinct error/exception blocks starting with [YYYY-MM-DD
    log_blocks = re.split(r"(?=\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\])", raw_log)
    documents = []

    for block in log_blocks:
        clean_block = block.strip()
        if not clean_block:
            continue

        # Capture timestamp and log level (e.g. laravel.ERROR, laravel.EMERGENCY)
        first_line = clean_block.splitlines()[0] if clean_block.splitlines() else "Laravel Log"
        level_match = re.search(r"laravel\.([A-Z]+):", first_line)
        log_level = level_match.group(1) if level_match else "INFO"

        # Truncate overly long stack traces to fit embedding context cleanly
        trimmed_block = clean_block[:1500]

        documents.append({
            "text": trimmed_block,
            "metadata": {
                "source": "laravel.log",
                "level": log_level,
                "first_line": first_line[:100],
                "category": "application_logs"
            }
        })

    print(f"   Parsed {len(documents)} recent log/error block(s).")
    return documents


def train():
    """
    Main training function:
    1. Loads project rules & architecture.
    2. Loads recent Laravel error logs.
    3. Feeds them into ChromaDB knowledge base via add_to_knowledge_base().
    4. Tests retrieval with search_knowledge_base().
    """
    print("=" * 65)
    print(" CHROMADB KNOWLEDGE BASE TRAINING SCRIPT")
    print("=" * 65)

    all_docs: List[Dict[str, Any]] = []

    # 1. Load Extracted Modules Knowledge Base (Controllers, Models, Routes, Schemas)
    modules_docs = load_modules_knowledge()
    all_docs.extend(modules_docs)

    # 2. Load Project Rules & Architecture
    rules_docs = load_project_rules()
    all_docs.extend(rules_docs)

    # 3. Load Laravel Error Logs
    logs_docs = load_laravel_logs(max_lines=150)
    all_docs.extend(logs_docs)

    print(f"\nTotal documents prepared for ChromaDB: {len(all_docs)}")

    if not all_docs:
        print("[WARNING] No documents available to train. Exiting.")
        return

    # 3. Add to ChromaDB Knowledge Base
    print("\n🧠 Converting to Embeddings (OpenAI text-embedding-3-small) and storing in ChromaDB...")
    try:
        inserted_ids = add_to_knowledge_base(all_docs)
        print(f" Training Successful! Stored {len(inserted_ids)} records in ChromaDB.\n")

        # 4. Verify Retrieval with Sample Queries
        test_queries = [
            "What are the database safety rules for SQL queries?",
            "What is the directory lock rule for Nagul's environment?",
            "What is the recent error in laravel.log?"
        ]

        print("=" * 65)
        print(" VERIFYING KNOWLEDGE RETRIEVAL FROM CHROMADB")
        print("=" * 65)

        for q in test_queries:
            print(f"\n🔍 Query: \"{q}\"")
            results = search_knowledge_base(q, limit=1)
            if results:
                matched = results[0]
                print(f"   Matched Section: {matched['metadata'].get('section') or matched['metadata'].get('first_line')}")
                print(f"   Excerpt: {matched['document'][:180]}...")
            else:
                print("   No match found.")

    except ValueError as ve:
        print(f"\n⚠️ Notice: {ve}")
    except Exception as e:
        print(f"\n⚠️ Error during ChromaDB ingestion: {e}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    train()
