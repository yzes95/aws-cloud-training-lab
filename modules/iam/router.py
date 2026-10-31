from typing import Any, Dict
from fastapi import APIRouter, status
from .schemas import (
    AssumeRoleRequest,
    CredentialAuditRequest,
    CredentialAuditResponse,
    PolicyEvaluationRequest,
    PolicyEvaluationResponse,
    TemporaryCredentialsResponse,
)
from .service import iam_service

router = APIRouter(prefix="/api/v1/iam", tags=["🔐 IAM & Least Privilege"])


@router.get(
    "/auth-vs-authz",
    summary="Interactive Guide: Authentication vs Authorization & Users vs Roles",
    response_model=Dict[str, Any]
)
def get_auth_vs_authz_guide():
    """Detailed walkthrough explaining:
    - Authentication (AuthN - 401) vs Authorization (AuthZ - 403)
    - IAM Users (long-term permanent keys) vs IAM Roles (temporary STS credentials)
    - Why IAM Roles are required for EC2, ECS, and Lambda
    """
    return iam_service.explain_auth_vs_authz()


@router.post(
    "/evaluate-policy",
    summary="Evaluate an IAM Policy against an Action & Resource",
    response_model=PolicyEvaluationResponse,
    status_code=status.HTTP_200_OK
)
def evaluate_policy(request: PolicyEvaluationRequest):
    """Simulates AWS IAM policy evaluation:
    - Tests Default Deny -> Explicit Allow -> Explicit Deny Override
    - Validates whether the policy adheres to Least Privilege (no wildcards `*` in Allow)
    """
    return iam_service.evaluate_policy(request)


@router.post(
    "/assume-role-simulation",
    summary="Simulate AWS STS AssumeRole (Temporary Credentials)",
    response_model=TemporaryCredentialsResponse
)
def simulate_assume_role(request: AssumeRoleRequest):
    """Demonstrates how AWS STS returns temporary credentials (`ASIA...`) with expiration:
    - Shows how EC2 Instance Profiles obtain credentials automatically
    - Explains why temporary credentials eliminate credential leak risks
    """
    return iam_service.generate_temporary_credentials(request)


@router.post(
    "/audit-credentials",
    summary="Static Credential Auditor: Detect Hardcoded AWS Keys",
    response_model=CredentialAuditResponse
)
def audit_credentials(request: CredentialAuditRequest):
    """Scans code snippets or configuration files for hardcoded AWS keys (`AKIA...`):
    - Demonstrates why committing credentials to GitHub leads to immediate AWS account compromise
    - Returns remediation steps using IAM Roles and Secrets Manager
    """
    return iam_service.audit_credentials(request)
