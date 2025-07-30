import logging
from email.utils import formataddr
from typing import Any, List, Optional, Union

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives

logger = logging.getLogger(__name__)

class MailomatEmailBackend(BaseEmailBackend):
    """
    A Django email backend that sends emails through the Mailomat API.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.api_url = getattr(settings, 'MAILOMAT_API_URL', '')
        self.api_token = getattr(settings, 'MAILOMAT_API_TOKEN', '')

    def _sanitize_email(self, email: str) -> str:
        """
        Sanitize email address by removing any display name.
        """
        if '<' in email and '>' in email:
            return email.split('<')[1].split('>')[0]
        return email

    def _format_email(self, email: str, name: Optional[str] = None) -> str:
        """
        Format email address with optional display name.
        """
        if name:
            return formataddr((name, self._sanitize_email(email)))
        return self._sanitize_email(email)

    def _send(self, email_message: Union[EmailMessage, EmailMultiAlternatives]) -> bool:
        """
        Send a single email message through the Mailomat API.
        """
        if not email_message.recipients():
            return False

        # Prepare email data
        data = {
            'to': [self._sanitize_email(recipient) for recipient in email_message.recipients()],
            'subject': email_message.subject,
            'text': email_message.body,
            'html': None,
            'from': self._format_email(
                email_message.from_email,
                getattr(email_message, 'from_name', None)
            ),
        }

        # Handle HTML content
        if isinstance(email_message, EmailMultiAlternatives):
            for content, mimetype in email_message.alternatives:
                if mimetype == 'text/html':
                    data['html'] = content
                    break

        # Handle attachments
        if email_message.attachments:
            data['attachments'] = []
            for filename, content, mimetype in email_message.attachments:
                if isinstance(content, bytes):
                    data['attachments'].append({
                        'filename': filename,
                        'content': content.decode('utf-8'),
                        'mimetype': mimetype
                    })

        # Send request to Mailomat API
        try:
            response = requests.post(
                f"{self.api_url}/send",
                json=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_token}'
                }
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            if not self.fail_silently:
                logger.error(f"Failed to send email through Mailomat API: {e}")
                raise
            return False

    def send_messages(self, email_messages: List[Union[EmailMessage, EmailMultiAlternatives]]) -> int:
        """
        Send multiple email messages through the Mailomat API.
        """
        if not email_messages:
            return 0

        success_count = 0
        for message in email_messages:
            if self._send(message):
                success_count += 1

        return success_count 