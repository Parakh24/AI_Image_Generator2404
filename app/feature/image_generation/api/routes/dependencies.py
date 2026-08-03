"""
dependencies.py

TEMPORARY stub for "who is making this request". Real authentication
(login, JWT tokens, sessions) has not been built yet in this project.
Every route that needs to know the current user depends on this
function - once real auth exists, only this file changes, no route
code needs to change.
"""

from typing import Optional

from fastapi import Header, HTTPException, status


def get_current_user_id(x_user_id: Optional[str] = Header(default=None)) -> str:
    """
    STUB ONLY - reads the user id directly from a request header.
    This is NOT secure: anyone can put any user id in this header
    and pretend to be that user. Replace this with real token
    verification before this goes anywhere near production.
    """
    if x_user_id is None or not x_user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user identity"
        )
    return x_user_id.strip()
