from fastapi import APIRouter
from .schemas import (
    ParameterGetRequest,
    ParameterResponse,
    SecretComparisonResponse,
    SecretGetRequest,
    SecretResponse,
)
from .service import secrets_service

router = APIRouter(prefix="/api/v1/secrets", tags=["🔑 Secrets & Environment Variables"])


@router.post(
    "/ssm/get-parameter",
    summary="Fetch Parameter from AWS SSM Parameter Store",
    response_model=ParameterResponse
)
def get_ssm_parameter(request: ParameterGetRequest):
    """Retrieves a hierarchical configuration parameter from AWS Systems Manager Parameter Store:
    - Demonstrates KMS decryption of `SecureString`
    - Demonstrates free-tier configuration management
    """
    return secrets_service.get_ssm_parameter(request)


@router.post(
    "/secrets-manager/get-secret",
    summary="Fetch Encrypted Secret from AWS Secrets Manager",
    response_model=SecretResponse
)
def get_secrets_manager_secret(request: SecretGetRequest):
    """Retrieves encrypted database credentials or API keys from AWS Secrets Manager:
    - Demonstrates automatic secret rotation configuration
    - Explains KMS envelope encryption
    """
    return secrets_service.get_secrets_manager_secret(request)


@router.get(
    "/compare-options",
    summary="Compare .env vs Docker Env vs SSM vs Secrets Manager",
    response_model=SecretComparisonResponse
)
def compare_secrets_options():
    """Provides a clear decision matrix comparing plain `.env` files, Docker environment variables,
    SSM Parameter Store, and AWS Secrets Manager on security, cost, and rotation.
    """
    return secrets_service.compare_secrets_options()
