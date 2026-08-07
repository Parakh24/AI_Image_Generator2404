"""Load the settings used to decode authentication access tokens.

The application uses these settings when it validates JSON Web Tokens (JWTs).
Values may come from environment variables or a local ``.env`` file. Keeping
the settings in one module prevents token-handling code from repeating the same
configuration.

The fallback secret key is intended only for local development. A production
deployment must provide a strong ``JWT_SECRET_KEY`` environment variable and
must keep that value private.
"""

import os
from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):
    """Describe the configurable values used for JWT authentication.

    Attributes:
        SECRET_KEY: Private key used to verify that a JWT was issued by a
            trusted source and has not been changed.
        ALGORITHM: Cryptographic algorithm expected when decoding a token.
        ACCESS_TOKEN_EXPIRE_MINUTES: Intended lifetime of an access token in
            minutes. The current value represents 24 hours.
    """
    # JWT Secret Key (Production mein Environment variable se aana chahiye)
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "u7Kq1s$e8!ZwP#2n@AvRxL&TgVwYdXc3QfEhRjUkMnBoIpL0Sz")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # <-- MAJOR BUG FIX HERE
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 Hours

    class Config:
        """Tell Pydantic to read additional setting values from ``.env``."""
        env_file = ".env"
        extra = "ignore"

auth_settings = AuthSettings()
