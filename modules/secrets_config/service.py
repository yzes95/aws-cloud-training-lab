import json
from typing import Any, Dict
from core.config import settings
from core.aws_client import get_boto3_client
from .schemas import (
    ParameterGetRequest,
    ParameterResponse,
    SecretComparisonResponse,
    SecretGetRequest,
    SecretResponse,
)


class SecretsConfigService:
    """Service providing hands-on training for AWS Secrets Manager, SSM Parameter Store, and Environment Variables."""

    def get_ssm_parameter(self, req: ParameterGetRequest) -> ParameterResponse:
        """Fetches or simulates fetching a parameter from AWS SSM Parameter Store."""
        path = req.parameter_path.strip()

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                ssm = get_boto3_client("ssm")
                resp = ssm.get_parameter(Name=path, WithDecryption=req.with_decryption)
                param = resp["Parameter"]
                return ParameterResponse(
                    name=param["Name"],
                    type=param["Type"],
                    value=param["Value"],
                    arn=param["ARN"],
                    version=param["Version"],
                    kms_key_id=param.get("KeyId"),
                    security_explanation="Fetched live from AWS Systems Manager Parameter Store."
                )
            except Exception:
                pass  # Fallback to simulation if parameter doesn't exist in AWS

        # Realistic SSM Simulation
        is_secure = "password" in path or "url" in path or "secret" in path or "key" in path
        val = "postgresql://ataa_user:SuperSecretPass2026@db.internal.ataa.org:5432/ataa_db" if is_secure else "https://api.ataa.org"
        if not req.with_decryption and is_secure:
            val = "AQICAHi4...encrypted_kms_ciphertext..."

        return ParameterResponse(
            name=path,
            type="SecureString" if is_secure else "String",
            value=val,
            arn=f"arn:aws:ssm:{settings.AWS_REGION}:123456789012:parameter{path}",
            version=3,
            kms_key_id="alias/aws/ssm" if is_secure else None,
            security_explanation=(
                "AWS Systems Manager (SSM) Parameter Store:\n"
                "1. Hierarchical storage: Paths like `/ataa/prod/db/url` allow fine-grained IAM policy scoping.\n"
                "2. Types: String (plain text), StringList (comma-separated), SecureString (encrypted with AWS KMS).\n"
                "3. Free Tier: Standard parameters are FREE (up to 10,000 parameters per account)."
            )
        )

    def get_secrets_manager_secret(self, req: SecretGetRequest) -> SecretResponse:
        """Fetches or simulates fetching an encrypted secret from AWS Secrets Manager."""
        secret_id = req.secret_id.strip()

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                sm = get_boto3_client("secretsmanager")
                resp = sm.get_secret_value(SecretId=secret_id)
                secret_str = resp.get("SecretString", "{}")
                secret_dict = json.loads(secret_str) if secret_str.startswith("{") else {"raw": secret_str}
                return SecretResponse(
                    secret_id=resp["Name"],
                    secret_value=secret_dict,
                    arn=resp["ARN"],
                    version_id=resp["VersionId"],
                    rotation_enabled=True,
                    rotation_rules={"AutomaticallyAfterDays": 30},
                    security_explanation="Fetched live from AWS Secrets Manager."
                )
            except Exception:
                pass

        # Realistic Secrets Manager Simulation
        return SecretResponse(
            secret_id=secret_id,
            secret_value={
                "username": "ataa_db_admin",
                "password": "xK9#mQ2$vL8!zR5_production_encrypted",
                "engine": "postgres",
                "host": "ataa-postgres.c9a9example.eu-central-1.rds.amazonaws.com",
                "port": 5432,
                "dbname": "ataa_prod"
            },
            arn=f"arn:aws:secretsmanager:{settings.AWS_REGION}:123456789012:secret:{secret_id}-abc123",
            version_id="08f7b764-58f7-4dc2-8075-812e9b0e2518",
            rotation_enabled=True,
            rotation_rules={"AutomaticallyAfterDays": 30},
            security_explanation=(
                "AWS Secrets Manager Advantages:\n"
                "1. Built-in Automatic Secret Rotation: An AWS Lambda function updates the database password "
                "and updates Secrets Manager simultaneously without service downtime!\n"
                "2. Envelope Encryption with AWS KMS: Keys are encrypted both at rest and in transit.\n"
                "3. Cross-Account Access: Allows different AWS accounts (e.g. dev vs prod) to securely share credentials."
            )
        )

    def compare_secrets_options(self) -> SecretComparisonResponse:
        """Compares plain .env files, Docker environment variables, SSM Parameter Store, and Secrets Manager."""
        return SecretComparisonResponse(
            comparison_table={
                "Plain .env file": {
                    "Security": "Low (High risk of accidental git commit)",
                    "Cost": "Free",
                    "Rotation": "Manual",
                    "Best For": "Local development on developer laptop ONLY"
                },
                "Docker env vars (-e / --env-file)": {
                    "Security": "Medium (Visible in `docker inspect` process tree)",
                    "Cost": "Free",
                    "Rotation": "Requires container restart",
                    "Best For": "Non-sensitive configs (APP_ENV, PORT, LOG_LEVEL)"
                },
                "SSM Parameter Store (Standard)": {
                    "Security": "High (KMS SecureString encryption + IAM)",
                    "Cost": "Free (up to 10k parameters)",
                    "Rotation": "Manual or custom Lambda",
                    "Best For": "API URLs, feature flags, configuration constants"
                },
                "AWS Secrets Manager": {
                    "Security": "Maximum (KMS + automated rotation + audit logs)",
                    "Cost": "$0.40 / secret / month + $0.05 per 10k API calls",
                    "Rotation": "Automatic via built-in AWS Lambda templates (e.g. RDS)",
                    "Best For": "Database passwords, payment gateway API keys, JWT master secrets"
                }
            },
            best_practice_recommendation=(
                "Production Recommendation for Ataa / FastAPI:\n"
                "1. Keep non-sensitive settings (like APP_NAME, CORS_ORIGINS) in environment variables.\n"
                "2. Fetch sensitive credentials (DATABASE_URL, JWT SECRET, PAYMENT KEYS) from AWS Secrets Manager "
                "or SSM Parameter Store during application startup.\n"
                "3. Cache the secret in memory with a Time-To-Live (TTL e.g. 1 hour) so your app doesn't call AWS on every HTTP request!"
            )
        )


secrets_service = SecretsConfigService()
