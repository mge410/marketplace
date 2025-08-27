from email.message import EmailMessage

import aiosmtplib

from src.core.config import settings


async def send_email(recipient: str, subject: str, body: str) -> None:
    admin_email = settings.email_config.admin_email

    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=recipient,
        hostname=settings.email_config.smtp_host,
        port=settings.email_config.smtp_port,
    )
