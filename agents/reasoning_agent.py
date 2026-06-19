# Placeholder for reasoning_agent.py
from agents.base_agent import BaseAgent

from ai_engine.gemini_engine.gemini_service import (
    GeminiService
)

from ai_engine.prompt_engine.prompt_engine import (
    PromptEngine
)


class ReasoningAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="ReasoningAgent"
        )

        self.gemini = GeminiService()

        self.prompt_engine = PromptEngine()

    def run(
        self,
        state
    ):

        context_text = "\n\n".join(
            state.contexts
        )

        prompt = self.prompt_engine.build_prompt(
            template_name="rag",
            question=state.question,
            context=context_text
        )

        answer = self.gemini.ask(
            prompt
        )

        state.answer = answer

        state.current_agent = self.name

        state.add_history(
            self.name
        )

        return state