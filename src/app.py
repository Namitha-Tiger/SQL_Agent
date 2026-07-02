from .graph import SQLAgentGraph
from .sql_tools import create_connection


class SQLAgentApp:
    def __init__(self) -> None:
        self.connection = create_connection()
        self.agent = SQLAgentGraph(self.connection)

    def run(self, question: str) -> dict:
        """
        Execute one complete LangGraph workflow.
        """
        return self.agent.invoke(question)

    def close(self) -> None:
        """
        Close the database connection.
        """
        if self.connection.is_connected():
            self.connection.close()


def main() -> None:
    print("=" * 60)
    print("Retail SQL Agent")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    app = SQLAgentApp()

    try:
        while True:
            question = input("\nQuestion: ").strip()

            if question.lower() in {"exit", "quit"}:
                break

            if not question:
                continue

            try:
                result = app.run(question)

                print("\nGenerated SQL")
                print("-" * 60)
                print(result.get("sql", ""))

                print("\nAnswer")
                print("-" * 60)
                print(result.get("answer", ""))

                rows = result.get("rows", [])

                print("\nRows Returned:", len(rows))

                if rows:
                    print("\nSample Rows")
                    print("-" * 60)
                    for row in rows[:5]:
                        print(row)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        app.close()


if __name__ == "__main__":
    main()