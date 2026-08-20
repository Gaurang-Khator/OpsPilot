from app.data.mock_logs import LOGS

def search_logs_tool(keyword: str) -> list[str]:
    """Search application logs for lines containing the given keyword (case-insensitive)."""

    keyword_lower = keyword.lower()

    return [ line for line in LOGS if keyword_lower in line.lower() ]