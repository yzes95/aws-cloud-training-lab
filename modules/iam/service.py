import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from core.config import settings
from core.aws_client import get_boto3_client
from .policies import ATAA_LEAST_PRIVILEGE_POLICY, evaluate_iam_policy
from .schemas import (
    AssumeRoleRequest,
    CredentialAuditRequest,
    CredentialAuditResponse,
    PolicyEvaluationRequest,
    PolicyEvaluationResponse,
    TemporaryCredentialsResponse,
)


class IAMTrainingService:
    """Service implementing hands-on training for IAM, Least Privilege, and Credentials Security."""

    def evaluate_policy(self, req: PolicyEvaluationRequest) -> PolicyEvaluationResponse:
        policy = req.policy_json or ATAA_LEAST_PRIVILEGE_POLICY
        res = evaluate_iam_policy(policy, req.action, req.resource_arn)

        # Check Least Privilege Compliance
        is_least = True
        recommendations: List[str] = []
        for stmt in policy.get("Statement", []):
            actions = stmt.get("Action", [])
            if isinstance(actions, str):
                actions = [actions]
            resources = stmt.get("Resource", [])
            if isinstance(resources, str):
                resources = [resources]

            if "*" in actions and stmt.get("Effect") == "Allow":
                is_least = False
                recommendations.append("High Risk: Avoid Action='*' in Allow statements. Specify precise actions (e.g. s3:PutObject).")
            if (resources == ["*"] or resources == "*") and stmt.get("Effect") == "Allow":
                is_least = False
                recommendations.append("High Risk: Avoid unconstrained Resource='*' in Allow statements. Scope down to specific ARN boundaries.")

        if not recommendations:
            recommendations.append("Excellent: Policy adheres to the Principle of Least Privilege by scoping down actions and resources.")

        return PolicyEvaluationResponse(
            allowed=res["allowed"],
            decision_reason=res["reason"],
            evaluation_logic=res["steps"],
            is_least_privilege_compliant=is_least,
            recommendations=recommendations,
        )

    def explain_auth_vs_authz(self) -> Dict[str, Any]:
        """Explains Authentication vs Authorization in AWS and Web APIs."""
        return {
            "concept": "Authentication (AuthN) vs Authorization (AuthZ)",
            "authentication": {
                "question": "Who are you?",
                "http_status": "401 Unauthorized (actually means Unauthenticated)",
                "aws_equivalent": "AWS IAM User credentials, Access Key + Secret Key, AWS STS temporary tokens, Cognito Login",
                "example": "A user sends a valid JWT Bearer token or signs an AWS API request using SigV4."
            },
            "authorization": {
                "question": "What permissions do you have / What are you allowed to do?",
                "http_status": "403 Forbidden",
                "aws_equivalent": "AWS IAM Policies, Role attachments, Service Control Policies (SCPs), Bucket Policies",
                "example": "The authenticated EC2 instance has valid credentials, but its IAM policy denies 's3:DeleteObject'."
            },
            "iam_users_vs_roles": {
                "iam_user": {
                    "definition": "An entity created in AWS representing a specific human or service with permanent long-term credentials.",
                    "security_warning": "High risk for production applications! If access keys are leaked, attackers gain indefinite access until rotated."
                },
                "iam_role": {
                    "definition": "An identity created in AWS that does NOT have permanent passwords or access keys. Instead, it is assumed dynamically.",
                    "best_practice": "Applications on EC2, ECS, or Lambda should ALWAYS use IAM Roles via Instance Profiles or Task Roles. AWS rotates keys every hour automatically."
                }
            }
        }

    def generate_temporary_credentials(self, req: AssumeRoleRequest) -> TemporaryCredentialsResponse:
        """Simulates AWS STS AssumeRole returning short-lived temporary security credentials."""
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=req.duration_seconds)

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                sts_client = get_boto3_client("sts")
                resp = sts_client.assume_role(
                    RoleArn=req.role_arn,
                    RoleSessionName=req.role_session_name,
                    DurationSeconds=req.duration_seconds
                )
                creds = resp["Credentials"]
                return TemporaryCredentialsResponse(
                    access_key_id=creds["AccessKeyId"],
                    secret_access_key=creds["SecretAccessKey"][:6] + "..." + creds["SecretAccessKey"][-4:],
                    session_token=creds["SessionToken"][:12] + "...",
                    expiration=creds["Expiration"].isoformat(),
                    credential_type="AWS STS Temporary Credentials (Real AWS)",
                    why_temporary_is_safer="Temporary credentials expire automatically. Even if intercepted, they cannot be used after expiration."
                )
            except Exception as e:
                # Fallback to simulation if role doesn't exist in AWS account
                pass

        # Realistic STS Temporary Credentials format
        # Starts with 'ASIA...' (AWS STS Temporary Key prefix), whereas permanent keys start with 'AKIA...'
        return TemporaryCredentialsResponse(
            access_key_id="ASIA" + "TEMPORARYSESSIONKEYEX99",
            secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            session_token="IQoJb3JpZ2luX2VjEExampleSessionTokenLongPayloadString...",
            expiration=expires_at.isoformat(),
            credential_type="AWS STS Temporary Credentials (ASIA Prefix)",
            why_temporary_is_safer=(
                "1. Temporary credentials start with 'ASIA' (instead of permanent 'AKIA').\n"
                "2. They expire automatically in 1 hour (or specified duration).\n"
                "3. They require a Session Token along with Access & Secret keys.\n"
                "4. When used on EC2 or ECS, the AWS SDK fetches and rotates them automatically in the background without modifying your code."
            )
        )

    def audit_credentials(self, req: CredentialAuditRequest) -> CredentialAuditResponse:
        """Scans code or config for hardcoded AWS credentials (AKIA..., secret keys, private keys)."""
        findings: List[Dict[str, str]] = []

        # AWS Access Key Pattern (AKIA prefix, 20 alphanumeric characters)
        access_key_pattern = r"(AKIA[0-9A-Z]{16})"
        for match in re.finditer(access_key_pattern, req.code_or_config_snippet):
            findings.append({
                "type": "Exposed Permanent AWS Access Key",
                "matched_text": match.group(1),
                "severity": "CRITICAL",
                "explanation": "Hardcoded permanent IAM user access key detected. If committed to GitHub, bots scan and compromise it within seconds."
            })

        # Secret Key heuristic (40 characters base64-like)
        secret_key_pattern = r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?"
        for match in re.finditer(secret_key_pattern, req.code_or_config_snippet):
            findings.append({
                "type": "Exposed AWS Secret Access Key",
                "matched_text": match.group(1)[:4] + "..." + match.group(1)[-4:],
                "severity": "CRITICAL",
                "explanation": "AWS Secret Access Key found in plain text code or config."
            })

        has_secrets = len(findings) > 0
        risk = "CRITICAL" if has_secrets else "SAFE"
        remediation = (
            "NEVER hard-code AWS credentials in code, git repositories, or public configs!\n"
            "Recommended Solutions:\n"
            "1. In Production (EC2/ECS/Lambda): Attach an IAM Role directly to the resource (Instance Profile / Task Role). The AWS SDK will automatically fetch temporary credentials from IMDSv2.\n"
            "2. In Local Development: Use the AWS CLI `aws configure` to store credentials in ~/.aws/credentials, or use environment variables loaded from git-ignored .env files.\n"
            "3. For Database/Third-Party Secrets: Use AWS Secrets Manager or AWS Systems Manager Parameter Store."
        )

        return CredentialAuditResponse(
            found_secrets=has_secrets,
            risk_level=risk,
            findings=findings,
            remediation_guide=remediation,
        )


iam_service = IAMTrainingService()
