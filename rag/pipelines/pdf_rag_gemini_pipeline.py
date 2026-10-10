from rag.pipelines.pdf_rag_pipeline import (
    PDFRAGPipeline
)

from ai_engine.groq_engine.groq_service import (
    GroqService
)

PLACEHOLDER_TOKEN = "[INSERT_RESULT_HERE]"


class PDFRAGGeminiPipeline:

    def __init__(self):

        self.pdf_rag = (
            PDFRAGPipeline()
        )

        self.groq_service = (
            GroqService()
        )

    def index_pdf(
        self,
        pdf_path,
        reset_index=True
    ):

        return self.pdf_rag.index_pdf(
            pdf_path,
            reset_index=reset_index
        )

    def _filter_contexts(self, contexts):
        """
        Remove or clean chunks that are dominated by placeholder text.
        A chunk is considered placeholder-heavy if it contains 2+ occurrences
        of the placeholder token (draft paper artefact).
        """
        filtered = []
        placeholder_found = False

        for ctx in contexts:
            count = ctx.count(PLACEHOLDER_TOKEN)
            if count >= 2:
                # Skip heavily placeholder-polluted chunks
                placeholder_found = True
                continue
            elif count == 1:
                # Keep but mark it
                cleaned = ctx.replace(
                    PLACEHOLDER_TOKEN,
                    "[Result not reported in document]"
                )
                filtered.append(cleaned)
                placeholder_found = True
            else:
                filtered.append(ctx)

        return filtered, placeholder_found

    def ask(
        self,
        question,
        top_k=5
    ):

        contexts = (
            self.pdf_rag.query(
                question,
                top_k
            )
        )

        print("\n" + "="*50)
        print("QUESTION:")
        print(question)

        print("\nRETRIEVED CONTEXTS:")

        for i, ctx in enumerate(contexts):
            print(f"\nChunk {i+1}:")
            print(ctx[:500])

        print("="*50)

        # Filter placeholder-heavy chunks before sending to LLM
        filtered_contexts, has_placeholders = self._filter_contexts(contexts)

        print(f"\nFiltered: {len(contexts)} -> {len(filtered_contexts)} chunks"
              f" | Placeholders detected: {has_placeholders}")

        if not filtered_contexts:
            # All chunks were placeholder-only — use original contexts as fallback
            filtered_contexts = contexts[:2]

        context_text = "\n\n".join(filtered_contexts)

        placeholder_note = (
            "\n\nIMPORTANT: Some sections of this document contain "
            "unreported quantitative results (marked as placeholders). "
            "For those sections, clearly state that the numerical values "
            "were NOT reported in the provided document."
            if has_placeholders else ""
        )

        prompt = f"""
You are MedShield-X Clinical Document Analysis Assistant.

Use ONLY the provided document context to answer the question.{placeholder_note}

Document Context:
{context_text}

Question:
{question}

Instructions:

1. Answer only from the document context above.
2. Summarize clearly using bullet points where appropriate.
3. If a section references unreported values ("[Result not reported in document]"), 
   explicitly note: "Quantitative results were not available in the document."
4. Mention the methodology, architecture, and conclusions where present.
5. Do NOT invent numbers or statistics.
6. Be concise and clinically informative.

Answer:
"""

        answer = (
            self.groq_service.ask(
                prompt
            )
        )

        return {
            "question": question,
            "answer": answer,
            "contexts": filtered_contexts
        }
