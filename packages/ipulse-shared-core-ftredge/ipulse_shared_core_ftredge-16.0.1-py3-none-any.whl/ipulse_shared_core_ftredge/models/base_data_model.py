from datetime import datetime, timezone
from typing import Any
from typing import ClassVar
from pydantic import BaseModel, Field, ConfigDict, field_validator
import dateutil.parser

class BaseDataModel(BaseModel):
    """Base model with common fields and configuration"""
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Required class variables that must be defined in subclasses
    VERSION: ClassVar[float]
    DOMAIN: ClassVar[str]
    OBJ_REF: ClassVar[str]

    # Schema versioning
    schema_version: float = Field(
        ...,  # Make this required
        description="Version of this Class == version of DB Schema",
        frozen=True
    )

    # Audit fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), frozen=True)
    created_by: str = Field(..., frozen=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), frozen=True)
    updated_by: str = Field(...)

    @classmethod
    def get_collection_name(cls) -> str:
        """Generate standard collection name"""
        return f"{cls.DOMAIN}_{cls.OBJ_REF}s"

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def parse_datetime(cls, v: Any) -> datetime:
        if isinstance(v, datetime): # If Firestore already gave a datetime object
            return v # Just use it, no parsing needed
        if isinstance(v, str): # If it's a string (e.g. from an API request, not Firestore direct)
            try:
                return dateutil.parser.isoparse(v)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid datetime string format: {v} - {e}")
        # Firestore might send google.api_core.datetime_helpers.DatetimeWithNanoseconds
        # which is a subclass of datetime.datetime, so isinstance(v, datetime) should catch it.
        # If for some reason it's a different type not caught by isinstance(v, datetime)
        # but has isoformat(), perhaps try that, but it's unlikely with current Firestore client.
        # For example, if v is some custom timestamp object from an older library:
        if hasattr(v, 'isoformat'): # Fallback for unknown datetime-like objects
             try:
                 return dateutil.parser.isoparse(v.isoformat())
             except Exception as e:
                 raise ValueError(f"Could not parse datetime-like object: {v} - {e}")

        raise ValueError(f"Unsupported type for datetime parsing: {type(v)} value: {v}")
