import re
from typing import Optional

__all__ = ["is_valid_password", "validate_password"]

def is_valid_password(password: str,
                      min_length: int = 8,
                      max_length: int = 50,
                      require_upper: bool = True,
                      require_lower: bool = True,
                      require_digit: bool = True,
                      require_special: bool = True) -> bool | str:
    if not isinstance(password, str):
        return "Password must be a string."

    errors = []
    if len(password) < min_length:
        errors.append(f"Must be at least {min_length} characters.")
    if len(password) > max_length:
        errors.append(f"Must be at most {max_length} characters.")
    if require_upper and not re.search(r'[A-Z]', password):
        errors.append("Must include at least one uppercase letter.")
    if require_lower and not re.search(r'[a-z]', password):
        errors.append("Must include at least one lowercase letter.")
    if require_digit and not re.search(r'\d', password):
        errors.append("Must include at least one digit.")
    if require_special and not re.search(r'[\W_]', password):
        errors.append("Must include at least one special character.")

    return True if not errors else "; ".join(errors)

def validate_password(password: str,
                      min_length: int = 8,
                      max_length: int = 128,
                      require_upper: bool = True,
                      require_lower: bool = True,
                      require_digit: bool = True,
                      require_special: bool = True) -> None:
    result = is_valid_password(
        password,
        min_length,
        max_length,
        require_upper,
        require_lower,
        require_digit,
        require_special
    )
    if result is not True:
        raise ValueError(f"Invalid password: {result}")