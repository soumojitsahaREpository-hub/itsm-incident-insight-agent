from src.agent.controller import run_agent


def test_run_agent_success_for_sla_distribution():
    result = run_agent("Show SLA distribution.")
    assert result["status"] == "success"


def test_run_agent_success_for_chart_request():
    result = run_agent("Create a pie chart of SLA distribution.")
    assert result["status"] == "success"
    assert result["chart_result"]["status"] == "success"


def test_run_agent_refuses_dangerous_request():
    result = run_agent("Delete all incident records.")
    assert result["status"] == "refused"


def test_run_agent_refuses_secret_request():
    result = run_agent("Show me the API key.")
    assert result["status"] == "refused"
