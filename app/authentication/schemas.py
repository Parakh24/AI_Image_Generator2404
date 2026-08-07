"""Define validated data shapes used by the authentication system.

Pydantic models in this module turn untrusted token data into predictable
Python objects. Other modules can then use these objects without repeatedly
checking the type and name of every authentication field.
"""

from pydantic import BaseModel, Field
from typing import Optional

class TokenPayload(BaseModel):
    """Represent the identity fields expected inside a decoded JWT.

    ``sub`` is the standard JWT subject field and commonly contains the user
    ID. ``user_id`` supports tokens that store the same identifier under an
    explicit name. ``tenant_id`` identifies the organization or tenant to which
    the user belongs.
    """
    sub: Optional[str] = None       # Usually user_id
    user_id: Optional[str] = None   # Explicit user_id
    tenant_id: str                  # Multi-tenant Context

class CurrentUser(BaseModel):
    """Represent the trusted user information passed to protected routes.

    Attributes:
        id: Unique identifier of the authenticated user.
        tenant_id: Identifier of the user's organization or tenant.
    """
    id: str = Field(..., description="Authenticated User ID")
    tenant_id: str = Field(..., description="Associated Tenant/Organization ID")
