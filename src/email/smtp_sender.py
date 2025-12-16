import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SMTPSender:

    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587, username="", app_password=""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.app_password = app_password

    def send_email(self, to_email, subject, body_text):
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body_text, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.app_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print("SMTP Error:", e)
            return False
