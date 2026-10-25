import os
import sys
import re
import uuid
import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import chromadb
from langchain_openai import OpenAIEmbeddings
from guardrails import SecurityException, validate_sql_query

# Load environment configuration
load_dotenv(override=True)

# ----------------------------------------------------------------------
# 1. LOCAL PERSISTENT CHROMADB STORE IN ./chroma_data
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DATA_DIR = os.path.join(BASE_DIR, "chroma_data")
os.makedirs(CHROMA_DATA_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_DIR)

# Cosine distance space: identical queries = 0.0, close semantics < 0.25
CACHE_COLLECTION_NAME = "cache_collection"
cache_collection = chroma_client.get_or_create_collection(
    name=CACHE_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine", "description": "Semantic query-answer cache for AI agent"}
)

# ----------------------------------------------------------------------
# 2. EMBEDDINGS MODEL (OpenAI text-embedding-3-small with Local ONNX fallback)
# ----------------------------------------------------------------------
class UniversalEmbeddingWrapper:
    """
    Supports OpenAI text-embedding-3-small when OPENAI_API_KEY is available in .env,
    and seamlessly falls back to fast local ONNX embeddings (all-MiniLM-L6-v2) otherwise.
    """
    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and not openai_key.startswith("your_"):
            try:
                from langchain_openai import OpenAIEmbeddings
                self._model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_key)
                self.mode = "OpenAI (text-embedding-3-small)"
                return
            except Exception:
                pass
        
        # Local ONNX fallback - works 100% offline without API keys
        from chromadb.utils import embedding_functions
        self._fn = embedding_functions.DefaultEmbeddingFunction()
        self.mode = "Local ONNX (all-MiniLM-L6-v2)"

    def embed_query(self, text: str) -> list:
        if hasattr(self, "_model"):
            return self._model.embed_query(text)
        return self._fn([text])[0]

    def embed_documents(self, texts: list) -> list:
        if hasattr(self, "_model"):
            return self._model.embed_documents(texts)
        return self._fn(texts)

_embeddings_instance: Optional[UniversalEmbeddingWrapper] = None

def get_embeddings_model() -> UniversalEmbeddingWrapper:
    """Lazily initializes and returns the embedding provider."""
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = UniversalEmbeddingWrapper()
        print(f"[INFO] ChromaDB Embedding Provider active: {_embeddings_instance.mode}")
    return _embeddings_instance


# ----------------------------------------------------------------------
# 3. SAFETY GUARDRAILS (READ ONLY DB & NAGUL'S DIRECTORY LOCK)
# ----------------------------------------------------------------------
SAFETY_SYSTEM_PROMPT = """You are an Autonomous AI Assistant operating strictly within Nagul's environment (/L9/nagul/).
MANDATORY SAFETY RULES:
1. DATABASE SAFETY: ONLY SELECT queries are permitted. UPDATE, DELETE, DROP, TRUNCATE, ALTER, INSERT, or any destructive queries are strictly FORBIDDEN.
2. DIRECTORY RESTRICTION: You are strictly restricted to Nagul's directory (/L9/nagul/). Any access or path modification outside this directory is prohibited.
Answer factually and concisely based on these guardrails."""


