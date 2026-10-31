from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ParameterGetRequest(BaseModel):
    parameter_path: str = Field(
        default="/ataa/production/database/url",
        description="SSM Parameter Store hierarchical path"
    )
    with_decryption: bool = Field(default=True, description="Whether to decrypt SecureString using AWS KMS")


class ParameterResponse(BaseModel):
    name: str
    type: str  # String, StringList, SecureString
    value: str
    arn: str
    version: int
    kms_key_id: Optional[str] = None
    security_explanation: str


class SecretGetRequest(BaseModel):
    secret_id: str = Field(
        default="ataa/production/jwt-secret",
        description="Secrets Manager Secret Name or ARN"
    )


class SecretResponse(BaseModel):
    secret_id: str
    secret_value: Dict[str, Any]
    arn: str
    version_id: str
    rotation_enabled: bool
    rotation_rules: Dict[str, Any]
    security_explanation: str


class SecretComparisonResponse(BaseModel):
    comparison_table: Dict[str, Any]
    best_practice_recommendation: str
