import requests
import openai

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

        llm_base_url = self.settings.llm_base_url
        if llm_base_url is None:
            raise ValueError("LLM base URL is not configured.")

        # response = requests.post(
        #     urljoin(llm_base_url, "v1/chat/completions"),
        #     headers={
        #         "Authorization": f"Bearer {self.settings.llm_api_key}",
        #         "Content-Type": "application/json",
        #     },
        #     json={
        #         "model": self.settings.llm_model,
        #         "messages": messages,
        #         "temperature": 0,
        #     },
        #     timeout=60,
        # )
        client = openai.OpenAI(api_key=self.settings.llm_api_key, base_url=llm_base_url)
        response = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=messages,
            temperature=0
        )

        # response.raise_for_status()

        # result = response.json()

        # return result["choices"][0]["message"]["content"].strip()
        return response.choices[0].message.content.strip()

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
                        You are a business analyst preparing insights for business users.

                        Rules:
                        - Answer only using the SQL result.
                        - Do not invent or assume information that is not present in the result.
                        - If no rows are returned, respond: "No matching data was found."
                        - Write 2-4 complete sentences.
                        - Start with the key finding.
                        - Then explain why the result is important from a business perspective.
                        - Use clear, professional business language instead of simply repeating the SQL result.
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