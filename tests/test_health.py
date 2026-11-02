"""Health check and baseline tests."""
from main import health_check


def test_health():
    res = health_check()
    assert res["status"] == "healthy"
    assert "aws_region" in res
    assert res["swagger_docs"] == "/docs"
