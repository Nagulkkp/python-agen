"""
memory/session_memory.py
========================
LangChain-compatible Session Memory backed by Valkey.

Architecture:
  - Primary store  : Valkey (192.168.20.152:6379) — fast, distributed
  - Fallback store : valkey_manager in-memory dict (same API, zero latency)
  - Window size    : last 5 conversation turns per session
  - TTL            : 1 hour per session (auto-reset on new conversation)

Context resolution (pronoun / entity carry-over):
  - Tracks active MRN, visit_no, bill_no across turns
  - "Avan"/"His"/"அவன்"/"இந்த நோயாளி" etc. → resolved to active MRN automatically
"""

import json
import re
import sys
from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# Valkey TTL for session memory (1 hour)
SESSION_TTL = 3600
# Sliding window — keep last N turns
WINDOW_K = 5


class ValkeySessionMemory(BaseChatMessageHistory):
    """
    LangChain BaseChatMessageHistory implementation backed by Valkey.

    Wraps valkey_manager so that LangChain chains and agents get persistent,
    windowed conversation history without extra network connections.
    """

    def __init__(self, session_id: str, window_k: int = WINDOW_K):
        super().__init__()
        from valkey_himes_manager import valkey_manager
        self._vm = valkey_manager
        self.session_id = session_id
        self.window_k = window_k
        self._memory_key = f"himes:session_mem:{session_id}"

    # ── Internal store / load ────────────────────────────────────────────────

    def _load_raw(self) -> Dict[str, Any]:
        """Loads raw session data from Valkey (or in-memory fallback)."""
        try:
            if self._vm._connected and self._vm._client:
                raw = self._vm._client.get(self._memory_key)
                if raw:
                    return json.loads(raw)
        except Exception:
            pass

        # In-memory fallback
        raw = self._vm._fallback_store.get(self._memory_key)
        if raw and isinstance(raw, str):
            try:
                return json.loads(raw)
            except Exception:
                pass
        elif raw and isinstance(raw, dict):
            return raw

        return {"turns": [], "active_entities": {"mrn": None, "visit_no": None, "bill_no": None}}

    def _save_raw(self, data: Dict[str, Any]) -> None:
        """Saves session data to Valkey with TTL (or in-memory fallback)."""
        payload = json.dumps(data, ensure_ascii=False)
        try:
            if self._vm._connected and self._vm._client:
                self._vm._client.setex(self._memory_key, SESSION_TTL, payload)
                return
        except Exception:
            pass
        self._vm._fallback_store[self._memory_key] = payload

    # ── Entity extraction ────────────────────────────────────────────────────

    def _extract_entities(self, text: str) -> Dict[str, Optional[str]]:
        """Extracts MRN, Visit No, and Bill No from text."""
        entities: Dict[str, Optional[str]] = {"mrn": None, "visit_no": None, "bill_no": None}

        # MRN: standard numeric (6-8 digits) or PHAR-prefixed
        m = re.search(r'\b(?:MRN|mrn)[\s#:]*(\d{5,9})\b', text, re.IGNORECASE)
        if not m:
            m = re.search(r'\b(PHAR\d{3,8})\b', text, re.IGNORECASE)
        if not m:
            # Standalone 6-8 digit number not looking like a date
            m = re.search(r'(?<!\d)(?:3\d{6}|[124-9]\d{5,7})(?!\d)', text)
        if m:
            entities["mrn"] = m.group(1) if m.groups() else m.group(0)

        # Visit No: "visit 16923", "visit # 16923"
        v = re.search(r'\b(?:visit|encounter)[\s#:]*(\d{4,8})\b', text, re.IGNORECASE)
        if v:
            entities["visit_no"] = v.group(1)

        # Bill No: "bill 55875", "inv 55875"
        b = re.search(r'\b(?:bill|inv|invoice)[\s#:]*(\d{4,9})\b', text, re.IGNORECASE)
        if b:
            entities["bill_no"] = b.group(1)

        return entities

    # ── Public LangChain BaseChatMessageHistory API ──────────────────────────

    @property
    def messages(self) -> List[BaseMessage]:
        """LangChain standard property: returns history as BaseMessage list."""
        return self.get_langchain_messages()

    def add_message(self, message: BaseMessage) -> None:
        """LangChain standard: appends a single message."""
        data = self._load_raw()
        if isinstance(message, HumanMessage):
            # Extract entities from user message
            ents = self._extract_entities(str(message.content))
            for k, v in ents.items():
                if v:
                    data["active_entities"][k] = v
            if ents.get("mrn") and not ents.get("visit_no"):
                data["active_entities"]["visit_no"] = None
            data["turns"].append({"user": str(message.content), "ai": ""})
        elif isinstance(message, AIMessage):
            if data["turns"]:
                data["turns"][-1]["ai"] = str(message.content)
            else:
                data["turns"].append({"user": "", "ai": str(message.content)})

        if len(data["turns"]) > self.window_k:
            data["turns"] = data["turns"][-self.window_k:]
        self._save_raw(data)

    def add_user_message(self, message: str) -> None:
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.add_message(AIMessage(content=message))

    def add_turn(self, user_message: str, ai_response: str) -> None:
        """
        Appends a complete human↔AI turn to the session window.
        Extracts and carries forward active entities (MRN, visit_no).
        """
        data = self._load_raw()

        ents = self._extract_entities(user_message)
        for k, v in ents.items():
            if v:
                data["active_entities"][k] = v
        if ents.get("mrn") and not ents.get("visit_no"):
            data["active_entities"]["visit_no"] = None

        data["turns"].append({"user": user_message, "ai": ai_response})
        if len(data["turns"]) > self.window_k:
            data["turns"] = data["turns"][-self.window_k:]

        self._save_raw(data)

    def get_history(self) -> List[Dict[str, str]]:
        """Returns the last window_k turns as [{'user':..., 'ai':...}, ...]."""
        return self._load_raw().get("turns", [])

    def get_active_entities(self) -> Dict[str, Optional[str]]:
        """Returns currently active patient context (MRN, visit_no, bill_no)."""
        return self._load_raw().get("active_entities", {})

    def get_langchain_messages(self) -> List[BaseMessage]:
        """Returns history as LangChain BaseMessage list."""
        messages: List[BaseMessage] = []
        for turn in self.get_history():
            u = turn.get("user")
            a = turn.get("ai")
            if u:
                messages.append(HumanMessage(content=u))
            if a:
                messages.append(AIMessage(content=a))
        return messages

    def format_context_for_prompt(self) -> str:
        """
        Returns a compact text block of recent conversation history
        suitable for injecting into an LLM system prompt.
        """
        turns = self.get_history()
        if not turns:
            return ""
        lines = ["### Recent Conversation History:"]
        for i, t in enumerate(turns, 1):
            lines.append(f"Turn {i}:")
            lines.append(f"  User: {t.get('user', '')}")
            lines.append(f"  Agent: {t.get('ai', '')[:200]}...")
        return "\n".join(lines)

    def clear(self) -> None:
        """Clears the session memory from Valkey."""
        try:
            if self._vm._connected and self._vm._client:
                self._vm._client.delete(self._memory_key)
            else:
                self._vm._fallback_store.pop(self._memory_key, None)
        except Exception:
            pass


# ── Factory ──────────────────────────────────────────────────────────────────

def get_session_memory(session_id: str) -> ValkeySessionMemory:
    """
    Factory — returns a ValkeySessionMemory instance for the given session.
    Each session_id maps to an isolated Valkey key.
    """
    return ValkeySessionMemory(session_id=session_id)


__all__ = ["ValkeySessionMemory", "get_session_memory"]
