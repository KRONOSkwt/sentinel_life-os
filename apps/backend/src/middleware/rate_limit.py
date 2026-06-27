"""Rate limiting middleware using slowapi."""

from slowapi import Limiter
from slowapi.util import get_remote_address

# 10 requests per minute for auth endpoints
auth_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10/minute"],
    storage_uri="memory://",
)

# 100 requests per minute for general endpoints
general_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    storage_uri="memory://",
)