from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class PolicyEvaluationRequest(BaseModel):
    user_or_role: str = Field(default="backend-service-role")
    action: str = Field(default="s3:PutObject")
    resource_arn: str = Field(default="arn:aws:s3:::my-bucket/files/*")
    policy_json: Optional[Dict[str, Any]] = None


class AssumeRoleRequest(BaseModel):
    role_arn: str = Field(default="arn:aws:iam::123456789012:role/MyServiceRole")
    role_session_name: str = Field(default="TrainingSession")
    duration_seconds: int = Field(default=3600, ge=900, le=43200)


class CredentialAuditRequest(BaseModel):
    code_or_config_snippet: str = Field(
        default="AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'"
    )
