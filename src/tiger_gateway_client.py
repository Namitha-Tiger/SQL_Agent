import requests

from .config import get_settings
from urllib.parse import urljoin


class TigerGatewayClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _call_llm(self, messages: list[dict]) -> str:
        """
        Sends a request to the Tiger AI Gateway and returns the
        generated response text.
        """

        response = requests.post(
            urljoin(self.settings.llm_base_url, "v1/chat/completions"),
            headers={
                "Authorization": f"Bearer {self.settings.llm_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.settings.llm_model,
                "messages": messages,
                "temperature": 0,
            },
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"].strip()

    def generate_sql(self, question: str, schema: str, history: str) -> str:
        """
        Uses the LLM to generate a MySQL SELECT query.
        """

        system_prompt = f"""
        You are an expert MySQL SQL generator.

        Rules:
       - Generate exactly one valid MySQL SQL statement that answers the user's request.
        - Return only SQL.
        - Never include explanations or markdown.
        - If the user asks a follow-up question, use the previous conversation context.
        - If the follow-up refers to "it", "them", "those", "same", etc., resolve it using the conversation history.

        Database Schema:

        {schema}
        """

        user_prompt = f"""
        Previous Conversation:

        {history}

        Current User Question:

        {question}
        """

        return self._call_llm(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

    def summarize(
        self,
        question: str,
        sql: str,
        rows: list[dict],
    ) -> str:
        """
        Converts SQL results into a business-friendly explanation.
        """

        system_prompt = """
You are a business analyst.

Answer only using the SQL result.

If no rows are returned, clearly say that no matching data was found.

Do not invent information.
"""

        user_prompt = f"""
User Question:

{question}

Executed SQL:

{sql}

Returned Rows:

{rows}

Provide a concise business summary.
"""

        return self._call_llm(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )