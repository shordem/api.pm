import os
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from pathlib import Path

from schemas.email import EmailSchema

load_dotenv()

templates = Jinja2Templates(directory=Path(__file__).parent / "../templates/")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_HOST"),
    MAIL_FROM_NAME="Todo App",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

mail = FastMail(conf)


async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=[email.to],
        body=templates.TemplateResponse(
            name=email.template, context={"request": None, **email.variables}
        ).body,
        subtype="html",
    )
    await mail.send_message(message)
