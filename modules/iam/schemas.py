from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PolicyEvaluationRequest(BaseModel):
    user_or_role: str = Field(default="backend-service-role", description="IAM Principal executing the action")
    action: str = Field(default="s3:PutObject", description="AWS Action to perform (e.g. s3:PutObject, ec2:TerminateInstances)")
    resource_arn: str = Field(
        default="arn:aws:s3:::ataa-verification-documents/cases/*",
        description="Target AWS Resource ARN"
    )
    policy_json: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Custom IAM Policy JSON. If omitted, uses default Least Privilege policy."
    )


class PolicyEvaluationResponse(BaseModel):
    allowed: bool
    decision_reason: str
    evaluation_logic: List[str]
    is_least_privilege_compliant: bool
    recommendations: List[str]


class AssumeRoleRequest(BaseModel):
    role_arn: str = Field(default="arn:aws:iam::123456789012:role/AtaaEC2S3UploadRole")
    role_session_name: str = Field(default="DonationUploadSession")
    duration_seconds: int = Field(default=3600, ge=900, le=43200)


class TemporaryCredentialsResponse(BaseModel):
    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: str
    credential_type: str
    why_temporary_is_safer: str


class CredentialAuditRequest(BaseModel):
    code_or_config_snippet: str = Field(
        description="Code or environment file content to audit for exposed credentials",
        default="AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'\nAWS_SECRET_ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'"
    )


class CredentialAuditResponse(BaseModel):
    found_secrets: bool
    risk_level: str
    findings: List[Dict[str, str]]
    remediation_guide: str
