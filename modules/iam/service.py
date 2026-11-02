from typing import Any, Dict
from .schemas import AssumeRoleRequest, CredentialAuditRequest, PolicyEvaluationRequest


class IAMTrainingService:
    """Service stubs for IAM and Least Privilege training."""

    def evaluate_policy(self, req: PolicyEvaluationRequest) -> Dict[str, Any]:
        # TODO: Implement IAM policy evaluation or use boto3 iam.simulate_principal_policy
        # Hint: check Default Deny -> Explicit Allow -> Explicit Deny override
        raise NotImplementedError("TODO: Implement IAM policy evaluation logic.")

    def explain_auth_vs_authz(self) -> Dict[str, Any]:
        # TODO: Return your summary of Authentication (401 / Who are you) vs Authorization (403 / What can you do)
        raise NotImplementedError("TODO: Implement AuthN vs AuthZ explanation.")

    def generate_temporary_credentials(self, req: AssumeRoleRequest) -> Dict[str, Any]:
        # TODO: Call boto3 sts.assume_role(RoleArn=req.role_arn, RoleSessionName=req.role_session_name)
        # Inspect the returned AccessKeyId (starts with ASIA), SecretAccessKey, and SessionToken
        raise NotImplementedError("TODO: Implement STS AssumeRole with boto3.")

    def audit_credentials(self, req: CredentialAuditRequest) -> Dict[str, Any]:
        # TODO: Write regex scan for hardcoded AWS keys (e.g., AKIA...) and warn about dangerous practices
        raise NotImplementedError("TODO: Implement credential scanner logic.")


iam_service = IAMTrainingService()
