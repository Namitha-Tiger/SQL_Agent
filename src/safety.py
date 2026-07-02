import re

# SQL keywords that are not allowed.
BLOCKED_KEYWORDS = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "grant",
    "revoke",
    "merge",
    "call",
    "execute",
)


def validate_sql(sql: str) -> str:
    """
    Validate that the SQL is a single safe SELECT statement.

    Returns
    -------
    str
        The cleaned SQL statement.

    Raises
    ------
    ValueError
        If the SQL is considered unsafe.
    """

    if not sql:
        raise ValueError("Empty SQL statement.")

    cleaned = sql.strip()

    # Remove markdown code fences if the LLM returns them.
    cleaned = cleaned.replace("```sql", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    # Remove trailing semicolon.
    cleaned = cleaned.rstrip(";").strip()

    if not cleaned:
        raise ValueError("Empty SQL statement.")

    lower_sql = cleaned.lower()

    # Only SELECT statements are allowed.
    if not lower_sql.startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")

    # Block multiple statements.
    if ";" in cleaned:
        raise ValueError("Multiple SQL statements are not allowed.")

    # Block destructive keywords.
    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lower_sql):
            raise ValueError("Destructive or write SQL is blocked.")

    # Block SQL comments.
    if "--" in cleaned or "/*" in cleaned or "*/" in cleaned:
        raise ValueError("SQL comments are not allowed.")

    return cleaned
