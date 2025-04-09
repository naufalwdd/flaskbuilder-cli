from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash a password."""
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """Verify a hashed password."""
    return check_password_hash(hashed_password, password)