from pydantic import BaseModel, Field


class ParameterGetRequest(BaseModel):
    parameter_path: str = Field(default="/myapp/production/database/url")
    with_decryption: bool = Field(default=True)


class SecretGetRequest(BaseModel):
    secret_id: str = Field(default="myapp/production/jwt-secret")
