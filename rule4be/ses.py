from django.core.mail import send_mail
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger('custom_email_logger')


def send_custom_email(subject, body, to_email):
    """
    Send a custom email using the AWS SES service
    """
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {to_email} via SES.")
    except Exception as e:
        logger.error(f'Error sending email to {to_email}: {e}')
