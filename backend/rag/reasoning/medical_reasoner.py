"""
===========================================================
MedShield-X

Medical Reasoner
===========================================================
"""


class MedicalReasoner:

    def reason(

        self,

        retrieval_result

    ):

        evidence = retrieval_result["evidence"]

        reasoning = {

            "summary": "",

            "supporting_evidence": [],

            "limitations": []

        }

        summary = []

        for item in evidence:

            summary.append(

                item["text"]

            )

            reasoning[

                "supporting_evidence"

            ].append(

                {

                    "chunk_id": item["chunk_id"],

                    "score": item["score"]

                }

            )

        reasoning["summary"] = "\n".join(

            summary

        )

        if len(evidence) < 3:

            reasoning["limitations"].append(

                "Limited supporting evidence retrieved."

            )

        retrieval_result["reasoning"] = reasoning

        return retrieval_result