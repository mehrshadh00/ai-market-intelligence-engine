import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(to_email, subject, body):
    recipient = (to_email or "").strip()

    host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    username = os.getenv("SMTP_USERNAME", "").strip()
    app_password = os.getenv("SMTP_APP_PASSWORD", "").strip().replace(" ", "")
    sender = os.getenv("SMTP_FROM", "").strip() or username

    try:
        port = int(os.getenv("SMTP_PORT", "587").strip())
    except ValueError:
        return {
            "success": False,
            "message": "SMTP_PORT is invalid. It must be 587.",
        }

    if not recipient:
        return {
            "success": False,
            "message": "Please enter the recipient email address.",
        }

    if not username:
        return {
            "success": False,
            "message": "SMTP_USERNAME is missing from .env.",
        }

    if not app_password:
        return {
            "success": False,
            "message": "SMTP_APP_PASSWORD is missing from .env.",
        }

    if not host:
        return {
            "success": False,
            "message": "SMTP_HOST is empty.",
        }

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject or "Business Opportunity"
    message.set_content(body or "")

    try:
        print(f"[EMAIL] Connecting to {host}:{port}")
        print(f"[EMAIL] Sender: {sender}")
        print(f"[EMAIL] Recipient: {recipient}")

        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(username, app_password)
            smtp.send_message(message)

        return {
            "success": True,
            "message": f"Email sent successfully to {recipient}.",
        }

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "message": (
                "Gmail authentication failed. "
                "Check your Gmail address and App Password."
            ),
        }

    except smtplib.SMTPRecipientsRefused:
        return {
            "success": False,
            "message": "Gmail rejected the recipient address.",
        }

    except smtplib.SMTPException as exc:
        return {
            "success": False,
            "message": f"SMTP error: {exc}",
        }

    except OSError as exc:
        return {
            "success": False,
            "message": f"Network/SMTP connection error: {exc}",
        }

    except Exception as exc:
        return {
            "success": False,
            "message": f"Unexpected email error: {exc}",
        }
