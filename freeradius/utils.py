import string
import secrets  # Use secrets for secure generation in Python 3.6+

def generate_random_string(length=8):
    """
    Generates a random string of specified length using recommended methods for security.
    """

    alphabet = string.ascii_letters + string.digits + string.punctuation  # Include a wider range of characters
    return ''.join(secrets.choice(alphabet) for i in range(length))

def generate_random_password(length=16):
    """
    Generates a secure random password using recommended guidelines.
    """

    try:
        # Use secrets.token_urlsafe for strong, URL-safe passwords (preferred)
        password = secrets.token_urlsafe(length)
    except AttributeError:  # Fallback for Python versions < 3.6
        password = generate_random_string(length)  # Use secure string generation

    # Ensure a mix of character types for password strength
    while not (any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password)):
        password = generate_random_password(length)  # Regenerate until requirements are met

    return password