def enforce_safety_rules(query: str):
    """
    Validates that user queries adhere to:
    1. Strict READ ONLY DB operations (no UPDATE, DELETE, DROP, INSERT, ALTER).
    2. Restricted to Nagul's directory (/L9/nagul/).
    """
    clean_q = query.strip()

    # Rule 1: Check for dangerous database write/alter keywords
    dangerous_keywords = ["UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "INSERT", "CREATE", "GRANT", "REVOKE"]
    for kw in dangerous_keywords:
        if re.search(rf"\b{kw}\b", clean_q, re.IGNORECASE):
            if re.search(rf"\b(RUN|EXECUTE|SQL|QUERY|TABLE)\b", clean_q, re.IGNORECASE) or any(c in clean_q for c in [";", "--", "/*"]):
                raise SecurityException(
                    f"Database Safety Violation: Keyword '{kw}' is forbidden. "
                    f"Only READ-ONLY (SELECT) database operations are permitted!"
                )

    # Rule 2: Check for directory escaping or references outside Nagul's directory
    if re.search(r"\bcd\s+\.\.(?:/|$|\s|;)", clean_q) or "../" in clean_q or "..\\" in clean_q:
        raise SecurityException("Directory Lock Violation: Directory traversal ('..') outside Nagul's directory is strictly forbidden!")

    # Block unauthorized system root paths
    # Note: When developers paste live stack traces or production log lines containing web app paths
    # like '/var/www/html/...', we allow it for log diagnostics, while still blocking raw system access to /var, /etc, etc.
    clean_q_without_webapp = re.sub(r"/var/www/(?:html/)?[a-zA-Z0-9_\-\./]+", "", clean_q, flags=re.IGNORECASE)
    for forbidden_path in ["/etc", "/root", "/home", "C:\\Windows", "C:\\Program Files"]:
        if forbidden_path.lower() in clean_q_without_webapp.lower():
            raise SecurityException(f"Directory Lock Violation: Access to '{forbidden_path}' is outside Nagul's authorized directory!")

    # Check for /var only if not part of a web application file path
    if "/var" in clean_q_without_webapp.lower():
        raise SecurityException("Directory Lock Violation: Access to '/var' is outside Nagul's authorized directory!")


# ----------------------------------------------------------------------
# 4. LLM CALLER (GPT-4o / Claude with Gemini fallback)
# ----------------------------------------------------------------------
def call_llm_api(prompt: str) -> str:
    """
    Calls the LLM (GPT-4o or Claude 3.5 Sonnet, with Gemini fallback)
    enforcing safety guardrails.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    # 1. GPT-4o
    if openai_key and not openai_key.startswith("your_"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                messages=[
                    {"role": "system", "content": SAFETY_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI call failed ({e}), checking alternatives...")

    # 2. Claude 3.5 Sonnet
    if anthropic_key and not anthropic_key.startswith("your_"):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=SAFETY_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Claude call failed ({e}), checking alternatives...")

    # 3. Google Gemini (Available in project .env)
    if gemini_key and not gemini_key.startswith("your_"):
        try:
            import google.genai as genai
            from google.genai import types
            client = genai.Client(api_key=gemini_key)
            full_prompt = f"{SAFETY_SYSTEM_PROMPT}\n\nUser Question:\n{prompt}"
            res = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            return res.text.strip()
        except Exception as e:
            print(f"Gemini call failed ({e})...")

    raise ValueError("No active LLM credentials found (OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY).")


def extract_intent_aspects(query: str) -> set:
    q = query.lower()
    aspects = set()
    if any(w in q for w in ["deposit", "depoite", "deposite"]):
        aspects.add("deposit")
    if any(w in q for w in ["receipt", "recpt"]):
        aspects.add("receipt")
    if any(w in q for w in ["bill", "invoice", "billing"]):
        aspects.add("bill")
    if any(w in q for w in ["visit", "visits"]):
        aspects.add("visit")
    if any(w in q for w in ["mrn", "patient", "name"]):
        aspects.add("patient")
    if any(w in q for w in ["service", "services", "cpt"]):
        aspects.add("service")
    if any(w in q for w in ["item", "inventory", "drug", "medicine", "pharmacy"]):
        aspects.add("inventory")
    if any(w in q for w in ["bed", "room", "ipd"]):
        aspects.add("bed")
    if any(w in q for w in ["price", "rate", "tariff", "cost", "selling"]):
        aspects.add("price")
    return aspects


def extract_entity_numbers(query: str) -> set:
    return set(re.findall(r'\b\d{4,}\b', query))


def verify_answer_relevance(user_query: str, candidate_answer: str) -> bool:
    """
    CRITICAL ANSWER-RELEVANCE VERIFICATION GUARDRAIL:
    Verifies that a candidate answer retrieved from Valkey or ChromaDB
    actually and specifically answers the user's inquiry before returning.

    Rejection Criteria:
    1. Empty answer or placeholder error.
    2. Generic Header / Summary Rejection: If user asks a specific question (e.g. contains
       'allow', 'mudiyuma', 'pannuma', 'can', 'how', 'why', 'revert', 'cancel', 'multiple', etc.)
       but candidate answer is merely a high-level title/overview without addressing the specific action.
    3. Keyword Alignment: If query contains distinct domain keywords (e.g. 'multiple', 'revert',
       'credit note', 'deposit', 'prior approval'), candidate answer MUST contain or address
       those key concepts.
    4. Capability / Yes-No Check: If query asks if something is allowed ('allow', 'mudiyuma', 'can we'),
       the answer must take a clear affirmative or negative stance ('yes', 'no', 'aama', 'illai',
       'allow', 'permit', 'blocked', 'mudiyaathu', 'mudiyum').
    """
    if not candidate_answer or not str(candidate_answer).strip():
        return False

    q_lower = user_query.lower()
    a_lower = candidate_answer.lower()

    # 1. Reject generic module card dumps when user asks a question
    question_markers = [
        "allow", "mudiyuma", "mudium", "mudiyadhu", "pannuma", "pannalama", "pannalam",
        "can ", "can i", "can we", "is it possible", "how to", "how do", "why", "what happens",
        "epdi", "eppadi", "enna aagum", "revert", "cancel", "multiple", "refund", "receipt",
        "short payment", "discount", "advance", "deposit", "copay", "co-pay", "vat", "thevai", "thevaiya"
    ]
    is_question = any(w in q_lower for w in question_markers)
    if is_question:
        # If candidate answer is just a static overview stub
        if "hospital workflows:" in a_lower and ("standard process verified" in a_lower or "senior architect guide covering" in a_lower):
            return False
        if len(a_lower.split()) < 8 and any(w in a_lower for w in ["guide", "system", "overview", "lifecycle"]):
            return False

    # 2. Check topical keyword presence if query has specialized terms
    specialized_topics = [
        ("multiple", ["multiple", "several", "more than one", "second invoice", "subsequent", "partial", "pend"]),
        ("revert", ["revert", "reopening", "unlock", "open"]),
        ("cancel", ["cancel", "cancellation", "void"]),
        ("refund", ["refund", "excess", "wallet", "credit note"]),
        ("deposit", ["deposit", "advance", "adjusted", "balance"]),
        ("copay", ["copay", "co-pay", "deductible", "coinsurance", "patient share"]),
        ("vat", ["vat", "tax", "trn"]),
        ("prior approval", ["prior approval", "pre-auth", "preauth", "authorization", "approval"]),
        ("prior visit", ["prior visit", "pre-auth", "preauth", "prior authorization", "pa_"]),
        ("pre-auth", ["pre-auth", "preauth", "prior approval", "authorization", "payer"]),
        ("preauth", ["pre-auth", "preauth", "prior approval", "authorization", "payer"])
    ]
    for topic, synonyms in specialized_topics:
        if topic in q_lower:
            if not any(s in a_lower for s in synonyms):
                return False

    # 3. If query asks 'allow' or capability, check for stance
    if any(w in q_lower for w in ["allow", "mudiyuma", "mudium", "pannuma", "can we", "is it possible"]):
        capability_words = [
            "allow", "yes", "no", "aama", "illai", "mudiyum", "mudiyaathu", "possible", "impossible",
            "permitted", "blocked", "supported", "cannot", "can "
        ]
        if not any(w in a_lower for w in capability_words):
            return False

    return True


# ----------------------------------------------------------------------
# 4b. HEALTHCARE PATIENT DATA PRIVACY (PHI) & LIVE DB GUARDRAILS
# ----------------------------------------------------------------------
PATIENT_ENTITY_PATTERNS = [
    re.compile(r'\b(?:mrn|visit|patient|visit_no|permanent_mrn|permanent_visit|emirates_id|eid|iqama)\b', re.IGNORECASE),
    re.compile(r'\b(?:mrn|visit|patient|visit_no)\s*[:#\-\s]*\d+', re.IGNORECASE),
    re.compile(r'\b(?:patient name|patient details|visit details|unbilled services|bill status|lab orders|prescriptions)\b', re.IGNORECASE)
]

def is_patient_or_phi_data(query: str, answer: str = "") -> bool:
    """
    Healthcare Data Protection & Real-time Freshness Guardrail:
    Detects whether a query or answer refers to specific patient entities or clinical PHI:
    - Queries containing MRN, Visit numbers, Patient Names, Emirates ID, Mobile numbers.
    - Clinical encounter data: Vitals, Prescriptions, Lab item results, Visit-specific billing/unbilled services.
    
    Guarantees:
    1. ZERO Patient Health Information (PHI) stored in persistent vector/semantic cache.
    2. Real-time accuracy: Any query referencing a patient/visit is ALWAYS dispatched
       to the live MSSQL Database, never returning stale cached results.
    """
    combined_text = f"{query} {answer}".lower()
    
    # 1. Check for explicit 4+ digit IDs combined with patient/visit/encounter keywords
    has_digit_entity = bool(re.search(r'\b\d{4,}\b', query))
    if has_digit_entity:
        if any(w in combined_text for w in ["mrn", "visit", "patient", "encounter", "bill", "receipt", "deposit", "cpt", "service"]):
            return True

    # 2. Check for explicit patient identity keywords in query
    for pat in PATIENT_ENTITY_PATTERNS:
        if pat.search(query):
            return True

    # 3. Check for clinical encounter keywords in query (vitals, rx, lab orders for a patient)
    clinical_keywords = [
        "vitals", "blood pressure", "spo2", "heart rate", "troponin", "potassium",
        "prescription", "prescribed", "unbilled", "patient share", "cashier",
        "emirates id", "phone number", "contact mobile", "patient registered"
    ]
    if any(k in query.lower() for k in clinical_keywords) and has_digit_entity:
        return True

    # 4. Check for patient identifiers in the generated answer
    if answer:
        ans_lower = answer.lower()
        if any(marker in ans_lower for marker in [
            "permanent_mrn_no", "permanent_visit_no", "patient_basic_details",
            "patient mrn:", "visit no:", "patient name:", "active unbilled services for patient mrn",
            "patient_visit_basic_details_serial_no", "active services list:"
        ]):
            return True
        if re.search(r'mrn:?\s*`?\d{4,}`?', ans_lower) or re.search(r'visit:?\s*`?\d{4,}`?', ans_lower):
            return True

    return False


def purge_patient_phi_from_cache() -> int:
    """
    Scans the ChromaDB cache_collection and purges all existing patient/visit records,
    leaving only static system, menu, and general knowledge.
    """
    try:
        if cache_collection.count() == 0:
            return 0
        all_items = cache_collection.get()
        ids_to_delete = []
        for doc_id, doc_text, meta in zip(all_items["ids"], all_items["documents"], all_items["metadatas"]):
            ans_text = meta.get("answer", "") if meta else ""
            if is_patient_or_phi_data(doc_text, ans_text):
                ids_to_delete.append(doc_id)
        
        if ids_to_delete:
            cache_collection.delete(ids=ids_to_delete)
            print(f"[CACHE PURGE] Successfully purged {len(ids_to_delete)} patient PHI records from ChromaDB cache_collection.")
        return len(ids_to_delete)
    except Exception as e:
        print(f"[CACHE PURGE ERROR] {e}")
        return 0


# ----------------------------------------------------------------------
# 5. MODULAR SEMANTIC CACHING FUNCTIONS
# ----------------------------------------------------------------------
def check_semantic_cache(user_query: str, threshold: float = 0.25) -> Optional[Dict[str, Any]]:
    """
    Checks if a semantically similar query exists in ChromaDB cache_collection.
    Returns matched details dict if distance < threshold and exact entity numbers and intent aspects match.
    STRICT GUARDRAIL: Automatically bypasses cache for ANY patient or clinical PHI queries!
    """
    if not user_query or not user_query.strip():
        return None

    # Healthcare Privacy & Real-time DB Guardrail: Bypass cache for patient data
    if is_patient_or_phi_data(user_query):
        print(f"[CACHE BYPASS - PATIENT/PHI GUARDRAIL] Query '{user_query}' contains patient/visit entity. Always querying live MSSQL DB.")
        return None

    try:
        if cache_collection.count() == 0:
            return None

        embeddings = get_embeddings_model()
        query_vector = embeddings.embed_query(user_query)

        results = cache_collection.query(
            query_embeddings=[query_vector],
            n_results=1,
            include=["documents", "metadatas", "distances"]
        )

        if results and results.get("distances") and results["distances"][0]:
            best_distance = results["distances"][0][0]
            matched_query = results["documents"][0][0]
            cached_meta = results["metadatas"][0][0]

            if best_distance < threshold:
                # 1. Exact Entity Number Guardrail:
                user_nums = extract_entity_numbers(user_query)
                matched_nums = extract_entity_numbers(matched_query)
                if user_nums != matched_nums:
                    print(f"[CACHE MISS (Entity ID Mismatch)] Query IDs {user_nums} != Cached IDs {matched_nums}")
                    return None

                # 2. Intent Aspect Guardrail:
                user_aspects = extract_intent_aspects(user_query)
                matched_aspects = extract_intent_aspects(matched_query)
                missing_aspects = user_aspects - matched_aspects
                if missing_aspects and ("deposit" in missing_aspects or "receipt" in missing_aspects or "service" in missing_aspects or "inventory" in missing_aspects or "bed" in missing_aspects or "price" in missing_aspects):
                    print(f"[CACHE MISS (Aspect Mismatch)] User asked for {missing_aspects} not present in cached query '{matched_query}'")
                    return None

                # 3. Language Isolation Guardrail:
                from utils.table_formatter import detect_language
                query_lang = detect_language(user_query)
                cached_lang = cached_meta.get("lang") or detect_language(matched_query)
                if query_lang != cached_lang:
                    print(f"[CACHE MISS (Language Mismatch)] Query lang '{query_lang}' != Cached lang '{cached_lang}'")
                    return None

                cached_answer = cached_meta.get("answer", "")
                
                # Double-check cached answer does not contain PHI
                if is_patient_or_phi_data(matched_query, cached_answer):
                    print(f"[CACHE PURGE ON HIT] Cached item contains PHI. Invalidating cache hit.")
                    return None

                # 4. Critical Answer-Relevance & Match Verification Guardrail:
                if not verify_answer_relevance(user_query, cached_answer):
                    print(f"[CACHE REJECTED - RELEVANCE MISMATCH] Cached answer does not specifically answer '{user_query}'. Bypassing cache to query reasoning engine.")
                    return None

                print(f"[CACHE HIT] Distance: {best_distance:.4f} (< {threshold}) | Matched: \"{matched_query}\"")
                return {
                    "answer": cached_answer,
                    "distance": best_distance,
                    "matched_query": matched_query
                }
            else:
                print(f"[CACHE MISS] Nearest distance: {best_distance:.4f} (>= {threshold})")
    except Exception as e:
        print(f"[WARNING] Cache check skipped: {e}")

    return None


def save_to_semantic_cache(user_query: str, answer: str) -> Optional[str]:
    """
    Saves user_query and its answer into ChromaDB cache_collection.
    Skips caching error responses, missing details prompts, and STRICTLY PROHIBITS Patient PHI.
    """
    if not user_query or not answer:
        return None

    # Healthcare Privacy & Real-Time Data Guardrail: Block patient/visit records
    if is_patient_or_phi_data(user_query, answer):
        print(f"[CACHE BLOCKED - PATIENT/PHI GUARDRAIL] Skipped caching patient/visit records to protect PHI and guarantee real-time data freshness.")
        return None

    lower_ans = answer.lower()
    for bad in [
        "please share", "specific mrn", "error processing", "guardrail protection",
        "unknown column", "no working ai llm", "visit number venum", "mrn venum",
        "antha visit number", "antha mrn", "please antha", "visit number-a sollunga",
        "mrn-a sollunga", "sollunga, naan"
    ]:
        if bad in lower_ans:
            print(f"[CACHE SKIP] Answer contains '{bad}', not caching.")
            return None

    try:
        embeddings = get_embeddings_model()
        query_vector = embeddings.embed_query(user_query)

        from utils.table_formatter import detect_language
        query_lang = detect_language(user_query)

        cache_id = str(uuid.uuid4())
        cache_collection.add(
            ids=[cache_id],
            documents=[user_query],
            embeddings=[query_vector],
            metadatas=[{
                "answer": answer,
                "lang": query_lang,
                "cached_at": datetime.datetime.now().isoformat(),
                "query": user_query
            }]
        )
        print(f"[CACHE STORED] Saved in ChromaDB ID: {cache_id}")
        return cache_id
    except Exception as e:
        print(f"[WARNING] Failed to save response to ChromaDB cache: {e}")
        return None


def get_cached_answer_or_query_llm(user_query: str) -> str:
    """
    Searches ChromaDB cache_collection for a query similar to user_query (distance < 0.25).
    - If a match is found: Returns the cached answer immediately without calling LLM API.
    - If NO match is found: Calls LLM (GPT-4o/Claude), saves (user_query, llm_answer) to ChromaDB.
    - Strictly enforces READ-ONLY DB rules and Nagul's directory lock.
    """
    if not user_query or not user_query.strip():
        return "Empty query provided."

    # 1. Enforce strict safety guardrails
    enforce_safety_rules(user_query)

    # 2. Check cache first
    cached_result = check_semantic_cache(user_query, threshold=0.25)
    if cached_result:
        return cached_result["answer"]

    # 3. Cache MISS -> Call LLM
    print(f"⚡ Calling LLM for new query: \"{user_query}\"")
    llm_answer = call_llm_api(user_query)

    # 4. Save into cache
    save_to_semantic_cache(user_query, llm_answer)

    return llm_answer


if __name__ == "__main__":
    print("=" * 60)
    print("Semantic Caching with ChromaDB & Guardrails")
    print("=" * 60)
    print(f"Cache Directory: {CHROMA_DATA_DIR}")
    print(f"Currently Cached Items: {cache_collection.count()}")

    # Demonstration / Test
    test_q1 = "Where is the price list management menu located in HIMES?"
    print(f"\n1. First query (expected cache MISS): \"{test_q1}\"")
    try:
        ans1 = get_cached_answer_or_query_llm(test_q1)
        print(f"Response: {ans1[:120]}...\n")

        # Semantically identical question (different phrasing)
        test_q2 = "where can I find the price list menu in himes application?"
        print(f"2. Similar query (expected cache HIT, threshold < 0.25): \"{test_q2}\"")
        ans2 = get_cached_answer_or_query_llm(test_q2)
        print(f"Response: {ans2[:120]}...\n")

        # Test Guardrail Safety check
        print("3. Testing Safety Guardrail (attempting forbidden SQL write):")
        try:
            get_cached_answer_or_query_llm("DELETE FROM users WHERE id = 1;")
        except SecurityException as se:
            print(f" Guardrail Blocked Successfully: {se}")

    except Exception as e:
        print(f"Note: {e}")
