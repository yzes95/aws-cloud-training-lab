"""AWS Boto3 Client Factory."""
import logging
from typing import Any
from core.config import settings

logger = logging.getLogger("aws_client")

try:
    import boto3
    from botocore.config import Config
except ImportError:
    boto3 = None  # type: ignore
    Config = None  # type: ignore


def get_boto3_client(service_name: str) -> Any:
    """Returns a boto3 client targeting real AWS or LocalStack.
    
    Resolves credentials via standard AWS credential chain.
    """
    if boto3 is None:
        raise RuntimeError("boto3 is not installed. Please run `pip install -r requirements.txt`.")

    client_kwargs: dict[str, Any] = {
        "service_name": service_name,
        "region_name": settings.AWS_REGION,
        "config": Config(
            retries={"max_attempts": 3, "mode": "standard"},
            connect_timeout=5,
            read_timeout=10,
        ),
    }

    if settings.LOCALSTACK_ENDPOINT_URL:
        client_kwargs["endpoint_url"] = settings.LOCALSTACK_ENDPOINT_URL
        client_kwargs["aws_access_key_id"] = "test"
        client_kwargs["aws_secret_access_key"] = "test"
        logger.info(f"Targeting LocalStack for {service_name} at {settings.LOCALSTACK_ENDPOINT_URL}")

    return boto3.client(**client_kwargs)
