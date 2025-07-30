"""
Validation module for ContactedAI SDK
Matches backend schema validation exactly
"""

import re
from typing import Dict, Any


def is_valid_email(email: str) -> bool:
    """
    Validates email format

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if valid email format, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    # Basic format check: must have exactly one @ symbol
    at_count = email.count('@')
    if at_count != 1:
        return False

    local_part, domain_part = email.split('@')

    # Check local part (before @)
    if not local_part:
        return False
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    if '..' in local_part:
        return False

    # Check domain part (after @)
    if not domain_part:
        return False
    if '.' not in domain_part:  # Must have at least one dot for TLD
        return False
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return False
    if '..' in domain_part:
        return False

    # Comprehensive regex for the full email
    email_regex = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$'
    )

    return bool(email_regex.match(email))


def validate_subject(subject: Any) -> None:
    """
    Validates subject according to backend schema

    Args:
        subject: Subject to validate

    Raises:
        ValueError: If validation fails
    """
    # Check if subject exists (required)
    if subject is None:
        raise ValueError("Subject is required")

    # Check if subject is a string
    if not isinstance(subject, str):
        raise ValueError("Subject must be a string")

    # Check length (2-256 characters)
    if len(subject) < 2:
        raise ValueError("Subject must be at least 2 characters long")

    if len(subject) > 256:
        raise ValueError("Subject must be no more than 256 characters long")


def validate_prompt(prompt: Any) -> None:
    """
    Validates prompt according to backend schema

    Args:
        prompt: Prompt to validate

    Raises:
        ValueError: If validation fails
    """
    # Check if prompt exists (required)
    if prompt is None:
        raise ValueError("Prompt is required")

    # Check if prompt is a string
    if not isinstance(prompt, str):
        raise ValueError("Prompt must be a string")

    # Check length (10-250 characters)
    if len(prompt) < 10:
        raise ValueError("Prompt must be at least 10 characters long")

    if len(prompt) > 250:
        raise ValueError("Prompt must be no more than 250 characters long")


def validate_data(data: Any) -> None:
    """
    Validates data object according to backend schema

    Args:
        data: Data object to validate

    Raises:
        ValueError: If validation fails
    """
    # Data is optional, so None is fine
    if data is None:
        return

    # Check if data is a dictionary
    if not isinstance(data, dict):
        raise ValueError("Data must be an object")

    # Check all keys and values
    for key, value in data.items():
        # Check that key is a non-empty string
        if not isinstance(key, str) or not key.strip():
            raise ValueError("All data keys must be non-empty strings")

        # Check if key contains spaces or whitespace
        if re.search(r'\s', key):
            raise ValueError("Data keys cannot contain spaces")

        # Values can be any type as mentioned in UI comment
        # "Don't worry about types" - so no validation on values needed


def validate_emails(from_email: Any, to_email: Any) -> None:
    """
    Validates email addresses

    Args:
        from_email: Sender email address
        to_email: Receiver email address

    Raises:
        ValueError: If validation fails
    """
    # Check required fields
    if not from_email or not to_email:
        raise ValueError('Both "from" and "to" email addresses are required')

    # Check if they are strings
    if not isinstance(from_email, str) or not isinstance(to_email, str):
        raise ValueError("Email addresses must be strings")

    # Validate email format
    if not is_valid_email(from_email):
        raise ValueError('Invalid "from" email address format')

    if not is_valid_email(to_email):
        raise ValueError('Invalid "to" email address format')


def validate_send_options(options: Any) -> None:
    """
    Main validation function for send options

    Args:
        options: Send options to validate

    Raises:
        ValueError: If any validation fails
    """
    if not options or not isinstance(options, dict):
        raise ValueError("Send options must be a dictionary")

    subject = options.get('subject')
    from_email = options.get('from')
    to_email = options.get('to')
    prompt = options.get('prompt')
    data = options.get('data')

    # Validate emails
    validate_emails(from_email, to_email)

    # Validate subject
    validate_subject(subject)

    # Validate prompt
    validate_prompt(prompt)

    # Validate data
    validate_data(data)