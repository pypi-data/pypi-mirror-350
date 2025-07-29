# Contacted Python SDK

Official Python SDK for the Contacted API.

[![PyPI version](https://badge.fury.io/py/contacted.svg)](https://badge.fury.io/py/contacted)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Support](https://img.shields.io/pypi/pyversions/contacted.svg)](https://pypi.org/project/contacted/)

## Getting Started

### 1. Get Your API Key

First, sign up and get your API key at [https://contacted.io](https://contacted.io)

### 2. Installation

```bash
pip install contacted
```

## Quick Start

```python
from contacted import ContactedAI

contacted = ContactedAI(api_key='your-api-key-here')

# Send a message
result = contacted.send({
    'from': 'sender@example.com',
    'to': 'receiver@example.com',
    'prompt': 'Generate a personalized welcome email',
    'data': {
        'name': 'John Doe',
        'link': 'https://example.com'
    }
})

print('Message sent:', result)
```

## Type Hints Support

The SDK includes comprehensive type hints for better IDE support:

```python
from contacted import ContactedAI
from typing import Dict, Any

contacted = ContactedAI(api_key='your-api-key-here')

options: Dict[str, Any] = {
    'from': 'sender@example.com',
    'to': 'receiver@example.com',
    'prompt': 'Generate email content',
    'data': {'name': 'John'}
}

result = contacted.send(options)
```

## API Reference

### `ContactedAI(api_key, base_url=None, timeout=30)`

Creates a new ContactedAI client instance.

**Parameters:**
- `api_key` (str, required): Your ContactedAI API key
- `base_url` (str, optional): Custom API base URL
- `timeout` (int, optional): Request timeout in seconds (default: 30)

### `contacted.send(options)`

Send a message through the ContactedAI API.

**Parameters:**
- `from` (str, required): Valid sender email address
- `to` (str, required): Valid receiver email address
- `prompt` (str, required): AI prompt (10-250 characters)
- `data` (dict, optional): Additional data for personalization

**Validation Rules:**
- Email addresses must be valid format
- Prompt must be 10-250 characters
- Data keys cannot contain spaces
- Data keys must be non-empty strings

**Returns:** `dict` - API response

**Raises:** `ValueError` - If validation fails or API error occurs

### `contacted.status()`

Check the API status and health.

**Returns:** `dict` - Status information

## Error Handling

The SDK provides detailed error messages for validation and API errors:

```python
try:
    contacted.send({
        'from': 'invalid-email',
        'to': 'user@example.com',
        'prompt': 'short'
    })
except ValueError as e:
    print(f'Error: {e}')
    # "Invalid 'from' email address format"
```

## Examples

### Basic Usage
```python
from contacted import ContactedAI
import os

contacted = ContactedAI(api_key=os.getenv('CONTACTED_API_KEY'))

result = contacted.send({
    'from': 'noreply@myapp.com',
    'to': 'user@example.com', 
    'prompt': 'Create a welcome email for a new premium user',
    'data': {
        'username': 'john_doe',
        'plan': 'premium',
        'dashboard_url': 'https://app.myservice.com'
    }
})
```

### With Error Handling
```python
try:
    result = contacted.send(options)
    print(f'✅ Email sent successfully: {result["id"]}')
except ValueError as e:
    if 'Invalid' in str(e):
        print(f'❌ Validation error: {e}')
    else:
        print(f'❌ API error: {e}')
```

### Environment Variables
```python
import os
from contacted import ContactedAI

# Use environment variable for API key
contacted = ContactedAI(
    api_key=os.getenv('CONTACTED_API_KEY'),
    timeout=60  # Custom timeout
)
```

## License

MIT

## Support

- 📧 Email: support@contacted.io
- 🐛 Issues: [GitHub Issues](https://github.com/LawrenceGB/contacted-python/issues)
- 📖 Documentation: [contacted.gitbook.io](https://contacted.gitbook.io)