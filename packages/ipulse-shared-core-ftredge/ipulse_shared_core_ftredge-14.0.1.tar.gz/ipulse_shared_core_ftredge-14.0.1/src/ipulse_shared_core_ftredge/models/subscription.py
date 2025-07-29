from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import uuid
from typing import Set, Optional, ClassVar, Dict, Any, List, Union
from pydantic import Field, ConfigDict
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Subject, SubscriptionPlan, SubscriptionStatus
from ipulse_shared_base_ftredge.enums.enums_iam import IAMUnitType
from .base_data_model import BaseDataModel
# ORIGINAL AUTHOR ="russlan.ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE=datetime(2024, 2, 12, 20, 5)


DEFAULT_SUBSCRIPTION_PLAN = SubscriptionPlan.FREE
DEFAULT_SUBSCRIPTION_STATUS = SubscriptionStatus.ACTIVE

############################################ !!!!! ALWAYS UPDATE SCHEMA VERSION , IF SCHEMA IS BEING MODIFIED !!! ############################################
class Subscription(BaseDataModel):
    """
    Represents a single subscription cycle with enhanced flexibility and tracking.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    VERSION: ClassVar[float] = 3.0  # Incremented version for direct fields instead of computed
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Subject.SUBSCRIPTION.name))
    OBJ_REF: ClassVar[str] = "subscription"

    # System-managed fields (read-only)
    schema_version: float = Field(
        default=VERSION,
        description="Version of this Class == version of DB Schema",
        frozen=True
    )

    # Unique identifier for this specific subscription instance - now auto-generated
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this subscription instance"
    )

    # Plan identification
    plan_name: SubscriptionPlan = Field(
        ...,  # Required field, no default
        description="Subscription Plan Name"
    )

    plan_version: int = Field(
        ...,  # Required field, no default
        description="Version of the subscription plan"
    )

    # Direct field instead of computed
    plan_id: str = Field(
        ...,  # Required field, no default
        description="Combined plan identifier (plan_name_plan_version)"
    )

    # Cycle duration fields
    cycle_start_date: datetime = Field(
        ...,  # Required field, no default
        description="Subscription Cycle Start Date"
    )

    # Direct field instead of computed
    cycle_end_date: datetime = Field(
        ...,  # Required field, no default
        description="Subscription Cycle End Date"
    )

    # Fields for cycle calculation
    validity_time_length: int = Field(
        ...,  # Required field, no default
        description="Length of subscription validity period (e.g., 1, 3, 12)"
    )

    validity_time_unit: str = Field(
        ...,  # Required field, no default
        description="Unit of subscription validity ('minute', 'hour', 'day', 'week', 'month', 'year')"
    )

    # Renewal and status fields
    auto_renew: bool = Field(
        ...,  # Required field, no default
        description="Auto-renewal status"
    )

    status: SubscriptionStatus = Field(
        ...,  # Required field, no default
        description="Subscription Status (active, trial, pending_confirmation, etc.)"
    )

    # IAM permissions structure
    default_iam_domain_permissions: Dict[str, Dict[str, List[str]]] = Field(
        ...,  # Required field, no default
        description="IAM domain permissions granted by this subscription (domain -> IAM unit type -> list of unit references)"
    )

    fallback_plan_id: Optional[str] = Field(
        ...,  # Required field (can be None), no default
        description="ID of the plan to fall back to if this subscription expires"
    )

    price_paid_usd: float = Field(
        ...,  # Required field, no default
        description="Amount paid for this subscription in USD"
    )

    payment_ref: Optional[str] = Field(
        default=None,
        description="Reference to payment transaction"
    )

    # Credit management fields
    subscription_based_insight_credits_per_update: int = Field(
        default=0,
        description="Number of insight credits to add on each update"
    )

    subscription_based_insight_credits_update_freq_h: int = Field(
        default=24,
        description="Frequency of insight credits update in hours"
    )

    extra_insight_credits_per_cycle: int = Field(
        default=0,
        description="Additional insight credits granted per subscription cycle"
    )

    voting_credits_per_update: int = Field(
        default=0,
        description="Number of voting credits to add on each update"
    )

    voting_credits_update_freq_h: int = Field(
        default=62,
        description="Frequency of voting credits update in hours"
    )

    # General metadata for extensibility
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the subscription"
    )

    # Helper method to calculate cycle end date
    @classmethod
    def calculate_cycle_end_date(cls, start_date: datetime, validity_length: int, validity_unit: str) -> datetime:
        """Calculate the end date based on start date and validity period."""
        if validity_unit == "minute":
            return start_date + relativedelta(minutes=validity_length)
        elif validity_unit == "hour":
            return start_date + relativedelta(hours=validity_length)
        elif validity_unit == "day":
            return start_date + relativedelta(days=validity_length)
        elif validity_unit == "week":
            return start_date + relativedelta(weeks=validity_length)
        elif validity_unit == "year":
            return start_date + relativedelta(years=validity_length)
        else:  # Default to months
            return start_date + relativedelta(months=validity_length)

    # Methods for subscription management
    def is_active(self) -> bool:
        """Check if the subscription is currently active."""
        now = datetime.now(timezone.utc)
        return (
            self.status == SubscriptionStatus.ACTIVE and
            self.cycle_start_date <= now <= self.cycle_end_date
        )

    def is_expired(self) -> bool:
        """Check if the subscription has expired."""
        now = datetime.now(timezone.utc)
        return now > self.cycle_end_date

    def days_remaining(self) -> int:
        """Calculate the number of days remaining in the subscription."""
        now = datetime.now(timezone.utc)
        if now > self.cycle_end_date:
            return 0

        # Get time difference
        time_diff = self.cycle_end_date - now

        # If there's any time remaining but less than a day, return 1
        if time_diff.days == 0 and time_diff.seconds > 0:
            return 1

        # Otherwise return the number of complete days
        return time_diff.days