# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# pylint: disable=no-self-argument  # Added for Pydantic validators
from datetime import datetime
from typing import Set, Optional, ClassVar
from pydantic import BaseModel, field_validator, Field, ConfigDict
import uuid
import dateutil.parser
from ipulse_shared_base_ftredge import (
    OrganizationRelation,
    OrganizationIndustry,
    Layer,
    Module,
    list_as_lower_strings,
    Subject
)
from .base_data_model import BaseDataModel

class OrganizationProfile(BaseDataModel):
    """
    Organisation model representing business entities in the system.
    Supports both retail and non-retail customer types with different validation rules.
    """
    model_config = ConfigDict(frozen=False, extra="forbid")  # Changed frozen to False to allow id assignment

    # Class constants
    VERSION: ClassVar[float] = 4.1
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Subject.ORGANIZATION.name))
    OBJ_REF: ClassVar[str] = "orgprofile"

    schema_version: float = Field(
        default=VERSION,
        description="Version of this Class == version of DB Schema",
        frozen=True
    )

    org_uid: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        description="Unique identifier for the organisation",
        frozen=True
    )

    id: str = Field(
        ...,  # Make it required
        description="Organisation ID, format: {OBJ_REF}_{org_uid}"
    )

    name: str = Field(..., min_length=1, max_length=100)
    relations: Set[OrganizationRelation] = Field(..., description="Organisation relations/types")

    description: Optional[str] = Field(None, max_length=1000)
    industries: Optional[Set[OrganizationIndustry]] = None
    website: Optional[str] = Field(None, max_length=200)
    org_admin_user_uids: Optional[Set[str]] = None

    @field_validator('id', mode='before')
    @classmethod
    def generate_id(cls, v: Optional[str], info) -> str:
        values = info.data
        org_uid = values.get('org_uid')
        if not org_uid:
            raise ValueError("org_uid must be set before generating id")
        return f"{cls.OBJ_REF}_{org_uid}"

    @field_validator('relations')
    @classmethod
    def validate_relations(cls, v: Set[OrganizationRelation]) -> Set[OrganizationRelation]:
        return v

    @field_validator('industries')
    @classmethod
    def validate_industries(cls, v: Optional[Set[OrganizationIndustry]], info) -> Optional[Set[OrganizationIndustry]]:
        values = info.data
        is_retail = values.get('relations') == {OrganizationRelation.RETAIL_CUSTOMER}
        if is_retail and v is not None:
            raise ValueError("Industries should not be set for retail customers")
        elif not is_retail and v is None:
            raise ValueError("Industries required for non-retail customers")
        return v

    @field_validator('website', 'description')
    @classmethod
    def validate_retail_fields(cls, v: Optional[str], info) -> Optional[str]:
        values = info.data
        field = info.field_name
        is_retail = values.get('relations') == {OrganizationRelation.RETAIL_CUSTOMER}
        if is_retail and v is not None:
            raise ValueError(f"{field} should not be set for retail customers")
        elif not is_retail and not v:
            raise ValueError(f"{field} required for non-retail customers")
        return v