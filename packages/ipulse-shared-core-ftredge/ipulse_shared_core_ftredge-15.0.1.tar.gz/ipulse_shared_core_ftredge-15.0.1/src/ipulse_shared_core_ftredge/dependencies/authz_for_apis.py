import os
import logging
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Iterable, Dict, Any, List
from datetime import datetime, timedelta, timezone
import json
import httpx
from fastapi import HTTPException, Request
from google.cloud import firestore
from ipulse_shared_core_ftredge.services import ServiceError, AuthorizationError, ResourceNotFoundError
from ipulse_shared_core_ftredge.models import UserStatus
from ipulse_shared_core_ftredge.utils.json_encoder import convert_to_json_serializable

# Constants derived from UserStatus model
USERS_STATUS_COLLECTION_NAME = UserStatus.COLLECTION_NAME
USERS_STATUS_DOC_REF = f"{UserStatus.OBJ_REF}_" # Use OBJ_REF and append underscore
USERSTATUS_CACHE_TTL = 60 # 60 seconds

class UserStatusCache:
    """Manages user status caching with dynamic invalidation"""
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._timestamps: Dict[str, datetime] = {}

    def get(self, user_uid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves user status from cache if available and valid.

        Args:
            user_uid (str): The user ID.

        """
        if user_uid in self._cache:
            status_data = self._cache[user_uid]
            # Force refresh for credit-consuming or sensitive operations
            # Check TTL for normal operations
            if datetime.now() - self._timestamps[user_uid] < timedelta(seconds=USERSTATUS_CACHE_TTL):
                return status_data
            self.invalidate(user_uid)
        return None

    def set(self, user_uid: str, data: Dict[str, Any]) -> None:
        """
        Sets user status data in the cache.

        Args:
            user_uid (str): The user ID.
            data (Dict[str, Any]): The user status data to cache.
        """
        self._cache[user_uid] = data
        self._timestamps[user_uid] = datetime.now()

    def invalidate(self, user_uid: str) -> None:
        """
        Invalidates (removes) user status from the cache.

        Args:
            user_uid (str): The user ID to invalidate.
        """
        self._cache.pop(user_uid, None)
        self._timestamps.pop(user_uid, None)

# Global cache instance
userstatus_cache = UserStatusCache()

# Replace the logger dependency with a standard logger
logger = logging.getLogger(__name__)

# Create a custom FirestoreTimeoutError class that can be identified in middlewares
class FirestoreTimeoutError(TimeoutError):
    """Custom exception for Firestore timeout errors to make them more identifiable."""
    pass


# Define a function to get a Firestore document with a strict timeout
async def get_with_strict_timeout(doc_ref, timeout_seconds: float):
    """
    Get a Firestore document with a strictly enforced timeout.

    Args:
        doc_ref: Firestore document reference
        timeout_seconds: Maximum time to wait in seconds

    Returns:
        Document snapshot

    Raises:
        FirestoreTimeoutError: If the operation takes longer than timeout_seconds
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        try:
            # Run the blocking Firestore get() operation in a thread and apply a strict timeout
            logger.debug(f"Starting Firestore get with strict timeout of {timeout_seconds}s")
            return await asyncio.wait_for(
                loop.run_in_executor(executor, doc_ref.get),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            error_message = f"User Status fetching for Authz timed out after {timeout_seconds} seconds, perhaps issue with Firestore Connectivity"
            logger.error(error_message)
            raise FirestoreTimeoutError(error_message)

# Update get_userstatus to use our new strict timeout function
async def get_userstatus(
    user_uid: str,
    db: firestore.Client,
    force_fresh: bool = False,
    timeout: float = 12.0  # Default timeout but allow override
) -> tuple[Dict[str, Any], bool]:
    """
    Fetch user status with intelligent caching and configurable timeout

    Args:
        user_uid: User ID to fetch status for
        db: Firestore client
        force_fresh: Whether to bypass cache
        timeout: Timeout for Firestore operations in seconds

    Returns:
        Tuple of (user status data, whether cache was used)
    """
    cache_used = False
    if not force_fresh:
        cached_status = userstatus_cache.get(user_uid)
        if cached_status:
            cache_used = True
            return cached_status, cache_used

    try:
        # Get reference to the document
        userstatus_id = USERS_STATUS_DOC_REF + user_uid
        user_ref = db.collection(USERS_STATUS_COLLECTION_NAME).document(userstatus_id)

        logger.debug(f"Fetching user status for {user_uid} with strict timeout {timeout}s")

        # Use our strict timeout wrapper instead of the native timeout parameter
        snapshot = await get_with_strict_timeout(user_ref, timeout)

        if not snapshot.exists:
            raise ResourceNotFoundError(
                resource_type="authorization userstatus",
                resource_id=userstatus_id,
                additional_info={"user_uid": user_uid}
            )

        status_data = snapshot.to_dict()

        # Only cache if not forced fresh
        if not force_fresh:
            userstatus_cache.set(user_uid, status_data)
        return status_data, cache_used

    except TimeoutError as e:
        logger.error(f"Timeout while fetching user status for {user_uid}: {str(e)}")
        raise ServiceError(
            operation="fetching user status for authz",
            error=e,
            resource_type="userstatus",
            resource_id=user_uid,
            additional_info={
                "force_fresh": force_fresh,
                "collection": USERS_STATUS_COLLECTION_NAME,
                "timeout_seconds": timeout
            }
        )
    except ResourceNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error fetching user status for {user_uid}: {str(e)}")
        raise ServiceError(
            operation=f"fetching user status",
            error=e,
            resource_type="userstatus",
            resource_id=user_uid,
            additional_info={
                "force_fresh": force_fresh,
                "collection": USERS_STATUS_COLLECTION_NAME
            }
        ) from e

def _validate_resource_fields(fields: Dict[str, Any]) -> List[str]:
    """
    Filter out invalid fields similar to BaseFirestoreService validation.
    Returns only fields that have actual values to update.
    """
    valid_fields = {
        k: v for k, v in fields.items()
        if v is not None and not (isinstance(v, (list, dict, set)) and len(v) == 0)
    }
    return list(valid_fields.keys())

async def extract_request_fields(request: Request) -> Optional[List[str]]:
    """
    Extract fields from request body for both PATCH and POST methods.
    For GET and DELETE methods, return None as they typically don't have a body.
    """
    # Skip body extraction for GET and DELETE requests
    if request.method.upper() in ["GET", "DELETE", "HEAD", "OPTIONS"]:
        return None

    try:
        body = await request.json()
        if isinstance(body, dict):
            if request.method.upper() == "PATCH":
                return _validate_resource_fields(body)
            if request.method.upper() == "POST":
                # For POST, we want to include all fields being set
                return list(body.keys())
        elif hasattr(body, 'model_dump'):
            data = body.model_dump(exclude_unset=True)
            if request.method.upper() == "PATCH":
                return _validate_resource_fields(data)
            if request.method.upper() == "POST":
                return list(data.keys())

        return None

    except Exception as e:
        logger.warning(f"Could not extract fields from request body: {str(e)}")
        return None  # Return None instead of raising an error

# Main authorization function with configurable timeout
async def authorizeAPIRequest(
    request: Request,
    db: firestore.Client,
    request_resource_fields: Optional[Iterable[str]] = None,
    firestore_timeout: float = 15.0  # Allow specifying timeout
) -> Dict[str, Any]:
    """
    Authorize API request based on user status and OPA policies.
    Enhanced with credit check information and proper exception handling.

    Args:
        request: The incoming request
        db: Firestore client
        request_resource_fields: Fields being accessed/modified in the request
        firestore_timeout: Timeout for Firestore operations in seconds

    Returns:
        Authorization result containing decision details

    Raises:
        HTTPException: For authorization failures (403) or service errors (500)
    """
    opa_decision = None
    try:
        # Extract fields for both PATCH and POST if not provided
        if not request_resource_fields:
            request_resource_fields = await extract_request_fields(request)

        # Extract request context
        user_uid = request.state.user.get('uid')
        if not user_uid:
            # Log authorization failures at DEBUG level, not ERROR
            logger.debug(f"Authorization denied for {request.method} {request.url.path}: No user UID found")
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this resource"
            )

        # Determine if we need fresh status
        force_fresh = _should_force_fresh_status(request)
        userstatus, cache_used = await get_userstatus(
            user_uid,
            db,
            force_fresh=force_fresh,
            timeout=firestore_timeout  # Pass the specified timeout
        )

        # Prepare authorization input that matches OPA expectations
        # Extract required values from user status
        primary_usertype = userstatus.get("primary_usertype")
        secondary_usertypes = userstatus.get("secondary_usertypes", [])

        # Extract IAM domain permissions
        iam_domain_permissions = userstatus.get("iam_domain_permissions", {})

        # Format the authz_input to match what the OPA policies expect
        authz_input = {
            "api_url": request.url.path,
            "requestor": {
                "uid": user_uid,
                "primary_usertype": primary_usertype,
                "secondary_usertypes": secondary_usertypes,
                "usertypes": [primary_usertype] + secondary_usertypes if primary_usertype else secondary_usertypes,
                "email_verified": request.state.user.get("email_verified", False),
                "iam_domain_permissions": iam_domain_permissions,
                "sbscrptn_based_insight_credits": userstatus.get("sbscrptn_based_insight_credits", 0),
                "extra_insight_credits": userstatus.get("extra_insight_credits", 0)
            },
            "method": request.method.lower(),
            "request_resource_fields": request_resource_fields
        }

        # Convert any non-serializable objects to JSON serializable format
        # Using the unified utility from utils
        json_safe_authz_input = convert_to_json_serializable(authz_input)

        # Query OPA
        opa_url = f"{os.getenv('OPA_SERVER_URL', 'http://localhost:8181')}{os.getenv('OPA_DECISION_PATH', '/v1/data/http/authz/ingress/decision')}"
        logger.debug(f"Attempting to connect to OPA at: {opa_url}")

        # Debug: Print raw JSON payload to identify any potential issues
        try:
            payload_json = json.dumps({"input": json_safe_authz_input})
            logger.debug(f"OPA Request JSON payload: {payload_json}")
        except Exception as json_err:
            logger.error(f"Error serializing OPA request payload: {json_err}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    opa_url,
                    json={"input": json_safe_authz_input},
                    timeout=5.0  # 5 seconds timeout
                )
                logger.debug(f"OPA Response Status: {response.status_code}")
                # logger.debug(f"OPA Response Body: {response.text}")

                if response.status_code != 200:
                    logger.error(f"OPA authorization failed: {response.text}")
                    raise HTTPException(
                        status_code=500,
                        detail="Authorization service error"
                    )

                result = response.json()
                logger.debug(f"Parsed OPA response: {result}")

                # Handle unusual OPA response formats
                if "result" in result:
                    opa_decision = result["result"]
                else:
                    logger.warning(f"OPA response missing 'result' field, using default")
                    raise HTTPException(
                        status_code=500,
                        detail="Authorization service error: OPA response format unexpected"
                    )

                # Extract key fields from result with better default handling
                allow = opa_decision.get("allow", False)

                # Handle authorization denial - log at DEBUG level, not ERROR
                if not allow:
                    logger.debug(f"Authorization denied for {request.method} {request.url.path}: insufficient permissions")
                    raise HTTPException(
                        status_code=403,
                        detail=f"Not authorized to {request.method} {request.url.path}"
                    )

            except httpx.RequestError as e:
                # Only log actual system errors at ERROR level
                logger.error(f"Failed to connect to OPA: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="Authorization service temporarily unavailable"
                )

        # More descriptive metadata about the data freshness
        return {
            "used_cached_status": cache_used,
            "required_fresh_status": force_fresh,
            "status_retrieved_at": datetime.now(timezone.utc).isoformat(),
            "opa_decision": opa_decision
        }

    except HTTPException:
        # Re-raise HTTPExceptions as-is (they're already properly formatted)
        raise
    except Exception as e:
        # Only log unexpected errors at ERROR level
        logger.error(f"Unexpected error during authorization for {request.method} {request.url.path}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal authorization error"
        )

def _should_force_fresh_status(request: Request) -> bool:
    """
    Determine if we should force a fresh status check based on the request path patterns
    and HTTP methods
    """
    # Path patterns that indicate credit-sensitive operations
    credit_sensitive_patterns = [
        'prediction',
        'user-statuses',
        'historic'
    ]
    # Methods that require fresh status
    sensitive_methods = {'post', 'patch', 'put', 'delete'}

    path = request.url.path.lower()
    method = request.method.lower()

    return (
        any(pattern in path for pattern in credit_sensitive_patterns) or
        method in sensitive_methods
    )
