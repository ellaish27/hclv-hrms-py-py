# services/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('GMAIL_USER')
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_APP_PASSWORD'))
        server.sendmail(os.getenv('GMAIL_USER'), to, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"📧 Email error: {e}")
        raise
