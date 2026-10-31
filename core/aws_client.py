"""AWS Boto3 Client Factory with LocalStack and Mock Mode Support."""
import logging
from typing import Any, Optional
from core.config import settings

logger = logging.getLogger("aws_client")

try:
    import boto3
    from botocore.config import Config
    BOTO3_AVAILABLE = True
except ImportError:
    boto3 = None  # type: ignore
    Config = None  # type: ignore
    BOTO3_AVAILABLE = False


def get_boto3_client(service_name: str) -> Any:
    """Creates a boto3 client configured for either real AWS, LocalStack, or mock mode.
    
    If boto3 is not installed or settings.AWS_MOCK_MODE is True, callers can use the built-in
    offline mock implementations in each module.
    """
    if not BOTO3_AVAILABLE:
        raise ImportError(
            f"boto3 is not installed in the current Python environment. "
            f"Install it via `pip install boto3` or set AWS_MOCK_MODE=True in .env."
        )

    client_kwargs: dict[str, Any] = {
        "service_name": service_name,
        "region_name": settings.AWS_REGION,
        "config": Config(
            retries={"max_attempts": 3, "mode": "standard"},
            connect_timeout=5,
            read_timeout=10,
        ),
    }

    # If LocalStack URL is provided, route boto3 requests to LocalStack
    if settings.LOCALSTACK_ENDPOINT_URL:
        client_kwargs["endpoint_url"] = settings.LOCALSTACK_ENDPOINT_URL
        client_kwargs["aws_access_key_id"] = "test"
        client_kwargs["aws_secret_access_key"] = "test"
        logger.info(f"Connecting to LocalStack {service_name} at {settings.LOCALSTACK_ENDPOINT_URL}")
        return boto3.client(**client_kwargs)

    # If real credentials are provided
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        client_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        client_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
        if settings.AWS_SESSION_TOKEN:
            client_kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN
        return boto3.client(**client_kwargs)

    # Otherwise fallback to default AWS credentials provider chain
    return boto3.client(**client_kwargs)
