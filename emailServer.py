import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailServer:
    """
    The EmailServer is meant to help streamline pandas dataframes that have been
    converted to html.
    """
    def __init__(self, smtp_server, port, sender_email, password, email_list):
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.email_list = email_list
        self.password = password
        self.server = smtplib.SMTP_SSL(self.smtp_server, port, context=ssl.create_default_context())
        self.message = MIMEMultipart("alternative")

    def mail_composition(self, subject, email_from, recipient, intro, body, conclusion):
        # Components of email message
        self.message["Subject"] = subject
        self.message["From"] = email_from
        self.message["To"] = recipient

        # Compose Message
        message_content = intro + body + conclusion
        data = MIMEText(message_content, "html")

        # Attach message to email
        self.message.attach(data)

    def send_message(self, recipient):
        # Create secure connection with server and send email
        self.server.ehlo()
        self.server.login(self.sender_email, self.password)
        self.server.sendmail(self.sender_email, recipient, self.message.as_string())

    def __del__(self):
        # Ensure email service is shutdown
        print("Server is closed and all credentials have been deleted")




