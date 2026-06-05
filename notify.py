import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl


def send_email_report(recipient, json_path):
    sender_email = os.environ["EMAIL_USER"]
    sender_password = os.environ["EMAIL_PASSWORD"]

    subject = "Web Crawler Report"
    body_text = "Please find the attached report from the web crawler."

    try:
        with open(json_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(json_path)}",
            )

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        body = MIMEText(body_text, "plain")
        message.attach(body)
        message.attach(part)


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
    





