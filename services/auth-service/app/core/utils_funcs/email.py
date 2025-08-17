# app/core/utils/email.py
from email.message import EmailMessage
from aiosmtplib import send
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[3] / ".env"

load_dotenv(dotenv_path=env_path, override=True)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)

async def send_verification_email(to_email: str, code: str):
    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = "Your Verification Code"
    message.set_content(f"Your verification code is: {code}")

    await send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
    )


async def send_query_email(to_email: str, msg: str):
    message = EmailMessage()
    message["From"] = to_email
    message["To"] = FROM_EMAIL
    message["Subject"] = "Sehat App User sent query"
    message.set_content(f"The query is: {msg}")

    await send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
    )
