from typing import Any, Dict
from fastapi import APIRouter
from .schemas import (
    AssumeRoleRequest,
    CredentialAuditRequest,
    PolicyEvaluationRequest,
)
from .service import iam_service

router = APIRouter(prefix="/api/v1/iam", tags=["🔐 IAM & Least Privilege"])


@router.get("/auth-vs-authz", summary="Authentication vs Authorization & Users vs Roles")
def get_auth_vs_authz_guide() -> Dict[str, Any]:
    """Summary of AuthN vs AuthZ and IAM Users vs IAM Roles."""
    return iam_service.explain_auth_vs_authz()


@router.post("/evaluate-policy", summary="Evaluate IAM Policy against Action & Resource")
def evaluate_policy(request: PolicyEvaluationRequest) -> Dict[str, Any]:
    """Evaluate an IAM policy against requested action and resource."""
    return iam_service.evaluate_policy(request)


@router.post("/assume-role", summary="Simulate or call AWS STS AssumeRole")
def assume_role(request: AssumeRoleRequest) -> Dict[str, Any]:
    """Request temporary security credentials from AWS STS."""
    return iam_service.generate_temporary_credentials(request)


@router.post("/audit-credentials", summary="Scan snippet for hardcoded AWS keys")
def audit_credentials(request: CredentialAuditRequest) -> Dict[str, Any]:
    """Audit code or configs for hardcoded credentials."""
    return iam_service.audit_credentials(request)
