"""Provide the current user's identity to protected API routes.

FastAPI routes can declare ``get_current_user_id`` as a dependency when they
need to know which user sent a request. For now, the dependency reads the user
ID directly from the ``X-User-ID`` HTTP header. It rejects requests when that
header is missing or contains only whitespace.

This header-based approach is a temporary development placeholder, not secure
authentication. A client can claim any user ID because no password, session,
or signed access token is verified. In production, this function should verify
a trusted login credential such as a JWT and return the authenticated user's
ID. Keeping this responsibility in one dependency allows the authentication
method to be replaced later without changing every route that uses it.
"""

from typing import Optional

from fastapi import Header, HTTPException, status


def get_current_user_id(x_user_id: Optional[str] = Header(default=None)) -> str:
    """Read and validate the temporary ``X-User-ID`` request header.

    Args:
        x_user_id: The value supplied in the request's ``X-User-ID`` header.
            FastAPI passes ``None`` when the header is not present.

    Returns:
        The user ID after removing whitespace from its beginning and end.

    Raises:
        HTTPException: Returns HTTP 401 when the header is missing or blank.

    Warning:
        This function identifies a user but does not securely authenticate
        them. Replace the header check with real credential verification
        before using the application in production.
    """
    if x_user_id is None or not x_user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user identity"
        )
    return x_user_id.strip()
