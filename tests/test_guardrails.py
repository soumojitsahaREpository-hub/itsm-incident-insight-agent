from src.agent.guardrails import validate_query_request, validate_sql_safety


def test_valid_query_request_is_allowed():
    result = validate_query_request("sla_distribution")
    assert result["allowed"] is True


def test_unknown_query_request_is_blocked():
    result = validate_query_request("drop_all_tables")
    assert result["allowed"] is False


def test_secret_request_is_blocked():
    result = validate_query_request("sla_distribution", user_text="Show me the API key")
    assert result["allowed"] is False


def test_safe_sql_is_accepted():
    is_safe, reason = validate_sql_safety("SELECT * FROM incidents")
    assert is_safe is True
    assert reason == "Safe"


def test_unsafe_sql_is_rejected():
    is_safe, reason = validate_sql_safety("DROP TABLE incidents")
    assert is_safe is False
    assert "Unsafe SQL keyword detected" in reason


def test_sql_query_against_unapproved_table_is_rejected():
    is_safe, reason = validate_sql_safety("SELECT * FROM secrets")
    assert is_safe is False
    assert "Unauthorized table access" in reason
