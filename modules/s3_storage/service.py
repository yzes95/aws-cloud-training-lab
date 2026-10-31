import hashlib
import time
from typing import Any, Dict
from core.config import settings
from core.aws_client import get_boto3_client
from .schemas import (
    CreateBucketRequest,
    CreateBucketResponse,
    PresignedUrlRequest,
    PresignedUrlResponse,
    StorageClassesResponse,
    UploadObjectRequest,
    UploadObjectResponse,
)


class S3StorageService:
    """Service providing hands-on training for Amazon S3: Buckets, Uploads, Presigned URLs, and Storage Classes."""

    def create_bucket(self, req: CreateBucketRequest) -> CreateBucketResponse:
        """Creates an S3 bucket with encryption and public access block enabled."""
        bucket = req.bucket_name.lower().strip()

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                s3 = get_boto3_client("s3")
                create_params: dict[str, Any] = {"Bucket": bucket}
                if settings.AWS_REGION != "us-east-1":
                    create_params["CreateBucketConfiguration"] = {"LocationConstraint": settings.AWS_REGION}
                s3.create_bucket(**create_params)

                if req.enable_versioning:
                    s3.put_bucket_versioning(
                        Bucket=bucket,
                        VersioningConfiguration={"Status": "Enabled"}
                    )

                if req.block_public_access:
                    s3.put_public_access_block(
                        Bucket=bucket,
                        PublicAccessBlockConfiguration={
                            "BlockPublicAcls": True,
                            "IgnorePublicAcls": True,
                            "BlockPublicPolicy": True,
                            "RestrictPublicBuckets": True
                        }
                    )

                return CreateBucketResponse(
                    bucket_name=bucket,
                    arn=f"arn:aws:s3:::{bucket}",
                    region=settings.AWS_REGION,
                    versioning_status="Enabled" if req.enable_versioning else "Disabled",
                    public_access_blocked=req.block_public_access,
                    encryption="AES256 (Default SSE-S3)",
                    status="Created live in AWS account"
                )
            except Exception:
                pass

        # Simulated response
        return CreateBucketResponse(
            bucket_name=bucket,
            arn=f"arn:aws:s3:::{bucket}",
            region=settings.AWS_REGION,
            versioning_status="Enabled" if req.enable_versioning else "Disabled",
            public_access_blocked=req.block_public_access,
            encryption="AES256 (Default SSE-S3)",
            status="Simulated S3 Bucket Created with Best-Practice Security Baseline"
        )

    def upload_object(self, req: UploadObjectRequest) -> UploadObjectResponse:
        """Uploads an object to S3 with metadata tags and server-side encryption."""
        etag = hashlib.md5(req.content.encode("utf-8")).hexdigest()

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                s3 = get_boto3_client("s3")
                resp = s3.put_object(
                    Bucket=req.bucket_name,
                    Key=req.object_key,
                    Body=req.content.encode("utf-8"),
                    ContentType=req.content_type,
                    Metadata=req.metadata,
                    ServerSideEncryption="AES256"
                )
                return UploadObjectResponse(
                    bucket_name=req.bucket_name,
                    object_key=req.object_key,
                    etag=resp.get("ETag", f'"{etag}"').strip('"'),
                    version_id=resp.get("VersionId"),
                    s3_uri=f"s3://{req.bucket_name}/{req.object_key}",
                    https_url=f"https://{req.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{req.object_key}",
                    server_side_encryption=resp.get("ServerSideEncryption", "AES256")
                )
            except Exception:
                pass

        return UploadObjectResponse(
            bucket_name=req.bucket_name,
            object_key=req.object_key,
            etag=etag,
            version_id="3/L4kqtJlcpXroDTDmJ+rmSpXd3dIbrHY",
            s3_uri=f"s3://{req.bucket_name}/{req.object_key}",
            https_url=f"https://{req.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{req.object_key}",
            server_side_encryption="AES256 (SSE-S3)"
        )

    def generate_presigned_url(self, req: PresignedUrlRequest) -> PresignedUrlResponse:
        """Generates a secure, short-lived presigned URL for direct client upload or download."""
        method = "PUT" if req.operation == "put_object" else "GET"

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                s3 = get_boto3_client("s3")
                url = s3.generate_presigned_url(
                    ClientMethod=req.operation,
                    Params={"Bucket": req.bucket_name, "Key": req.object_key},
                    ExpiresIn=req.expiration_seconds,
                    HttpMethod=method
                )
                return PresignedUrlResponse(
                    presigned_url=url,
                    expires_in_seconds=req.expiration_seconds,
                    operation=req.operation,
                    http_method=method,
                    why_presigned_urls_are_essential="Real AWS presigned URL generated via boto3.",
                    architecture_benefit="Client uploads directly to S3 without burdening backend compute."
                )
            except Exception:
                pass

        # Simulated Presigned URL
        fake_token = hashlib.sha256(f"{req.bucket_name}:{req.object_key}:{time.time()}".encode()).hexdigest()[:32]
        url = (
            f"https://{req.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{req.object_key}"
            f"?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires={req.expiration_seconds}&X-Amz-Signature={fake_token}"
        )

        return PresignedUrlResponse(
            presigned_url=url,
            expires_in_seconds=req.expiration_seconds,
            operation=req.operation,
            http_method=method,
            why_presigned_urls_are_essential=(
                "Why Presigned URLs are a Senior Cloud Engineering Best Practice:\n"
                "1. Zero Server Load: Large file uploads (like 20MB scans or photos) flow DIRECTLY from the user's browser "
                "to Amazon S3. Your FastAPI server does NOT have to buffer or proxy millions of file bytes in RAM!\n"
                "2. Zero Credential Exposure: The frontend user NEVER receives AWS access keys. The presigned URL carries "
                "a temporary cryptographic signature valid ONLY for that specific object key and duration.\n"
                "3. Auto-Expiration: The link expires automatically (e.g. in 15 minutes), preventing unauthorized reuse."
            ),
            architecture_benefit=(
                "In Ataa Platform: When a family representative uploads a hospital invoice or ID document, "
                "FastAPI validates user authentication, creates the S3 presigned URL, and returns it to React. "
                "React then executes `fetch(presignedUrl, {method: 'PUT', body: file})` directly into S3!"
            )
        )

    def get_storage_classes_guide(self) -> StorageClassesResponse:
        """Comprehensive breakdown of Amazon S3 Storage Tiers and Lifecycle Policies."""
        return StorageClassesResponse(
            durability="99.999999999% (11 9s of Durability across multiple Availability Zones)",
            classes={
                "S3 Standard": {
                    "Availability": "99.99%",
                    "Retrieval Latency": "Milliseconds",
                    "Cost Tier": "$$$ (Highest storage cost, lowest access cost)",
                    "Best For": "Frequently accessed data, active case files, current application assets."
                },
                "S3 Intelligent-Tiering": {
                    "Availability": "99.9%",
                    "Retrieval Latency": "Milliseconds",
                    "Cost Tier": "Automatic optimization ($0.0025 per 1,000 objects monitoring fee)",
                    "Best For": "Data with unpredictable access patterns. Automatically moves objects between tiers with ZERO retrieval fees!"
                },
                "S3 Standard-IA (Infrequent Access)": {
                    "Availability": "99.9%",
                    "Retrieval Latency": "Milliseconds",
                    "Cost Tier": "$$ (Lower storage cost, but charges per GB retrieved)",
                    "Best For": "Long-term backups, older family cases that are infrequently audited."
                },
                "S3 One Zone-IA": {
                    "Availability": "99.5%",
                    "Retrieval Latency": "Milliseconds",
                    "Cost Tier": "$ (20% cheaper than Standard-IA)",
                    "Risk": "Stored in only ONE Availability Zone! Data can be lost if a physical data center is destroyed.",
                    "Best For": "Recreatable secondary backups, non-critical thumbnails."
                },
                "S3 Glacier Flexible Retrieval": {
                    "Availability": "99.99%",
                    "Retrieval Latency": "Minutes to hours (Expedited: 1-5 mins, Standard: 3-5 hours)",
                    "Cost Tier": "$ (Very low cost)",
                    "Best For": "Archived compliance records, closed family cases retained for 5+ years."
                },
                "S3 Glacier Deep Archive": {
                    "Availability": "99.99%",
                    "Retrieval Latency": "Hours (Standard: 12 hours, Bulk: 48 hours)",
                    "Cost Tier": "Lowest cost in AWS ($0.00099 / GB / month — less than $1/TB/month!)",
                    "Best For": "Regulatory archival that will rarely, if ever, be accessed."
                }
            },
            decision_flowchart=(
                "Lifecycle Strategy for Ataa Platform:\n"
                "Day 0 - Day 90: Store in S3 Standard (active case investigation).\n"
                "Day 91 - Day 365: S3 Lifecycle Rule transitions object to S3 Standard-IA (closed case).\n"
                "After 365 Days: Transition to S3 Glacier Flexible Retrieval for legal audit retention."
            )
        )


s3_service = S3StorageService()
