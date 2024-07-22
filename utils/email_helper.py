# email_config.py
import asyncio

from fastapi import HTTPException
from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail, MessageSchema
from pydantic import BaseModel, EmailStr
from typing import List

from starlette.background import BackgroundTasks


class EmailSchema(BaseModel):
    subject: str
    recipients: List[EmailStr]
    body: str


conf = ConnectionConfig(
    MAIL_USERNAME="helloahao@icloud.com",
    MAIL_PASSWORD="ozrb-whio-mtjz-nuco",
    MAIL_FROM="helloahao@icloud.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.mail.me.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

class EmailContent(BaseModel):
    subject: str
    recipients: List[EmailStr]
    body: str
    subtype: str = "plain"

class EmailUtils:
    def __init__(self, conf):
        self.fm = FastMail(conf)

    async def send_email(self, email_content: EmailContent):
        message = MessageSchema(
            subject=email_content.subject,
            recipients=email_content.recipients,
            body=email_content.body,
            subtype=email_content.subtype
        )
        await self.fm.send_message(message)



email_utils = EmailUtils(conf)

async def send_email(email: EmailSchema):
    email_content = EmailContent(
        subject=email.subject,
        recipients=email.recipients,
        body=email.body
    )
    try:
        await email_utils.send_email(email_content)
        # return {"message": "Email will be sent in background"}
        return {"message": "Email will be sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    email_data = {
        "subject" : "test email",
        "recipients" : ["helloahao@qq.com"],
        "body" : "token test"
    }
    email: EmailSchema = EmailSchema(**email_data)
    # asyncio.run()
    send_email(email)