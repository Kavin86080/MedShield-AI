# Placeholder for prompt_service.py
from datetime import datetime

from ai_engine.prompt_engine.prompt_engine import PromptEngine


class PromptService:

    def __init__(self):

        self.engine = PromptEngine()

        self.prompt_history = []

    def generate_prompt(
        self,
        template_name,
        question,
        context=""
    ):

        prompt = self.engine.build_prompt(
            template_name=template_name,
            question=question,
            context=context
        )

        self.prompt_history.append({
            "timestamp": datetime.now(),
            "template": template_name,
            "question": question
        })

        return prompt

    def get_prompt_history(self):

        return self.prompt_history

    def available_templates(self):

        return self.engine.get_available_templates()

    def prompt_statistics(self):

        stats = {}

        for item in self.prompt_history:

            template = item["template"]

            stats[template] = (
                stats.get(template, 0) + 1
            )

        return stats
