"""AWS runtime integrations (STS, Secrets Manager / SSM, S3, CloudWatch).

Important AWS rule:
- Do NOT pass `aws_access_key_id` or `aws_secret_access_key` inside your code!
- Boto3 automatically uses:
  1. Your local AWS CLI profile (`aws configure`) when running on your laptop.
  2. The attached IAM Role (EC2 Instance Profile / ECS Task Role) via temporary STS
     credentials (IMDSv2) when running on AWS.
"""
import os
from typing import Any, Dict

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "my-training-s3-bucket")
CLOUDWATCH_LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/training-lab/app")


def get_aws_identity() -> Dict[str, Any]:
    """Calls AWS STS `get_caller_identity` to check which IAM User or Role the app is using.
    
    Used in GET /health to verify that the EC2 IAM Role is working without hardcoded keys.
    """
    # TODO 1: Create a boto3 'sts' client and return `sts.get_caller_identity()`
    # Example:
    # import boto3
    # sts = boto3.client("sts", region_name=AWS_REGION)
    # return sts.get_caller_identity()
    raise NotImplementedError("TODO: Implement get_aws_identity() using boto3 STS.")


def get_secret(secret_name: str) -> str:
    """Fetches a secret (like DATABASE_URL) from AWS Secrets Manager or SSM Parameter Store."""
    # TODO 2: Create a boto3 'secretsmanager' or 'ssm' client and fetch the secret value
    # Hint for Secrets Manager: client.get_secret_value(SecretId=secret_name)["SecretString"]
    # Hint for SSM: client.get_parameter(Name=secret_name, WithDecryption=True)["Parameter"]["Value"]
    raise NotImplementedError("TODO: Implement get_secret() using Secrets Manager or SSM.")


def upload_to_s3(file_bytes: bytes, object_key: str, content_type: str = "application/octet-stream") -> str:
    """Uploads a file to Amazon S3 and returns the S3 object key or presigned URL."""
    # TODO 3: Create a boto3 's3' client:
    # 1. Call `s3.put_object(Bucket=S3_BUCKET_NAME, Key=object_key, Body=file_bytes, ContentType=content_type)`
    # 2. (Optional) Generate a presigned GET URL so the user can view the private file:
    #    `s3.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME, 'Key': object_key}, ExpiresIn=900)`
    raise NotImplementedError("TODO: Implement upload_to_s3() using boto3 S3.")


def record_cloudwatch_metric(metric_name: str, value: float = 1.0) -> None:
    """Sends a custom metric (e.g., 'ItemsCreated') to Amazon CloudWatch."""
    # TODO 4: Create a boto3 'cloudwatch' client and call `put_metric_data`:
    # cw.put_metric_data(
    #     Namespace="TrainingApp",
    #     MetricData=[{"MetricName": metric_name, "Value": value, "Unit": "Count"}]
    # )
    raise NotImplementedError("TODO: Implement record_cloudwatch_metric() using boto3 CloudWatch.")
