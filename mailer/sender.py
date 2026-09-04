import smtplib
from email.message import EmailMessage

from common.logger import logger


def send_email(
    *,
    sender: str,
    recipient: str,
    app_password: str,
    subject: str,
    body: str,
    html_body: str | None = None,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 587,
) -> bool:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    if html_body:
        message.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(sender, app_password)
            smtp.send_message(message)

        logger.info("Email sent successfully to %s.", recipient)
        return True

    except (smtplib.SMTPException, OSError):
        logger.exception("Failed to send email.")
        return False
