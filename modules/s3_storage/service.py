from typing import Any, Dict
from core.aws_client import get_boto3_client
from .schemas import (
    CreateBucketRequest,
    PresignedUrlRequest,
    UploadObjectRequest,
)


class S3StorageService:
    """Service stubs for Amazon S3 operations."""

    def create_bucket(self, req: CreateBucketRequest) -> Dict[str, Any]:
        # TODO: Use boto3 s3 client:
        # s3.create_bucket(Bucket=req.bucket_name, ...)
        # If req.enable_versioning: s3.put_bucket_versioning(...)
        # If req.block_public_access: s3.put_public_access_block(...)
        raise NotImplementedError("TODO: Implement S3 create_bucket with boto3.")

    def upload_object(self, req: UploadObjectRequest) -> Dict[str, Any]:
        # TODO: Use boto3 s3.put_object(Bucket=req.bucket_name, Key=req.object_key, Body=..., ...)
        raise NotImplementedError("TODO: Implement S3 upload_object with boto3.")

    def generate_presigned_url(self, req: PresignedUrlRequest) -> Dict[str, Any]:
        # TODO: Use boto3 s3.generate_presigned_url(ClientMethod=req.operation, Params={...}, ExpiresIn=...)
        # Explain why presigned URLs allow direct client upload without proxying file bytes through FastAPI.
        raise NotImplementedError("TODO: Implement S3 generate_presigned_url with boto3.")

    def get_storage_classes_guide(self) -> Dict[str, Any]:
        # TODO: Return your summary of S3 Storage Classes (Standard, IA, Glacier, Deep Archive) and Lifecycle rules.
        raise NotImplementedError("TODO: Implement S3 storage classes guide.")


s3_service = S3StorageService()
