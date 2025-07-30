# Django Mailomat

A Django email backend for sending emails through the Mailomat API.

## Installation

```bash
pip install django-mailomat
```

## Configuration

Add the following settings to your Django settings file:

```python
# Mailomat settings
MAILOMAT_API_URL = 'http://mailomat-api:5000'  # Your Mailomat API URL
MAILOMAT_API_TOKEN = 'your-api-token'  # Your Mailomat API token
DEFAULT_FROM_EMAIL = 'noreply@example.com'  # Default sender email

# Use the Mailomat email backend
EMAIL_BACKEND = 'django_mailomat.backend.MailomatEmailBackend'
```

## Usage

The backend can be used like any other Django email backend:

```python
from django.core.mail import send_mail

send_mail(
    'Subject',
    'Message',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

## Features

- Supports both plain text and HTML email content
- Handles email attachments
- Includes API token authentication
- Sanitizes email addresses
- Configurable fail_silently option

## Development

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`

## License

MIT License 