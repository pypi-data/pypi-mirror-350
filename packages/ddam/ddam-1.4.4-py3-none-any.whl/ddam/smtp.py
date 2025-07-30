import logging
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        ssl: bool,
        email_from: str,
        recipients: list[str],
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.ssl = ssl
        self.email_from = email_from
        self.recipients = recipients

    def send(self, subject: str, body: str):
        smtp_cls: type[smtplib.SMTP_SSL] | type[smtplib.SMTP]

        smtp_cls = smtplib.SMTP_SSL if self.ssl else smtplib.SMTP

        message = MIMEText(body)
        message["From"] = self.email_from
        message["To"] = ", ".join(self.recipients)
        message["Subject"] = subject

        logger.debug("Sending email")
        with smtp_cls(self.smtp_host, port=self.smtp_port) as smtp:
            smtp.sendmail(self.email_from, self.recipients, message.as_bytes())
        logger.debug("Email sent")
