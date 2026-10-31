import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    USE_PYDANTIC_SETTINGS = True
except ImportError:
    from pydantic import BaseModel
    USE_PYDANTIC_SETTINGS = False

    class BaseSettings(BaseModel):  # type: ignore
        def __init__(self, **data):
            super().__init__(**data)
            # Read from os.environ
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

    # AWS Environment & Emulation
    # When AWS_MOCK_MODE is True, requests are simulated locally with realistic AWS data
    # When False, requests call real AWS APIs (or LocalStack if LOCALSTACK_ENDPOINT_URL is set)
    AWS_MOCK_MODE: bool = True
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_SESSION_TOKEN: Optional[str] = None
    LOCALSTACK_ENDPOINT_URL: Optional[str] = None

    # Default Resources for Labs
    TRAINING_S3_BUCKET: str = "aws-training-lab-bucket"
    CLOUDWATCH_LOG_GROUP: str = "/aws/training-lab/fastapi"

    if USE_PYDANTIC_SETTINGS:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )


settings = Settings()
