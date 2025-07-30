from typing import Optional, Annotated
from fastapi import Request, HTTPException, Depends, Header
from firebase_admin import auth

class AuthenticatedUser:
    """
    Represents an authenticated user with necessary attributes.
    """
    def __init__(self, uid: str, email: str, email_verified: bool, usertypes: list[str]):
        self.uid = uid
        self.email = email
        self.email_verified = email_verified
        self.usertypes = usertypes

async def verify_firebase_token(
    request: Request,
    x_forwarded_authorization: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
) -> AuthenticatedUser:
    """
    Represents an authenticated user with necessary attributes.
    """
    # Get token from either x-forwarded-authorization or authorization header
    token = x_forwarded_authorization or authorization

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is missing"
        )

    try:
        # Remove 'Bearer ' prefix if present
        token = token.replace("Bearer ", "")
        # Verify the token
        decoded_token = auth.verify_id_token(token)

        # Create AuthenticatedUser instance
        user = AuthenticatedUser(
            uid=decoded_token.get('uid'),
            email=decoded_token.get('email'),
            email_verified=decoded_token.get('email_verified', False),
            usertypes=decoded_token.get('usertypes', [])
        )

        # Store user in request state for use in other parts of the application
        request.state.user = decoded_token

        return user

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        ) from e

# Type alias for dependency injection
AuthUser = Annotated[AuthenticatedUser, Depends(verify_firebase_token)]

