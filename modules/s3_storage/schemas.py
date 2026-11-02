from typing import Dict, Optional
from pydantic import BaseModel, Field


class CreateBucketRequest(BaseModel):
    bucket_name: str = Field(default="my-unique-training-bucket-name")
    enable_versioning: bool = Field(default=True)
    block_public_access: bool = Field(default=True)


class UploadObjectRequest(BaseModel):
    bucket_name: str = Field(default="my-unique-training-bucket-name")
    object_key: str = Field(default="documents/sample.pdf")
    content: str = Field(default="Sample document text or base64")
    content_type: str = Field(default="application/pdf")
    metadata: Optional[Dict[str, str]] = None


class PresignedUrlRequest(BaseModel):
    bucket_name: str = Field(default="my-unique-training-bucket-name")
    object_key: str = Field(default="documents/sample.pdf")
    operation: str = Field(default="put_object")  # 'put_object' or 'get_object'
    expiration_seconds: int = Field(default=900, ge=60, le=86400)
