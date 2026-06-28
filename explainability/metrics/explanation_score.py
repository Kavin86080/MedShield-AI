class ExplanationScore:

    @staticmethod
    def calculate(
        confidence,
        shap_importance
    ):

        confidence_component = (
            confidence / 100
        ) * 70

        shap_component = (
            shap_importance
        ) * 30

        final_score = (
            confidence_component
            +
            shap_component
        )

        return round(
            final_score,
            2
        )