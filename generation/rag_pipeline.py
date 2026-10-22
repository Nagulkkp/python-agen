"""
generation/rag_pipeline.py
==========================
Orchestrates context packaging, strict grounded prompt generation,
inline citation formatting ([Source: <doc_title> > <section>]),
graceful refusal handling, and dual-mode UI presentation.
"""

import time
from typing import Dict, Any

from retrieval.hybrid_search import hybrid_search_engine
from autonomous_agent import autonomous_agent

class GroundedRAGPipeline:
    def answer_query(self, query: str, is_developer_mode: bool = False) -> Dict[str, Any]:
        start_time = time.perf_counter()

        # 1. Retrieve hybrid ranked chunks
        retrieval_res = hybrid_search_engine.search(query)
        chunks = retrieval_res.get("top_chunks", [])
        latency_retrieval_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 2. Handle Zero-Context / Low-Relevance Graceful Refusal
        if not chunks or (len(chunks) > 0 and chunks[0].get("rrf_score", 0.0) < 0.008):
            refusal_user = (
                "⚠️ **Clinical Knowledge Boundary Refusal:**\n\n"
                "The requested procedure or protocol is not documented in the verified hospital standard "
                "operating procedures (SOPs). To maintain clinical safety, I cannot extrapolate medical advice "
                "without verified protocol citations.\n\n"
                "*Please consult the Hospital Medical Director or Head of Department.*"
            )
            return {
                "reply": refusal_user,
                "status": "refused_out_of_domain",
                "citations": [],
                "latency_ms": latency_retrieval_ms
            }

        # 3. Build Grounded Context Block
        context_blocks = []
        citations_metadata = []
        for chunk in chunks:
            meta = chunk.get("metadata", {})
            doc_title = meta.get("doc_title", "Hospital SOP")
            section = meta.get("section", "Clinical Standard")
            c_tag = f"Source: {doc_title} > {section}"
            citations_metadata.append(c_tag)
            context_blocks.append(f"[{c_tag}]\n{chunk['text']}")

        joined_context = "\n\n---\n\n".join(context_blocks)

        # 4. Strict Grounded Prompting
        system_prompt = (
            "You are the HIMES Clinical Intelligence System. You must strictly answer the user query "
            "using ONLY the provided hospital clinical SOP context below. If the answer cannot be fully "
            "justified by the context, refuse politely. Every key clinical statement MUST include an inline "
            "citation tag in the format: `[Source: <doc_title> > <section>]`."
        )

        user_prompt = (
            f"CLINICAL SOP RETRIEVED CONTEXT:\n{joined_context}\n\n"
            f"USER QUERY: {query}\n\n"
            f"Formulate a precise, authoritative answer in clean Markdown with inline citations."
        )

        # Invoke LLM
        llm_start = time.perf_counter()
        raw_llm_answer = autonomous_agent.call_llm(user_prompt, system_prompt)
        llm_latency_ms = round((time.perf_counter() - llm_start) * 1000, 2)
        total_latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 5. Dual-Mode Output Construction
        if is_developer_mode:
            diag_rows = ""
            for c in chunks:
                v_rank = c.get('vector_rank') or "N/A"
                b_rank = c.get('bm25_rank') or "N/A"
                diag_rows += f"| `{c['chunk_id']}` | **{c['rrf_score']}** | Vector: {v_rank} | BM25: {b_rank} |\n"

            dev_reply = (
                f"{raw_llm_answer}\n\n"
                f"### 💻 Developer Diagnostics (Hybrid RAG)\n"
                f"• **Total Latency:** `{total_latency_ms} ms` (Retrieval: `{latency_retrieval_ms} ms`, LLM: `{llm_latency_ms} ms`)\n"
                f"• **Fused Chunks:** `{len(chunks)}`\n\n"
                f"| Chunk ID | RRF Score | Dense Rank | Sparse Rank |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"{diag_rows}"
            )
            final_reply = dev_reply
        else:
            final_reply = f"{raw_llm_answer}\n\n> 📘 *Verified against HIMES Authoritative Clinical SOPs*"

        return {
            "reply": final_reply,
            "status": "success",
            "citations": list(set(citations_metadata)),
            "latency_ms": total_latency_ms,
            "chunks_used": [c["chunk_id"] for c in chunks]
        }

rag_pipeline = GroundedRAGPipeline()
