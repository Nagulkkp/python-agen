"""
valkey_himes_manager.py
=======================
Valkey (In-Memory Redis-compatible Data Store) Manager for HIMES AI Agent.

Accelerates HIMES Application knowledge retrieval, session persistence,
module workflow caching, and distributed folder locks alongside ChromaDB.

Features:
1. Valkey Connection Setup: Connects to local or remote Valkey/Redis instance on default port 6379,
   with graceful in-memory fallback if the service is temporarily unreachable.
2. HIMES Module Flow Caching: Instant retrieval of pre-seeded and dynamically cached HIMES workflows.
3. Smart Hybrid Search (Valkey + ChromaDB):
   - Fast-path: Instant in-memory cache hit in sub-milliseconds from Valkey.
   - Slow-path: Fallback to ChromaDB vector search (`search_knowledge_base`), then auto-caches
     the result into Valkey for future requests.
4. HIMES Session & State Store: Multi-turn chat session state and active module tracking.
5. Nagul Folder Lock: Atomic distributed lock to prevent concurrent file modifications in /L9/nagul/himes-ai.
"""

import os
import sys
import json
import time
import uuid
import hashlib
from typing import Dict, Any, Optional, List, Union
from contextlib import contextmanager
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure .env is loaded
load_dotenv(override=True)

# Attempt importing valkey first, fallback to redis
try:
    import valkey
    VALKEY_CLIENT_CLASS = valkey.Valkey
    VALKEY_POOL_CLASS = valkey.ConnectionPool
    VALKEY_BACKEND_NAME = "Valkey"
except ImportError:
    try:
        import redis
        VALKEY_CLIENT_CLASS = redis.Redis
        VALKEY_POOL_CLASS = redis.ConnectionPool
        VALKEY_BACKEND_NAME = "Redis (Valkey-compatible)"
    except ImportError:
        VALKEY_CLIENT_CLASS = None
        VALKEY_POOL_CLASS = None
        VALKEY_BACKEND_NAME = "InMemoryFallback"

# Import ChromaDB search from existing memory manager
try:
    from memory_manager import search_knowledge_base, add_to_knowledge_base
    CHROMADB_AVAILABLE = True
except Exception as e:
    CHROMADB_AVAILABLE = False
    print(f"[ValkeyManager] Warning: ChromaDB memory_manager not loaded: {e}")


