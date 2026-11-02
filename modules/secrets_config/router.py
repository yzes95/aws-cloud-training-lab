from typing import Any, Dict
from fastapi import APIRouter
from .schemas import ParameterGetRequest, SecretGetRequest
from .service import secrets_service

router = APIRouter(prefix="/api/v1/secrets", tags=["🔑 Secrets & Environment Variables"])


@router.post("/ssm/get-parameter", summary="Fetch Parameter from AWS SSM Parameter Store")
def get_ssm_parameter(request: ParameterGetRequest) -> Dict[str, Any]:
    """Retrieve parameter from SSM Parameter Store."""
    return secrets_service.get_ssm_parameter(request)


@router.post("/secrets-manager/get-secret", summary="Fetch Secret from AWS Secrets Manager")
def get_secrets_manager_secret(request: SecretGetRequest) -> Dict[str, Any]:
    """Retrieve secret value from AWS Secrets Manager."""
    return secrets_service.get_secrets_manager_secret(request)


@router.get("/compare-options", summary="Compare .env vs Docker Env vs SSM vs Secrets Manager")
def compare_secrets_options() -> Dict[str, Any]:
    """Comparison matrix for managing credentials and configs."""
    return secrets_service.compare_secrets_options()
