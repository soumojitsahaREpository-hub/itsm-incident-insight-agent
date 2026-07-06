from src.agent.intent_parser import parse_user_intent


def test_sla_distribution_maps_to_expected_query_id():
    result = parse_user_intent("Show SLA distribution.")
    assert result["query_id"] == "sla_distribution"


def test_chart_request_maps_to_chart_intent_and_pie_type():
    result = parse_user_intent("Create a pie chart of SLA distribution.")
    assert result["intent"] == "create_chart"
    assert result["chart_type"] == "pie"


def test_priority_distribution_maps_to_expected_query_id():
    result = parse_user_intent("Create a bar chart of priority distribution.")
    assert result["query_id"] == "priority_distribution"


def test_delete_request_returns_refuse_intent():
    result = parse_user_intent("Delete all incident records.")
    assert result["intent"] == "refuse"
