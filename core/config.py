import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel

    class BaseSettings(BaseModel):  # type: ignore
        def __init__(self, **data):
            super().__init__(**data)
            for field_name in self.__class__.model_fields.keys():
                if field_name in os.environ:
                    env_val = os.environ[field_name]
                    current_val = getattr(self, field_name)
                    if isinstance(current_val, bool):
                        setattr(self, field_name, env_val.lower() in ("true", "1", "yes", "t"))
                    else:
                        setattr(self, field_name, env_val)

    SettingsConfigDict = dict  # type: ignore


class Settings(BaseSettings):
    APP_NAME: str = "AWS Cloud Training Lab"
    APP_ENV: str = "development"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # AWS Configuration
    # Boto3 resolves credentials via the standard AWS credential chain:
    # 1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    # 2. Shared credentials file (~/.aws/credentials)
    # 3. AWS IAM Role (Instance Profile on EC2, Task Role on ECS)
    AWS_REGION: str = "us-east-1"

    # Optional LocalStack endpoint (e.g., "http://localhost:4566")
    # Leave empty or unset to target real AWS
    LOCALSTACK_ENDPOINT_URL: Optional[str] = None

    # Target resource names for lab exercises
    TRAINING_S3_BUCKET: str = "aws-training-lab-bucket"
    CLOUDWATCH_LOG_GROUP: str = "/aws/training-lab/fastapi"


settings = Settings()
