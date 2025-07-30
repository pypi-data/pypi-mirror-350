from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserAuth(BaseModel):
    """Authentication model for user credentials"""
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")
    extra_fields: dict = Field(default_factory=dict, description="Additional authentication fields")