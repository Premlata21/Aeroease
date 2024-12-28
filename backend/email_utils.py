from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

# Debugging lines to check if environment variables are loaded correctly
print("MAIL_PORT:", os.getenv("MAIL_PORT"))
print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("MAIL_SERVER:", os.getenv("MAIL_SERVER"))

MAIL_PORT = os.getenv("MAIL_PORT")

if MAIL_PORT is None:
    raise ValueError("MAIL_PORT environment variable is not set")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(MAIL_PORT),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
)

async def send_verification_email(email: str):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body="Please verify your email.",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name=None)

async def send_password_reset_email(email: str):
    message = MessageSchema(
        subject="Password Reset",
        recipients=[email],
        body="Click here to reset your password.",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
