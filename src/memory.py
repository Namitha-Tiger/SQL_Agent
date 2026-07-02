from typing import Any


class MemoryManager:
    """
    Helper class for working with LangGraph state.
    """

    @staticmethod
    def add_interaction(state: dict[str, Any]) -> list[dict]:
        """
        Append the current interaction to conversation history.
        """

        history = state.get("history", [])

        history.append(
            {
                "question": state["question"],
                "sql": state["sql"],
                "answer": state["answer"],
            }
        )

        return history

    @staticmethod
    def format_history(history: list[dict], limit: int = 5) -> str:
        """
        Convert previous interactions into text for the LLM prompt.
        """

        if not history:
            return "No previous conversation."

        context = []

        for item in history[-limit:]:
            context.append(
                f"""
Question:
{item['question']}

SQL:
{item['sql']}

Answer:
{item['answer']}
"""
            )

        return "\n".join(context)