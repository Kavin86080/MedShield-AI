"""
===========================================================
MedShield-X

Confidence Score
===========================================================
"""


class ConfidenceScore:

    def calculate(

        self,

        retrieval_result

    ):

        evidence = retrieval_result["evidence"]

        if not evidence:

            retrieval_result["confidence"] = 0.0

            return retrieval_result

        scores = [

            item["score"]

            for item in evidence

        ]

        confidence = (

            sum(scores)

            / len(scores)

        )

        confidence = round(

            confidence,

            3

        )

        retrieval_result["confidence"] = confidence

        return retrieval_result