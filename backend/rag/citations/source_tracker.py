"""
===========================================================
MedShield-X

Source Tracker

Tracks where every retrieved chunk originated.
===========================================================
"""


class SourceTracker:

    def build_sources(

        self,

        retrieval_result

    ):

        sources = []

        for chunk in retrieval_result["final_results"]:

            sources.append(

                {

                    "document_id": chunk["document_id"],

                    "chunk_id": chunk["chunk_id"],

                    "chunk_index": chunk["chunk_index"],

                    "score": chunk.get(

                        "cross_encoder_score",

                        chunk.get(

                            "hybrid_score",

                            0

                        )

                    )

                }

            )

        retrieval_result["sources"] = sources

        return retrieval_result