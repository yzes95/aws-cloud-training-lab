"""Tests for the 2-endpoint AWS training app.

Run locally with:
    pytest test_main.py -v
"""
from main import health_check


def test_health_endpoint():
    """Verifies that GET /health returns healthy status (used by CI/CD test gate)."""
    res = health_check()
    assert res["status"] == "healthy"


# TODO: Add a test for creating and listing items once `db.py` and `aws_services.py` are implemented.
