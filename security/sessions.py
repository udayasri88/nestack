import secrets
import hashlib
from datetime import datetime, timedelta, timezone


# Generate a secure session token
def generate_session_token():

    return secrets.token_urlsafe(32)


# Hash the session token
def hash_session_token(token):

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


# Generate session expiration time
def get_session_expiry():

    expiry = datetime.now(timezone.utc) + timedelta(hours=1)

    return expiry.isoformat()