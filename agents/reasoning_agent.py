from agents.base_agent import BaseAgent

from ai_engine.groq_engine.groq_service import (
    GroqService
)


class ReasoningAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="ReasoningAgent"
        )

        self.llm = (
            GroqService()
        )

    def run(
        self,
        state
    ):

        if not state.contexts:

            state.answer = (
                "No relevant medical evidence found."
            )

            state.current_agent = (
                self.name
            )

            state.add_history(
                self.name
            )

            return state

        context_text = "\n\n".join(
            state.contexts[:5]
        )

        try:

            answer = (
                self.llm.generate_medical_summary(

                    question=
                    state.question,

                    context=
                    context_text
                )
            )

        except Exception as e:

            answer = (
                f"Groq Error: {str(e)}"
            )

        state.answer = answer

        state.current_agent = (
            self.name
        )

        state.add_history(
            self.name
        )

        return state