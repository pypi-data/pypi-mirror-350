from typing import Optional, Set, ClassVar
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date

class UserProfileUpdate(BaseModel):
    """
    User Profile Update model for partial updates of user information.
    All fields are optional to support partial updates.
    """
    model_config = ConfigDict(extra="forbid")

    # Metadata as class variables
    VERSION: ClassVar[float] = 2.01
    CLASS_ORIGIN_AUTHOR: ClassVar[str] = "Russlan Ramdowar;russlan@ftredge.com"
 

    # System fields
    email: Optional[EmailStr] = Field(None, description="Propagated from Firebase Auth")
    organizations_uids: Optional[Set[str]] = Field(None, description="Organization memberships")
    
    # System identification
    aliases: Optional[Set[str]] = None
    provider_id: Optional[str] = None

    # User-editable fields
    username: Optional[str] = Field(None, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    dob: Optional[date] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    mobile: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")

    # Remove audit fields

    def model_dump(self, **kwargs):
        kwargs.setdefault('exclude_none', True)
        return super().model_dump(**kwargs)