class ValkeyHimesManager:
    """
    Manages Valkey in-memory operations, hybrid search with ChromaDB,
    session state tracking, and execution locks for HIMES.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None,
        db: Optional[int] = None,
        socket_timeout: float = 2.0
    ):
        # Resolve configuration from parameters or environment
        self.host = host or os.getenv("VALKEY_HOST", "192.168.20.152")
        self.port = port or int(os.getenv("VALKEY_PORT", "6379"))
        self.password = password or os.getenv("VALKEY_PASSWORD") or None
        self.db = db if db is not None else int(os.getenv("VALKEY_DB", "0"))
        self.socket_timeout = socket_timeout

        self._client = None
        self._pool = None
        self._connected = False
        self._fallback_store: Dict[str, Any] = {}
        self._fallback_expiry: Dict[str, float] = {}

        self._init_connection()
        self._seed_default_himes_flows()

    # ----------------------------------------------------------------------
    # 1. VALKEY CONNECTION SETUP
    # ----------------------------------------------------------------------
    def _init_connection(self):
        """Establishes connection to the Valkey instance with ping verification."""
        if not VALKEY_CLIENT_CLASS:
            print("[ValkeyManager] valkey/redis client library not installed. Running in In-Memory fallback mode.")
            self._connected = False
            return

        try:
            connect_kwargs = {
                "host": self.host,
                "port": self.port,
                "db": self.db,
                "socket_timeout": self.socket_timeout,
                "socket_connect_timeout": self.socket_timeout,
                "decode_responses": True,
            }
            if self.password and not self.password.startswith("your_"):
                connect_kwargs["password"] = self.password

            self._pool = VALKEY_POOL_CLASS(**connect_kwargs)
            self._client = VALKEY_CLIENT_CLASS(connection_pool=self._pool)

            # Test connection with PING
            if self._client.ping():
                self._connected = True
                print(f"[ValkeyManager] Connected to {VALKEY_BACKEND_NAME} at {self.host}:{self.port} (DB: {self.db})")
        except Exception as e:
            self._connected = False
            self._client = None
            print(f"[ValkeyManager] Notice: Could not connect to Valkey at {self.host}:{self.port} ({e}). Using robust In-Memory fallback.")

    @property
    def is_connected(self) -> bool:
        """Returns True if live Valkey server is connected and responsive."""
        if not self._connected or not self._client:
            return False
        try:
            return bool(self._client.ping())
        except Exception:
            self._connected = False
            return False

    def get_client(self):
        """Returns the active Valkey client, or None if in fallback mode."""
        if self.is_connected:
            return self._client
        return None

    # ----------------------------------------------------------------------
    # INTERNAL HELPERS FOR STORAGE & EXPIRY (Works with Valkey or Fallback)
    # ----------------------------------------------------------------------
    def _set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        val_str = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
        if self.is_connected:
            try:
                if ttl:
                    return bool(self._client.setex(key, ttl, val_str))
                return bool(self._client.set(key, val_str))
            except Exception as e:
                print(f"[ValkeyManager] Error in SET {key}: {e}")

        # Fallback in-memory dictionary
        self._fallback_store[key] = val_str
        if ttl:
            self._fallback_expiry[key] = time.time() + ttl
        elif key in self._fallback_expiry:
            del self._fallback_expiry[key]
        return True

    def _get(self, key: str) -> Optional[Any]:
        if self.is_connected:
            try:
                val = self._client.get(key)
                if val is not None:
                    try:
                        return json.loads(val)
                    except Exception:
                        return val
                return None
            except Exception as e:
                print(f"[ValkeyManager] Error in GET {key}: {e}")

        # Fallback check
        if key in self._fallback_store:
            exp = self._fallback_expiry.get(key)
            if exp and time.time() > exp:
                del self._fallback_store[key]
                del self._fallback_expiry[key]
                return None
            val = self._fallback_store[key]
            try:
                return json.loads(val)
            except Exception:
                return val
        return None

    def _delete(self, key: str) -> bool:
        deleted = False
        if self.is_connected:
            try:
                deleted = bool(self._client.delete(key))
            except Exception:
                pass
        if key in self._fallback_store:
            del self._fallback_store[key]
            deleted = True
        if key in self._fallback_expiry:
            del self._fallback_expiry[key]
        return deleted

    # ----------------------------------------------------------------------
    # 2. HIMES MODULE FLOW CACHING
    # ----------------------------------------------------------------------
    def cache_himes_flow(self, module_name: str, flow_data: Union[dict, list, str], ttl: int = 86400) -> bool:
        """
        Caches a key HIMES workflow/module schema into Valkey with a TTL (default 24h).
        Key Format: `himes:flow:{module_name}`
        """
        clean_name = module_name.strip().lower().replace(" ", "_").replace("-", "_")
        key = f"himes:flow:{clean_name}"
        payload = {
            "module_name": module_name,
            "cached_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": flow_data
        }
        success = self._set(key, payload, ttl=ttl)
        if success:
            print(f"[ValkeyManager] Cached HIMES flow: '{module_name}' (TTL: {ttl}s)")
        return success

    def get_himes_flow(self, module_name: str) -> Optional[Any]:
        """
        Retrieves a cached HIMES workflow by module name in milliseconds.
        """
        clean_name = module_name.strip().lower().replace(" ", "_").replace("-", "_")
        key = f"himes:flow:{clean_name}"
        res = self._get(key)
        if res and isinstance(res, dict) and "data" in res:
            return res["data"]
        return res

    def invalidate_himes_flow(self, module_name: str) -> bool:
        """Deletes a cached HIMES module flow from Valkey."""
        clean_name = module_name.strip().lower().replace(" ", "_").replace("-", "_")
        key = f"himes:flow:{clean_name}"
        return self._delete(key)

    # ----------------------------------------------------------------------
    # 2B. GENERAL & CLINICAL SOP CACHING
    # ----------------------------------------------------------------------
    def set_cached_data(self, key: str, value: Any, ttl_seconds: int = 86400) -> bool:
        """Sets any structured JSON or string data in Valkey with TTL."""
        return self._set(key, value, ttl=ttl_seconds)

    def get_cached_data(self, key: str) -> Optional[Any]:
        """Gets cached data from Valkey by key."""
        return self._get(key)

    def get_clinical_sop(self, slug_or_query: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a clinical SOP protocol from Valkey by slug or keyword in sub-milliseconds.
        Key Format: `himes:clinical:sop:{slug}`
        """
        clean = slug_or_query.strip().lower().replace(" ", "_").replace("-", "_")
        # Direct key lookup
        data = self._get(f"himes:clinical:sop:{clean}")
        if data:
            return data
        
        # Keyword alias matching
        aliases = {
            "triage": "emergency_triage_protocol",
            "esi": "emergency_triage_protocol",
            "emergency": "emergency_triage_protocol",
            "icu": "icu_admission_discharge_criteria",
            "intensive_care": "icu_admission_discharge_criteria",
            "code_blue": "code_blue_cardiac_arrest_sop",
            "cardiac_arrest": "code_blue_cardiac_arrest_sop",
            "resuscitation": "code_blue_cardiac_arrest_sop",
            "antibiotic": "antibiotic_stewardship_policy",
            "stewardship": "antibiotic_stewardship_policy",
            "restricted_antibiotic": "antibiotic_stewardship_policy",
            "panic_values": "lis_result_verification_critical_values_and_dispatch_sop",
            "critical_values": "lis_result_verification_critical_values_and_dispatch_sop",
            "panic": "lis_result_verification_critical_values_and_dispatch_sop",
            "vacutainer": "lis_specimen_collection_and_preanalytics_sop",
            "tube_colors": "lis_specimen_collection_and_preanalytics_sop",
            "blood_collection": "lis_specimen_collection_and_preanalytics_sop",
            "microbiology": "lis_microbiology_culture_and_ast_guidelines",
            "culture_ast": "lis_microbiology_culture_and_ast_guidelines",
            "ast": "lis_microbiology_culture_and_ast_guidelines",
            "qc": "lis_analytical_testing_and_qc_protocols",
            "westgard": "lis_analytical_testing_and_qc_protocols",
            "tat": "lis_result_verification_critical_values_and_dispatch_sop",
            "turnaround": "lis_result_verification_critical_values_and_dispatch_sop",
            "insurance_billing": "hospital_billing_insurance_policy",
            "preauth": "hospital_billing_insurance_policy",
            "tpa": "hospital_billing_insurance_policy",
        }
        for k, target_slug in aliases.items():
            if k in clean:
                data = self._get(f"himes:clinical:sop:{target_slug}")
                if data:
                    return data
        return None

    def get_panic_values_master(self) -> Dict[str, Any]:
        """Retrieves authoritative master table of critical/panic values from Valkey."""
        res = self._get("himes:clinical:panic_values")
        return res if isinstance(res, dict) else {}

    def evaluate_panic_value(self, analyte_name: str, value: float) -> Optional[Dict[str, Any]]:
        """
        Evaluates a patient's numerical test result against the authoritative
        hospital panic value thresholds. Returns an alert dict if value is critical.
        """
        master = self.get_panic_values_master()
        if not master:
            return None
        
        clean_name = analyte_name.strip().lower().replace(" ", "_")
        for key, entry in master.items():
            if key in clean_name or entry.get("analyte", "").lower() in clean_name:
                low = entry.get("low_critical")
                high = entry.get("high_critical")
                unit = entry.get("unit", "")
                risk = entry.get("clinical_significance", "Life-threatening risk")
                analyte = entry.get("analyte", analyte_name)

                if low is not None and isinstance(low, (int, float)) and value < low:
                    return {
                        "is_panic": True,
                        "level": "PANIC_LOW",
                        "analyte": analyte,
                        "value": value,
                        "unit": unit,
                        "threshold": f"< {low}",
                        "clinical_significance": risk,
                        "alert_banner": f"🚨 **CRITICAL / PANIC LOW ALERT:** {analyte} is **{value} {unit}** (Critical Threshold: < {low} {unit}). Immediate physician escalation required within 15 minutes! Risk: {risk}."
                    }
                if high is not None and isinstance(high, (int, float)) and value > high:
                    return {
                        "is_panic": True,
                        "level": "PANIC_HIGH",
                        "analyte": analyte,
                        "value": value,
                        "unit": unit,
                        "threshold": f"> {high}",
                        "clinical_significance": risk,
                        "alert_banner": f"🚨 **CRITICAL / PANIC HIGH ALERT:** {analyte} is **{value} {unit}** (Critical Threshold: > {high} {unit}). Immediate physician escalation required within 15 minutes! Risk: {risk}."
                    }
        return None

    def _seed_default_himes_flows(self):
        """
        Pre-seeds core HIMES application workflows so they are instantly
        available in sub-milliseconds without querying MSSQL or ChromaDB.
        """
        default_flows = {
            "patient_billing": {
                "description": "HIMES Patient Billing & Invoicing Workflow",
                "rules": [
                    "Billing Status: Check Patient_Bill_Header via Patient_Visit_Basic_Details_Serial_No AND Bill_Cancellation_Flag = 'N'.",
                    "Finalized: Is_Bill_Finalized = 'C' indicates finalized bill. Bill No = Bill_No, Net = Bill_Net_Value.",
                    "Unbilled: No Patient_Bill_Header record means visit is Unbilled / Pending.",
                    "Price Resolution: If unbilled, fetch configuration prices: Cash uses Service_Rate_For_Non_Insurance, Insurance uses Service_Rate_For_Insurance.",
                    "Latest Date Rule: Always select TOP 1 ... WHERE Start_Date <= GETDATE() ORDER BY Start_Date DESC."
                ]
            },
            "deposits_and_receipts": {
                "description": "HIMES Deposit Collection & Receipt Payments Workflow (editPatientBilling)",
                "rules": [
                    "Receipt Number: Displayed in UI grid as pbpr.Patient_Bill_Header_Payments_Received_Serial_No (e.g. 55875).",
                    "Receipt Amount: Paid by patient via pbpr.Bill_Amount_Paid_By_Patient (e.g. 20.00 AED).",
                    "Card Reference: receipts_for_payments_received rpr.Card_Reference_Details.",
                    "Bill Total vs Receipt: Bill Net Value is total bill, Bill_Insured_Value is insurance claim, pbpr is patient share.",
                    "Deposits: Check Patient_Visit_Deposits pvd. Balance_Deposit_Amount indicates unadjusted deposit."
                ]
            },
            "inventory_pricing": {
                "description": "HIMES Pharmacy & Consumables Pricing Architecture",
                "rules": [
                    "Cash Price: Stock_Item_Price.Selling_Price WHERE Stock_Item_Price_Effective_Date <= GETDATE() ORDER BY Stock_Item_Price_Effective_Date DESC.",
                    "Insurance Price: Stock_Item_Insurance_Price.Insurance_Gross_Amount WHERE Effective_Date <= GETDATE() ORDER BY Effective_Date DESC."
                ]
            },
            "bed_management": {
                "description": "HIMES IPD Bed & Room Charges Architecture (getBillingBedManagementGrid)",
                "rules": [
                    "Bed Link: Patient_Visit_Resources -> Resource_Service -> Service_USSDB.",
                    "Bed Cash Rate: Service_Rate_For_Non_Insurance.Service_Base_Rate WHERE Start_Date <= GETDATE().",
                    "Bed Insurance Rate: Resource_Rate_For_Insurance.Resource_Base_Rate WHERE Start_Date <= GETDATE()."
                ]
            },
            "patient_registration": {
                "description": "HIMES Patient Registration & Encounter Architecture",
                "rules": [
                    "Patient Master: Patient_Basic_Details pbd (MRN = Permanent_MRN_No).",
                    "Patient Encript: Patient_Basic_Encript_Details pbed (Patient_First_Name, Patient_Last_Name, Contact_Phone_Mobile).",
                    "Encounters: Patient_Visit_Basic_Details pvbd (Permanent_Visit_No, Patient_Visit_Registered_Date_Time, Active_Status = 'A')."
                ]
            }
        }

        for name, flow in default_flows.items():
            key = f"himes:flow:{name}"
            # Only set if not already in cache
            if not self._get(key):
                self.cache_himes_flow(name, flow, ttl=86400)

    # ----------------------------------------------------------------------
    # 3. SMART HYBRID SEARCH (Valkey In-Memory + ChromaDB Vector Store)
    # ----------------------------------------------------------------------
    def get_himes_context(self, user_query: str, limit: int = 3, ttl: int = 3600) -> Dict[str, Any]:
        """
        Executes a high-performance Smart Hybrid Search:
        1. Fast-Path: Checks Valkey for an exact query hash match or module workflow.
           Returns instant in-memory context in sub-milliseconds.
        2. Slow-Path: On cache miss, queries ChromaDB's vector knowledge base (`search_knowledge_base`).
        3. Auto-Cache: Automatically stores the retrieved ChromaDB context into Valkey
           under `himes:query_cache:{hash}` with a TTL for instant subsequent access.

        Returns:
            Dict containing 'source' ('valkey_in_memory' or 'chromadb_vector_store'),
            'retrieval_ms', 'cache_hit', and 'context'.
        """
        start_time = time.perf_counter()
        normalized_query = " ".join(user_query.strip().lower().split())
        query_hash = hashlib.sha256(normalized_query.encode("utf-8")).hexdigest()[:16]
        cache_key = f"himes:query_cache:{query_hash}"

        # ------------------------------------------------------------------
        # Step 1: Check Valkey Exact Query Cache (Instant Hit)
        # ------------------------------------------------------------------
        cached_result = self._get(cache_key)
        if cached_result:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "status": "success",
                "source": "valkey_in_memory",
                "cache_hit": True,
                "retrieval_ms": round(elapsed_ms, 2),
                "query": user_query,
                "context": cached_result
            }

        # ------------------------------------------------------------------
        # Step 1b: Check Valkey Pre-seeded Module Flows based on keywords
        # ------------------------------------------------------------------
        matched_flow = None
        if any(w in normalized_query for w in ["billing", "bill", "invoice", "cpt"]):
            matched_flow = self.get_himes_flow("patient_billing")
        elif any(w in normalized_query for w in ["deposit", "receipt", "advance", "refund", "share"]):
            matched_flow = self.get_himes_flow("deposits_and_receipts")
        elif any(w in normalized_query for w in ["bed", "room", "ipd", "admission"]):
            matched_flow = self.get_himes_flow("bed_management")
        elif any(w in normalized_query for w in ["inventory", "pharmacy", "drug", "item price", "medicine"]):
            matched_flow = self.get_himes_flow("inventory_pricing")
        elif any(w in normalized_query for w in ["patient", "mrn", "register", "encounter", "visit"]):
            matched_flow = self.get_himes_flow("patient_registration")

        # ------------------------------------------------------------------
        # Step 2: Query ChromaDB Vector Knowledge Base on cache miss
        # ------------------------------------------------------------------
        chroma_docs = []
        if CHROMADB_AVAILABLE:
            try:
                chroma_results = search_knowledge_base(user_query, limit=limit)
                for r in chroma_results:
                    chroma_docs.append({
                        "id": r.get("id"),
                        "text": r.get("document"),
                        "metadata": r.get("metadata", {}),
                        "distance": r.get("distance")
                    })
            except Exception as e:
                print(f"[ValkeyManager] ChromaDB vector search exception: {e}")

        # Combine vector results with module flow if matched
        combined_context = {
            "flow_guidance": matched_flow,
            "vector_documents": chroma_docs,
            "source_query": user_query
        }

        # ------------------------------------------------------------------
        # Step 3: Automatically save into Valkey for future instant access
        # ------------------------------------------------------------------
        self._set(cache_key, combined_context, ttl=ttl)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "success",
            "source": "chromadb_vector_store",
            "cache_hit": False,
            "retrieval_ms": round(elapsed_ms, 2),
            "query": user_query,
            "context": combined_context
        }

    # ----------------------------------------------------------------------
    # 4. HIMES SESSION & STATE STORE
    # ----------------------------------------------------------------------
    def save_session_state(self, session_id: str, state_data: dict, ttl: int = 86400) -> bool:
        """
        Stores active user/agent chat session state in Valkey (TTL default: 24h).
        Key Format: `himes:session:{session_id}`
        """
        key = f"himes:session:{session_id}"
        return self._set(key, state_data, ttl=ttl)

    def get_session_state(self, session_id: str) -> dict:
        """
        Retrieves active session state (entities, history, context) in milliseconds.
        """
        key = f"himes:session:{session_id}"
        res = self._get(key)
        if isinstance(res, dict):
            return res
        return {
            "session_id": session_id,
            "active_entities": {"visit_no": None, "mrn": None, "bill_no": None},
            "active_module": None,
            "turns": []
        }

    def set_active_module(self, session_id: str, module_name: str, ttl: int = 86400) -> bool:
        """
        Records the current module being worked on by the user or agent
        (e.g., 'PatientBilling', 'BedManagement', 'EMR').
        """
        sess = self.get_session_state(session_id)
        sess["active_module"] = module_name
        sess["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return self.save_session_state(session_id, sess, ttl=ttl)

    def get_active_module(self, session_id: str) -> Optional[str]:
        """Returns the current active module for the session."""
        sess = self.get_session_state(session_id)
        return sess.get("active_module")

    def update_session_entities(self, session_id: str, entities: dict) -> dict:
        """
        Updates active entities (visit_no, mrn, bill_no) in Valkey session storage.
        """
        sess = self.get_session_state(session_id)
        if "active_entities" not in sess:
            sess["active_entities"] = {}
        for k, v in entities.items():
            if v:
                sess["active_entities"][k] = v
        self.save_session_state(session_id, sess)
        return sess

    def set_session_mode(self, session_id: str, mode: str, ttl: int = 86400) -> bool:
        """
        Stores current mode ('user' or 'developer') for session under chat_session:{session_id}:mode.
        """
        clean_mode = "developer" if str(mode).lower() in ["developer", "dev", "true", "1"] else "user"
        key = f"chat_session:{session_id}:mode"
        return self._set(key, clean_mode, ttl=ttl)

    def get_session_mode(self, session_id: str) -> str:
        """
        Retrieves current mode for session from chat_session:{session_id}:mode. Default is 'user'.
        """
        key = f"chat_session:{session_id}:mode"
        val = self._get(key)
        if isinstance(val, str) and val.strip().lower() in ["developer", "dev"]:
            return "developer"
        return "user"

    def clear_session_state(self, session_id: str) -> bool:
        """Removes session state from Valkey."""
        key = f"himes:session:{session_id}"
        self._delete(f"chat_session:{session_id}:mode")
        return self._delete(key)

    # ----------------------------------------------------------------------
    # 5. TEMPORARY EXECUTION LOCKS (Nagul Folder Lock)
    # ----------------------------------------------------------------------
    def acquire_nagul_folder_lock(
        self,
        lock_name: str = "nagul_folder_lock",
        timeout: int = 60,
        owner_id: Optional[str] = None
    ) -> bool:
        """
        Acquires an atomic distributed lock in Valkey to prevent concurrent
        file modifications or simultaneous git commits in /L9/nagul/himes-ai.

        Args:
            lock_name: Identifier for the lock (default: 'nagul_folder_lock').
            timeout: Maximum hold time in seconds before auto-expiration (default: 60s).
            owner_id: Unique string identifying the worker/thread holding the lock.

        Returns:
            True if the lock was acquired, False if already held by another task.
        """
        owner = owner_id or str(uuid.uuid4())
        key = f"himes:lock:{lock_name}"

        if self.is_connected:
            try:
                # Atomic SET with NX (not exists) and EX (expiry seconds)
                acquired = self._client.set(key, owner, nx=True, ex=timeout)
                if acquired:
                    return True
                return False
            except Exception as e:
                print(f"[ValkeyManager] Lock acquisition error: {e}")

        # In-memory lock fallback
        now = time.time()
        if key in self._fallback_store:
            exp = self._fallback_expiry.get(key, 0)
            if now < exp:
                return False  # Still locked
        self._fallback_store[key] = owner
        self._fallback_expiry[key] = now + timeout
        return True

    def release_nagul_folder_lock(
        self,
        lock_name: str = "nagul_folder_lock",
        owner_id: Optional[str] = None
    ) -> bool:
        """
        Releases the lock. If owner_id is provided, safely releases ONLY
        if the caller is the current lock holder (prevents releasing expired/overwritten locks).
        """
        key = f"himes:lock:{lock_name}"

        if self.is_connected:
            try:
                if owner_id:
                    # Safe atomic Lua script release
                    lua_script = """
                    if redis.call("get", KEYS[1]) == ARGV[1] then
                        return redis.call("del", KEYS[1])
                    else
                        return 0
                    end
                    """
                    res = self._client.eval(lua_script, 1, key, owner_id)
                    return bool(res)
                return bool(self._client.delete(key))
            except Exception as e:
                print(f"[ValkeyManager] Lock release error: {e}")

        # In-memory fallback release
        if key in self._fallback_store:
            if owner_id and self._fallback_store.get(key) != owner_id:
                return False
            del self._fallback_store[key]
            if key in self._fallback_expiry:
                del self._fallback_expiry[key]
            return True
        return False

    @contextmanager
    def nagul_folder_lock_context(self, lock_name: str = "nagul_folder_lock", timeout: int = 60):
        """
        Context manager for safe execution lock:
        Usage:
            with valkey_manager.nagul_folder_lock_context():
                # Perform critical file edit / git commit
        """
        owner = str(uuid.uuid4())
        acquired = self.acquire_nagul_folder_lock(lock_name, timeout=timeout, owner_id=owner)
        if not acquired:
            raise TimeoutError(f"Could not acquire execution lock '{lock_name}': Resource currently busy.")
        try:
            yield owner
        finally:
            self.release_nagul_folder_lock(lock_name, owner_id=owner)


# Global singleton instance
valkey_manager = ValkeyHimesManager()

# Functional exports matching user request requirements
cache_himes_flow = valkey_manager.cache_himes_flow
get_himes_flow = valkey_manager.get_himes_flow
get_himes_context = valkey_manager.get_himes_context
save_session_state = valkey_manager.save_session_state
get_session_state = valkey_manager.get_session_state
set_active_module = valkey_manager.set_active_module
get_active_module = valkey_manager.get_active_module
acquire_nagul_folder_lock = valkey_manager.acquire_nagul_folder_lock
release_nagul_folder_lock = valkey_manager.release_nagul_folder_lock
nagul_folder_lock_context = valkey_manager.nagul_folder_lock_context
