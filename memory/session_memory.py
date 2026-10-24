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
# Sliding window — keep last N turns (10 complete turns for multi-turn conversational continuity)
WINDOW_K = 10


class ConversationBufferWindowMemory:
    """
    LangChain-compatible ConversationBufferWindowMemory.
    Wraps ValkeySessionMemory to provide standard LangChain memory interface:
      - load_memory_variables()
      - save_context()
      - clear()
      - buffer / chat_memory
    """

    def __init__(
        self,
        chat_memory: Optional[BaseChatMessageHistory] = None,
        k: int = WINDOW_K,
        return_messages: bool = True,
        memory_key: str = "chat_history"
    ):
        self.chat_memory = chat_memory
        self.k = k
        self.return_messages = return_messages
        self.memory_key = memory_key

    @property
    def buffer(self):
        if not self.chat_memory:
            return [] if self.return_messages else ""
        msgs = self.chat_memory.messages
        windowed = msgs[-(self.k * 2):] if len(msgs) > (self.k * 2) else msgs
        if self.return_messages:
            return windowed
        return "\n".join([f"{type(m).__name__}: {m.content}" for m in windowed])

    def load_memory_variables(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {self.memory_key: self.buffer}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        input_str = next(iter(inputs.values())) if inputs else ""
        output_str = next(iter(outputs.values())) if outputs else ""
        if self.chat_memory:
            self.chat_memory.add_user_message(str(input_str))
            self.chat_memory.add_ai_message(str(output_str))

    def clear(self) -> None:
        if self.chat_memory:
            self.chat_memory.clear()


class ValkeySessionMemory(BaseChatMessageHistory):
    """
    LangChain BaseChatMessageHistory implementation backed by Valkey.

    Wraps valkey_manager so that LangChain chains and agents get persistent,
    windowed conversation history without extra network connections.
    Enforces user-isolated storage keys: himes:chat_history:{user_id}:{session_id}.
    """

    def __init__(self, session_id: str, user_id: Optional[str] = None, window_k: int = WINDOW_K):
        super().__init__()
        from valkey_himes_manager import valkey_manager
        self._vm = valkey_manager
        self.session_id = session_id
        self.window_k = window_k

        # Extract user_id from parameter or parse from session_id (himes_user_{user_id}_{uuid})
        if not user_id:
            m = re.match(r"^himes_user_([a-zA-Z0-9_\-]+?)_", session_id)
            if m:
                user_id = m.group(1)
            else:
                user_id = "default_user"
        self.user_id = str(user_id)
        # Task Specification Requirement: himes:chat_history:{user_id}:{session_id}
        self._memory_key = f"himes:chat_history:{self.user_id}:{session_id}"

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

    def add_turn(self, user_message: str, ai_response: str, entities: Optional[Dict[str, Any]] = None) -> None:
        """
        Appends a complete human↔AI turn to the session window.
        Extracts and carries forward active entities (MRN, visit_no).
        """
        data = self._load_raw()

        if entities and isinstance(entities, dict):
            for k, v in entities.items():
                if v:
                    data["active_entities"][k] = v

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

    def format_context_for_prompt(self, max_turns: int = WINDOW_K) -> str:
        """
        Returns a rich text block of recent conversation history (up to last 10 turns)
        suitable for injecting into an LLM system prompt for conversational co-reference resolution.
        """
        turns = self.get_history()
        if not turns:
            return ""
        recent = turns[-max_turns:]
        lines = [f"### FULL SESSION CHAT HISTORY (Last {len(recent)} Turns - Chronological):"]
        for i, t in enumerate(recent, 1):
            lines.append(f"Turn {i}:")
            lines.append(f"  User: {t.get('user', '')}")
            lines.append(f"  Assistant: {str(t.get('ai', ''))[:1200]}")
        return "\n".join(lines)



    def get_langchain_window_memory(self):
        """
        Returns a LangChain ConversationBufferWindowMemory instance
        synchronized with this Valkey chat message history.
        """
        try:
            from langchain.memory import ConversationBufferWindowMemory as LCWindowMemory
            return LCWindowMemory(
                chat_memory=self,
                k=self.window_k,
                return_messages=True,
                memory_key="chat_history"
            )
        except Exception:
            return ConversationBufferWindowMemory(
                chat_memory=self,
                k=self.window_k,
                return_messages=True,
                memory_key="chat_history"
            )

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

def get_session_memory(session_id: str, user_id: Optional[str] = None) -> ValkeySessionMemory:
    """
    Factory — returns a ValkeySessionMemory instance for the given session.
    Each session_id and user_id maps to an isolated Valkey key:
    himes:chat_history:{user_id}:{session_id}
    """
    return ValkeySessionMemory(session_id=session_id, user_id=user_id)


__all__ = [
    "ValkeySessionMemory",
    "ConversationBufferWindowMemory",
    "get_session_memory",
    "SESSION_TTL",
    "WINDOW_K"
]
