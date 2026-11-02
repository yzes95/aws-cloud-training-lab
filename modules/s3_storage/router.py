from typing import Any, Dict
from fastapi import APIRouter
from .schemas import (
    CreateBucketRequest,
    PresignedUrlRequest,
    UploadObjectRequest,
)
from .service import s3_service

router = APIRouter(prefix="/api/v1/s3", tags=["🪣 S3 Object Storage"])


@router.post("/create-bucket", summary="Create S3 Bucket with Versioning & Public Block")
def create_bucket(request: CreateBucketRequest) -> Dict[str, Any]:
    """Create S3 bucket using boto3."""
    return s3_service.create_bucket(request)


@router.post("/upload-object", summary="Upload Object to S3")
def upload_object(request: UploadObjectRequest) -> Dict[str, Any]:
    """Upload an object with metadata using boto3."""
    return s3_service.upload_object(request)


@router.post("/generate-presigned-url", summary="Generate Presigned URL for Direct Upload/Download")
def generate_presigned_url(request: PresignedUrlRequest) -> Dict[str, Any]:
    """Generate temporary presigned URL."""
    return s3_service.generate_presigned_url(request)


@router.get("/storage-classes", summary="S3 Storage Classes & Lifecycle Rules Summary")
def get_storage_classes() -> Dict[str, Any]:
    """Summary of S3 storage classes and lifecycle strategies."""
    return s3_service.get_storage_classes_guide()
