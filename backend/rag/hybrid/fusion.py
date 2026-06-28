"""
===========================================================
MedShield-X

Hybrid Fusion Engine

Purpose
-------
Merge FAISS and BM25 retrieval results.
===========================================================
"""


class HybridFusion:

    def __init__(self):

        self.faiss_weight = 0.60
        self.bm25_weight = 0.40

    def fuse(

        self,

        faiss_results,

        bm25_results

    ):

        fused = {}

        # -----------------------
        # FAISS Results
        # -----------------------

        for item in faiss_results:

            chunk_id = item["chunk_id"]

            fused[chunk_id] = {

                **item,

                "faiss_score": item["score"],

                "bm25_score": 0.0,

                "hybrid_score":

                    item["score"] * self.faiss_weight

            }

        # -----------------------
        # BM25 Results
        # -----------------------

        for item in bm25_results:

            chunk_id = item["chunk_id"]

            if chunk_id in fused:

                fused[chunk_id]["bm25_score"] = item["score"]

                fused[chunk_id]["hybrid_score"] += (

                    item["score"] * self.bm25_weight

                )

            else:

                fused[chunk_id] = {

                    **item,

                    "faiss_score": 0.0,

                    "bm25_score": item["score"],

                    "hybrid_score":

                        item["score"] * self.bm25_weight

                }

        results = list(

            fused.values()

        )

        results.sort(

            key=lambda x: x["hybrid_score"],

            reverse=True

        )

        return results