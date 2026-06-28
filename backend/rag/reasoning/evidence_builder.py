"""
===========================================================
MedShield-X

Evidence Builder
===========================================================
"""


class EvidenceBuilder:

    def build(

        self,

        retrieval_result

    ):

        evidence = []

        for item in retrieval_result["final_results"]:

            evidence.append(

                {

                    "chunk_id": item["chunk_id"],

                    "document_id": item["document_id"],

                    "text": item["text"],

                    "score": item.get(

                        "cross_encoder_score",

                        item.get(

                            "hybrid_score",

                            0

                        )

                    )

                }

            )

        retrieval_result["evidence"] = evidence

        return retrieval_result