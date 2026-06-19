# Placeholder for prompt_engine.py
from ai_engine.prompt_engine.prompt_templates import (
    ZERO_SHOT_TEMPLATE,
    FEW_SHOT_TEMPLATE,
    CHAIN_OF_THOUGHT_TEMPLATE,
    REACT_TEMPLATE,
    MEDICAL_QA_TEMPLATE,
    RAG_TEMPLATE
)


class PromptEngine:

    def __init__(self):

        self.templates = {
            "zero_shot": ZERO_SHOT_TEMPLATE,
            "few_shot": FEW_SHOT_TEMPLATE,
            "cot": CHAIN_OF_THOUGHT_TEMPLATE,
            "react": REACT_TEMPLATE,
            "medical_qa": MEDICAL_QA_TEMPLATE,
            "rag": RAG_TEMPLATE
        }

    def get_available_templates(self):

        return list(self.templates.keys())

    def get_template(self, template_name):

        if template_name not in self.templates:

            raise ValueError(
                f"Template '{template_name}' not found"
            )

        return self.templates[template_name]

    def build_prompt(
        self,
        template_name,
        question,
        context=""
    ):

        template = self.get_template(
            template_name
        )

        return template.format(
            question=question,
            context=context
        )