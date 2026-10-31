from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class CreateBucketRequest(BaseModel):
    bucket_name: str = Field(default="ataa-verification-docs-demo", description="Globally unique S3 bucket name")
    enable_versioning: bool = Field(default=True, description="Enable S3 object versioning to prevent accidental deletions")
    block_public_access: bool = Field(default=True, description="Always enforce S3 Block Public Access for security")


class CreateBucketResponse(BaseModel):
    bucket_name: str
    arn: str
    region: str
    versioning_status: str
    public_access_blocked: bool
    encryption: str
    status: str


class UploadObjectRequest(BaseModel):
    bucket_name: str = Field(default="ataa-verification-docs-demo")
    object_key: str = Field(default="families/family_01/national_id.pdf", description="S3 Key / path inside the bucket")
    content: str = Field(default="Simulated binary PDF bytes of family verification document", description="Text or document content")
    content_type: str = Field(default="application/pdf")
    metadata: Dict[str, str] = Field(
        default={"family_id": "FAM-101", "researcher": "social_worker_ahmed"},
        description="User-defined metadata tags"
    )


class UploadObjectResponse(BaseModel):
    bucket_name: str
    object_key: str
    etag: str
    version_id: Optional[str]
    s3_uri: str
    https_url: str
    server_side_encryption: str


class PresignedUrlRequest(BaseModel):
    bucket_name: str = Field(default="ataa-verification-docs-demo")
    object_key: str = Field(default="families/family_01/medical_report.pdf")
    operation: str = Field(default="put_object", description="'put_object' for client upload, 'get_object' for secure client download")
    expiration_seconds: int = Field(default=900, ge=60, le=86400, description="Expiration time in seconds (default: 15 minutes)")


class PresignedUrlResponse(BaseModel):
    presigned_url: str
    expires_in_seconds: int
    operation: str
    http_method: str
    why_presigned_urls_are_essential: str
    architecture_benefit: str


class StorageClassesResponse(BaseModel):
    durability: str
    classes: Dict[str, Any]
    decision_flowchart: str
