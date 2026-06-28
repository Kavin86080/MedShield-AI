"""
===========================================================
MedShield-X

Citation Builder

Creates references for doctor review.
===========================================================
"""


class CitationBuilder:

    def build(

        self,

        retrieval_result

    ):

        citations = []

        for source in retrieval_result["sources"]:

            citations.append(

                {

                    "reference":

                    f"Document {source['document_id']} | "

                    f"Chunk {source['chunk_index']}",

                    "document_id": source["document_id"],

                    "chunk_id": source["chunk_id"],

                    "score": source["score"]

                }

            )

        retrieval_result["citations"] = citations

        return retrieval_result