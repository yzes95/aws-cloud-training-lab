from fastapi import APIRouter
from .schemas import (
    CreateBucketRequest,
    CreateBucketResponse,
    PresignedUrlRequest,
    PresignedUrlResponse,
    StorageClassesResponse,
    UploadObjectRequest,
    UploadObjectResponse,
)
from .service import s3_service

router = APIRouter(prefix="/api/v1/s3", tags=["🪣 S3 Object Storage"])


@router.post(
    "/create-bucket",
    summary="Create S3 Bucket with Versioning & Public Block",
    response_model=CreateBucketResponse
)
def create_bucket(request: CreateBucketRequest):
    """Creates a secure S3 bucket following AWS best practices:
    - S3 Block Public Access enabled
    - Object Versioning enabled
    - Default SSE-S3 encryption applied
    """
    return s3_service.create_bucket(request)


@router.post(
    "/upload-object",
    summary="Upload Object with Metadata Tags",
    response_model=UploadObjectResponse
)
def upload_object(request: UploadObjectRequest):
    """Uploads an object (document/file) to an S3 bucket with user-defined metadata and server-side encryption."""
    return s3_service.upload_object(request)


@router.post(
    "/generate-presigned-url",
    summary="Generate S3 Presigned URL for Direct Browser Upload/Download",
    response_model=PresignedUrlResponse
)
def generate_presigned_url(request: PresignedUrlRequest):
    """Generates a secure, temporary presigned URL:
    - Allows frontend browser clients to upload files directly to S3 without sending file bytes through FastAPI!
    - Completely eliminates exposing AWS secret keys to clients
    """
    return s3_service.generate_presigned_url(request)


@router.get(
    "/storage-classes",
    summary="S3 Storage Classes & Lifecycle Rules Guide",
    response_model=StorageClassesResponse
)
def get_storage_classes():
    """Returns an interactive guide comparing S3 Standard, Intelligent-Tiering, Standard-IA, Glacier, and Deep Archive."""
    return s3_service.get_storage_classes_guide()
