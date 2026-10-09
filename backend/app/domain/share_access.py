"""Share token generation and validation for review access."""
import secrets


def generate_share_token() -> str:
    """Generate a secure random share token.
    
    Returns:
        Secure random token string (32 characters hex)
    """
    return secrets.token_urlsafe(24)  # 24 bytes = 32 chars base64url


def validate_share_token(token: str) -> bool:
    """Validate share token format.
    
    Args:
        token: Share token to validate
        
    Returns:
        True if token format is valid (24-64 chars)
    """
    if not token or not isinstance(token, str):
        return False
    
    # Token should be 24-64 chars per LLD Section 4.10
    return 24 <= len(token) <= 64
