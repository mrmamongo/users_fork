import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage

from src.config.settings import EMAIL_LOGIN, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT


class BaseEmailSender(ABC):
    def __init__(self, receiver):
        self.subject = ...
        self.sender = EMAIL_LOGIN
        self.receiver = receiver

    @abstractmethod
    def get_message(self):
        ...

    @abstractmethod
    def send_email(self):
        ...


class VerificationEmailSender(BaseEmailSender):
    def __init__(self, receiver):
        super().__init__(receiver)
        self.subject = "Подтверждение электронной почты"

    def get_message(self):
        email = EmailMessage()
        email["Subject"] = self.subject
        email["From"] = EMAIL_LOGIN
        email["To"] = self.receiver
        email.set_content(
            "<div>"
            f"<h1>Здравствуйте, {self.receiver}!</h1>"
            "<p>Благодарим Вас за регистрацию, чтобы продолжить, пожалуйста, перейдите по ссылке:</p>"
            "http://127.0.0.1:8000/"
            "</div>",
            subtype="html",
        )
        return email

    def send_email(self):
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            smtp.send_message(self.get_message())