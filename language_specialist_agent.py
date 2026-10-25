"""
language_specialist_agent.py
============================
Dedicated Multi-Agent Language Specialist for HIMES AI.

Architecture Role:
1. Detects the exact language of the user input (English, Tanglish, Pure Tamil, Arabic, Hindi, etc.).
2. Translates / normalizes non-English queries into clean English for optimal MSSQL schema matching and internal agent reasoning.
3. Intercepts the final response and ensures it is translated / mirrored back to the exact same language the user used to ask the question.
   - User in English  -> 100% fluent English (NO Tanglish words like 'Aamaanga', 'nethu', 'irukku').
   - User in Tanglish -> 100% natural, conversational Tanglish (Latin alphabet, NO Tamil Unicode script, NO pure English).
   - User in Tamil    -> 100% Pure Tamil script (தமிழ்).
   - User in Arabic   -> 100% Arabic.
"""

import re
import json
from typing import Dict, Any, Optional

class LanguageSpecialistAgent:
    def __init__(self):
        self.name = "LanguageSpecialistAgent"
        self.role_description = "User Language Detection, Intent Normalization to English, and Strict Multilingual Response Mirroring"

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Determines the exact language of user text.
        Returns:
            - language_name: e.g. 'English', 'Tanglish', 'Tamil', 'Arabic', 'Hindi'
            - language_code: e.g. 'en', 'tanglish', 'ta', 'ar', 'hi'
            - is_english: bool
            - is_tanglish: bool
        """
        if not text or not str(text).strip():
            return {
                "language_name": "English",
                "language_code": "en",
                "is_english": True,
                "is_tanglish": False
            }

        clean = str(text).strip()
        lower = clean.lower()

        # 1. Unicode Script Checks
        if re.search(r"[\u0600-\u06FF]", clean):
            return {"language_name": "Arabic", "language_code": "ar", "is_english": False, "is_tanglish": False}
        if re.search(r"[\u0B80-\u0BFF]", clean):
            return {"language_name": "Tamil", "language_code": "ta", "is_english": False, "is_tanglish": False}
        if re.search(r"[\u0900-\u097F]", clean):
            return {"language_name": "Hindi", "language_code": "hi", "is_english": False, "is_tanglish": False}
        if re.search(r"[\u0D00-\u0D7F]", clean):
            return {"language_name": "Malayalam", "language_code": "ml", "is_english": False, "is_tanglish": False}
        if re.search(r"[\u0C00-\u0C7F]", clean):
            return {"language_name": "Telugu", "language_code": "te", "is_english": False, "is_tanglish": False}

        # 2. Tanglish Morphemes, Lexicon & Conversational Markers (Tamil in Latin/English characters)
        tanglish_patterns = [
            # Verbs - be/exist/have
            r"\biruk(?:ku|ka|kum|kura|ken|kom|kanga|kaanga|kunu|kanum|kattum|kalam|kuthu)?\b",
            r"\birun(?:tha|dha|thuchu|thathu|thanga|then)?\b",
            r"\bill(?:a|ai|ana|aya|aye|e)?\b",
            # Verbs - know/understand/able
            r"\btheri(?:yum|um|yuma|uma|yathu|yala|yadhu|yavillai)\b",
            r"\bpuriy(?:um|uma|ala|adhu|yathu)\b",
            r"\bmudi(?:yum|um|yuma|uma|yathu|yaathu|yadhu|yala)\b",
            # Verbs - do/put/make
            r"\bpann(?:u|a|i|ren|ra|ran|ranga|ala|adhe|idunga|ikalam|ikkalam|unga|itta|itten|idalam|iruk\w*)\b",
            r"\bpod(?:u|a|i|ren|ra|unga|uthu|ala|adhe|idunga|ikalam|iruk\w*)\b",
            r"\bpott(?:u|a|en|anga|iruk\w*)\b",
            # Verbs - say/tell/show/see/give/take/go/come
            r"\bsoll(?:u|a|i|ren|ra|unga|ala|idunga|iruk\w*)\b",
            r"\bsonn(?:a|en|anga|adhu)\b",
            r"\bkaat(?:tu|ta|ti|tunga|talam|tidunga)\b",
            r"\bpaar(?:u|a|unga|tha|thutu|thukonga|alam)\b",
            r"\bpaath(?:u|a|en|anga|ukonga)\b",
            r"\bkod(?:u|a|u|unga|uthu|utha|uthutu|uthiruk\w*)\b",
            r"\bkud(?:u|a|unga|uthu|utha)\b",
            r"\bedu(?:thu|tha|ka|thukalam|thukonga|thiruk\w*)\b",
            r"\bpo(?:ga|i|nga|na|num|guthu|yiruk\w*)\b",
            r"\bva(?:anga|nga|ra|ndha|ndhu|ndhutu|ruthu|rum|lame)\b",
            r"\bvandh(?:a|u|en|anga|iruk\w*)\b",
            r"\bkedaik(?:kum|kuma|kala|kuthu)\b",
            r"\bkidaik(?:kum|kuma|kala|kuthu)\b",
            r"\bvach(?:u|uruk\w*|iruk\w*)\b",
            # Interrogatives & Demonstratives (What, where, how, when, who, which)
            r"\benna(?:va|nu|ndu)?\b",
            r"\beng(?:a|ae|e|ada)\b",
            r"\bepp(?:adi|idi|o|a)\b",
            r"\beth(?:ana|anai|u)\b",
            r"\bev(?:lo|lavu|valavu)\b",
            r"\byaar(?:u|avathu|a)?\b",
            r"\ben(?:akku|noda|akkenna|na)\b",
            r"\bun(?:akku|noda|gala|galukku)\b",
            r"\bnam(?:ma|akku|modaya)\b",
            r"\bavan(?:oda|ukku)?\b",
            r"\bavang(?:a|al|alukku|aloda)\b",
            r"\bith(?:u|ula|uku|oda)\b",
            r"\bath(?:u|ula|uku|oda)\b",
            r"\binth(?:a|u)\b",
            r"\banth(?:a|u)\b",
            # Particles, Suffixes & Common Conjunctions
            r"\baama(?:anga|a)?\b",
            r"\bven(?:um|uma|duma|am|umna)?\b",
            r"\bvaen(?:um|uma)\b",
            r"\bpoth(?:um|uma)\b",
            r"\bpodh(?:um|uma)\b",
            r"\bap(?:rom|ram|uram|romna)?\b",
            r"\bip(?:po|podhu)\b",
            r"\bap(?:po|podhu)\b",
            r"\bneth(?:u|i)\b",
            r"\binnaik(?:u|i)\b",
            r"\binaik(?:u|i)\b",
            r"\bnaalaik(?:u|i)\b",
            r"\bkeezh(?:e)?\b",
            r"\bmel(?:a|e)?\b",
            r"\bpath(?:i|ina|iyo|u)\b",
            r"\bkood(?:a)?\b",
            r"\bmatt(?:um|uma)\b",
            r"\bathig(?:a|am|ama|amaana)\b",
            r"\bkonj(?:am)?\b",
            r"\bromba\b",
            r"\binn(?:um)?\b",
            r"\bmaathiri\b", r"\bmathiri\b", r"\bmari\b",
            r"\bthanglish\b",
            # Question particle endings
            r"\b(?:ah|aa)\b",
            r"\b-la\b", r"\b-ku\b", r"\b-oda\b", r"\b-ukku\b", r"\b-a\b", r"\b-nu\b"
        ]
        has_tanglish_marker = any(re.search(p, lower) for p in tanglish_patterns)

        if has_tanglish_marker:
            return {
                "language_name": "Tanglish",
                "language_code": "tanglish",
                "is_english": False,
                "is_tanglish": True
            }

        # Check for English structural keywords (pronouns, auxiliary verbs, prepositions)
        english_words = {
            "is", "there", "any", "visit", "visits", "still", "unbilled", "billed", "for", "yesterday",
            "today", "what", "which", "how", "many", "show", "me", "give", "list", "patient", "patients",
            "details", "invoice", "invoices", "amount", "highest", "lowest", "service", "services",
            "payment", "mode", "receipt", "deposit", "are", "have", "been", "was", "were", "can", "you",
            "tell", "find", "who", "when", "why", "where", "with", "from", "and", "or", "not"
        }
        tokens = re.findall(r"[a-z]+", lower)
        english_count = sum(1 for t in tokens if t in english_words)
        total_tokens = len(tokens)

        # If user explicitly wrote in English words with no Tanglish morphemes
        if total_tokens > 0 and (english_count / total_tokens) >= 0.35:
            return {
                "language_name": "English",
                "language_code": "en",
                "is_english": True,
                "is_tanglish": False
            }

        # Fallback to English for Latin-based texts
        return {
            "language_name": "English",
            "language_code": "en",
            "is_english": True,
            "is_tanglish": False
        }

    def normalize_to_english(self, user_text: str, lang_info: Dict[str, Any]) -> str:
        """
        Translates/Normalizes non-English queries into standard English for optimal
        database query formulation, controller searching, and tool calling.
        """
        if lang_info.get("is_english"):
            return user_text

        try:
            from autonomous_agent import autonomous_agent
            prompt = (
                f"Translate the following user question into clear, concise English for a hospital database query.\n"
                f"User Question: \"{user_text}\"\n"
                f"Source Language: {lang_info.get('language_name')}\n\n"
                f"RULES:\n"
                f"- Return ONLY the direct English translation without explanations, quotes, or conversational filler.\n"
                f"- Keep medical terms, numbers, dates, MRN numbers, and Visit numbers exactly intact."
            )
            eng_trans = autonomous_agent.call_llm(prompt, "You are a professional medical translator for hospital management systems.")
            clean_eng = str(eng_trans or "").strip().strip('"').strip("'")
            if clean_eng and len(clean_eng) > 3:
                return clean_eng
        except Exception as e:
            print(f"[LanguageSpecialistAgent] Normalization notice: {e}")

        return user_text

    def mirror_reply(self, reply_text: str, target_lang_info: Dict[str, Any]) -> str:
        """
        Ensures the final response delivered to the user strictly matches the user's language:
        - If user asked in English -> Translate any Tanglish sentences to fluent English.
        - If user asked in Tanglish -> Ensure natural, conversational Tanglish.
        - If user asked in Tamil -> Ensure pure Tamil script.
        - If user asked in Arabic -> Translate to Arabic.
        
        CRITICAL GUARDRAIL:
        Preserves Markdown tables, code blocks, <details> accordions, CPT codes, amounts, and numbers!
        """
        if not reply_text or not isinstance(reply_text, str):
            return reply_text

        # Strip any internal Thought prefix or reasoning scratchpad before language checks
        try:
            from autonomous_agent import clean_agent_thought
            reply_text = clean_agent_thought(reply_text)
        except Exception:
            if 'Final Answer:' in reply_text:
                reply_text = reply_text.split('Final Answer:', 1)[-1].strip()
            reply_text = re.sub(r'^Thought:\s*', '', reply_text, flags=re.IGNORECASE).strip()

        target_code = target_lang_info.get("language_code", "en")
        target_name = target_lang_info.get("language_name", "English")

        # 1. Quick check: If target is English, does the text contain Tanglish words?
        if target_code == "en":
            tanglish_tokens = ["aamaanga", "nethu", "irukku", "eduthirukaanga", "pannirukaanga", "pannala", "solren", "paathukonga", "kidaikala", "theriyum"]
            has_tanglish_leak = any(w in reply_text.lower() for w in tanglish_tokens)
            if not has_tanglish_leak:
                return reply_text  # Already clean English!

        # 2. Quick check: If target is Tanglish, does the text contain Pure Tamil script or is it already natural Tanglish?
        if target_code == "tanglish":
            has_tamil_script = bool(re.search(r"[\u0B80-\u0BFF]", reply_text))
            if not has_tamil_script:
                # Count distinct whole-word Tanglish markers in reply
                tanglish_check_patterns = [
                    r"\biruk(?:ku|ka|kum|kura|ken|kom|kanga|kaanga|kunu|kanum)?\b",
                    r"\bpann(?:u|a|i|ren|ra|ran|ranga|ala|unga|itta|itten|idalam|iruk\w*)\b",
                    r"\baamaanga\b", r"\baama\b", r"\billa\b", r"\billana\b",
                    r"\bavang(?:a|al|alukku|aloda)\b", r"\bneeng(?:a|al|alukku)\b",
                    r"\bnethu\b", r"\binnaiku\b", r"\btheri(?:yum|um|yuma)\b",
                    r"\bmudi(?:yum|um|yuma|yaathu)\b", r"\bsoll(?:u|unga|ren)\b",
                    r"\bkaat(?:tu|tunga)\b", r"\bpaath(?:u|ukonga)\b", r"\bkod(?:u|unga)\b"
                ]
                distinct_matches = sum(1 for p in tanglish_check_patterns if re.search(p, reply_text.lower()))
                # If there are 2 or more distinct Tanglish words, it is already conversational Tanglish
                if distinct_matches >= 2:
                    return reply_text

        # 3. Perform Language Mirroring using LLM
        try:
            from autonomous_agent import autonomous_agent

            # Protect <details> accordions and ```sql blocks from being altered
            stash = []
            def _stash_block(m):
                idx = len(stash)
                stash.append(m.group(0))
                return f"__HIMES_PROTECTED_BLOCK_{idx}__"

            text_to_translate = re.sub(r"<details[\s\S]*?</details>", _stash_block, reply_text, flags=re.IGNORECASE)
            text_to_translate = re.sub(r"```[\s\S]*?```", _stash_block, text_to_translate)

            sys_prompt = (
                f"You are the HIMES Language Mirroring Specialist Agent.\n"
                f"Your task is to rewrite the text into {target_name.upper()}.\n\n"
                f"MANDATORY RULES:\n"
                f"1. Target Language: {target_name.upper()}\n"
                f"   - If target is English: Output ONLY fluent, professional English (e.g. translate 'Aamaanga, nethu...' to 'Yes, yesterday...'). NO Tanglish words!\n"
                f"   - If target is Tanglish: Output ONLY natural, conversational Tanglish written in Latin characters (e.g. 'Nethu 6 visits innum bill aagala'). NEVER output Tamil Unicode script!\n"
                f"   - If target is Tamil: Output in pure Tamil script (தமிழ் எழுத்துகளில்).\n"
                f"   - If target is Arabic: Output in Arabic script.\n"
                f"2. PRESERVE EXACT FORMATTING: Keep Markdown tables (| ... |), bullets, status cards (✅, ⚠️, ℹ️), numbers, CPT codes, Invoice Nos, MRNs, and placeholder tokens '__HIMES_PROTECTED_BLOCK_X__' 100% untouched!\n"
                f"3. Return ONLY the translated response text without commentary."
            )

            prompt = f"Text to translate to {target_name}:\n\n{text_to_translate}"
            mirrored = autonomous_agent.call_llm(prompt, sys_prompt)
            clean_mirrored = str(mirrored or "").strip()

            # Restore protected blocks
            for idx, block in enumerate(stash):
                clean_mirrored = clean_mirrored.replace(f"__HIMES_PROTECTED_BLOCK_{idx}__", block)

            return clean_mirrored if clean_mirrored else reply_text
        except Exception as e:
            print(f"[LanguageSpecialistAgent] Mirroring notice: {e}")
            return reply_text

# Global Singleton
language_specialist = LanguageSpecialistAgent()
