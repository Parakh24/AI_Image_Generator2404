"""Decode and validate JWT access tokens for the authentication layer.

The main helper in this module verifies a token with the configured secret and
algorithm, checks that the required user and tenant identifiers are present,
and converts the decoded values into a validated ``TokenPayload`` object.
Invalid and expired tokens are translated into HTTP 401 errors that FastAPI can
return to the client.
"""

import jwt
from fastapi import HTTPException, status
from app.authentication.config import auth_settings
from app.authentication.schemas import TokenPayload

def decode_access_token(token: str) -> TokenPayload:
    """Validate an encoded access token and return its identity information.

    Args:
        token: Encoded JWT normally received from the request's bearer-token
            ``Authorization`` header.

    Returns:
        A validated payload containing the user's ID and tenant ID.

    Raises:
        HTTPException: Returns HTTP 401 when the token has expired, cannot be
        verified, or does not contain both a user ID and a tenant ID.
    """
    try:
        payload_dict = jwt.decode(
            token, 
            auth_settings.SECRET_KEY, 
            algorithms=[auth_settings.ALGORITHM]
        )
        
        user_id = payload_dict.get("sub") or payload_dict.get("user_id")
        tenant_id = payload_dict.get("tenant_id")

        if not user_id or not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing user_id or tenant_id claims"
            )

        return TokenPayload(
            user_id=str(user_id),
            tenant_id=str(tenant_id)
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
