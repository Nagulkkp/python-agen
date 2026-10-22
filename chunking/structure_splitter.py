"""
chunking/structure_splitter.py
==============================
Parses raw clinical Markdown (.md) documents, splits along structural 
headers (##, ###), enforces word-count boundaries with overlap, 
and produces rich metadata schemas.
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    doc_title: str
    section: str
    subsection: str
    chunk_index: int
    has_table: bool
    has_code_block: bool
    word_count: int

    def to_metadata(self) -> Dict[str, Any]:
        """Converts chunk metadata to ChromaDB-compatible primitive types."""
        return {
            "doc_title": self.doc_title,
            "section": self.section,
            "subsection": self.subsection,
            "chunk_index": self.chunk_index,
            "has_table": self.has_table,
            "has_code_block": self.has_code_block,
            "word_count": self.word_count,
        }

class MarkdownStructureSplitter:
    def __init__(self, target_words: int = 400, overlap_words: int = 50):
        self.target_words = target_words
        self.overlap_words = overlap_words

    def split_document(self, markdown_content: str, default_title: str = "Clinical SOP") -> List[DocumentChunk]:
        """
        Parses Markdown text, traverses H1, H2, and H3 hierarchies, and produces
        structured chunks adhering to word limits with sliding window overlaps.
        """
        lines = markdown_content.splitlines()
        doc_title = default_title
        chunks: List[DocumentChunk] = []

        # 1. Extract primary document title from first H1 if present
        for line in lines:
            line_strip = line.strip()
            if line_strip.startswith("# "):
                doc_title = line_strip.lstrip("# ").strip()
                break

        # 2. Segment document by H2 headers
        h2_pattern = re.compile(r"^##\s+(.+)$")
        h3_pattern = re.compile(r"^###\s+(.+)$")

        current_h2 = "General Overview"
        current_h3 = "Main Section"
        current_block: List[str] = []
        global_chunk_idx = 0

        def process_block(text_lines: List[str], h2_title: str, h3_title: str):
            nonlocal global_chunk_idx
            raw_text = "\n".join(text_lines).strip()
            if not raw_text or len(raw_text) < 20:
                return

            words = raw_text.split()
            if len(words) <= self.target_words:
                chunks.append(self._create_chunk(raw_text, doc_title, h2_title, h3_title, global_chunk_idx))
                global_chunk_idx += 1
            else:
                # Sliding window split across word boundaries
                start = 0
                step = max(1, self.target_words - self.overlap_words)
                while start < len(words):
                    window = words[start : start + self.target_words]
                    chunk_text = " ".join(window)
                    chunks.append(self._create_chunk(chunk_text, doc_title, h2_title, h3_title, global_chunk_idx))
                    global_chunk_idx += 1
                    start += step

        for line in lines:
            line_strip = line.strip()
            if line_strip.startswith("# ") and not line_strip.startswith("## "):
                continue

            h2_match = h2_pattern.match(line)
            h3_match = h3_pattern.match(line)

            if h2_match:
                process_block(current_block, current_h2, current_h3)
                current_block = []
                current_h2 = h2_match.group(1).strip()
                current_h3 = "General"
            elif h3_match:
                process_block(current_block, current_h2, current_h3)
                current_block = []
                current_h3 = h3_match.group(1).strip()
            else:
                current_block.append(line)

        # Process any trailing content
        if current_block:
            process_block(current_block, current_h2, current_h3)

        return chunks

    def _create_chunk(self, text: str, doc_title: str, section: str, subsection: str, index: int) -> DocumentChunk:
        has_table = ("|" in text and "-|-" in text) or ("|:---" in text) or ("| ---" in text)
        has_code_block = "```" in text
        words = text.split()
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", doc_title.lower())[:20].strip("_")
        chunk_id = f"{slug}_{index:04d}"

        return DocumentChunk(
            chunk_id=chunk_id,
            text=text,
            doc_title=doc_title,
            section=section,
            subsection=subsection,
            chunk_index=index,
            has_table=has_table,
            has_code_block=has_code_block,
            word_count=len(words)
        )
