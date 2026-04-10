import smtplib
from email.mime.text import MIMEText
from Config.config import EMAIL, EMAIL_PASSWORD

def send_email(receiver: str, message: str) -> str:
    if EMAIL is None:
        raise ValueError("EMAIL is not configured")
    if EMAIL_PASSWORD is None:
        raise ValueError("EMAIL_PASSWORD is not configured")

    msg = MIMEText(message)
    msg["Subject"] = "Message from Ishwar's AI Agent"
    msg["From"] = EMAIL
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, receiver, msg.as_string())
        return "Email sent successfully."
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError("Authentication failed. Check your email credentials.")
    except smtplib.SMTPRecipientsRefused:
        raise RuntimeError(f"Recipient address refused: {receiver}")
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}")