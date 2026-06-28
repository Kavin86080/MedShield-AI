"""
===========================================================
MedShield-X

Enterprise Query Pipeline
===========================================================
"""

from backend.rag.hybrid.hybrid_retriever import HybridRetriever

from backend.rag.memory.conversation_memory import ConversationMemory

from backend.rag.reasoning.evidence_builder import EvidenceBuilder

from backend.rag.reasoning.medical_reasoner import MedicalReasoner

from backend.rag.reasoning.confidence_score import ConfidenceScore

from backend.rag.citations.source_tracker import SourceTracker

from backend.rag.citations.citation_builder import CitationBuilder

from backend.rag.prompting.prompt_builder import PromptBuilder

from backend.rag.llm.groq_service import GroqService


class QueryPipeline:

    def __init__(

    self,

    collection_manager

):

        self.memory = ConversationMemory()

        self.collection = collection_manager

        self.retriever = HybridRetriever(

            self.collection.faiss

        )

        self.evidence = EvidenceBuilder()

        self.reasoner = MedicalReasoner()

        self.confidence = ConfidenceScore()

        self.source_tracker = SourceTracker()

        self.citation_builder = CitationBuilder()

        self.prompt_builder = PromptBuilder()

        self.llm = GroqService()

        self.retriever.build_indexes(

            self.collection.documents.get_all_chunks()

        )

    def ask(self, question):

        # Store doctor's question
        self.memory.add_message(
            "doctor",
            question
        )

        retrieval = self.retriever.retrieve(question)

        retrieval = self.evidence.build(retrieval)

        retrieval = self.reasoner.reason(retrieval)

        retrieval = self.confidence.calculate(retrieval)

        retrieval = self.source_tracker.build_sources(retrieval)

        retrieval = self.citation_builder.build(retrieval)

        prompt = self.prompt_builder.build(

            question=question,

            context=retrieval["reasoning"],

            evidence=retrieval["evidence"],

            confidence=retrieval["confidence"],

            citations=retrieval["citations"],

            conversation=self.memory.get_history()

        )

        response = self.llm.generate(

            prompt=prompt,

            confidence=retrieval["confidence"],

            evidence=retrieval["evidence"],

            citations=retrieval["citations"]

        )

        self.memory.add_message(

            "assistant",

            response["answer"]

        )

        return {

            "status": "success",

            "question": question,

            "response": response,

            "collection": self.collection.collection_summary()

        }