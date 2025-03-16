import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email_with_attachment(subject, body, to_email, from_email, app_password, attachment_path):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a multipart email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach the file
    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, "rb") as attachment_file:
            # Create a MIMEBase object
            mime_base = MIMEBase("application", "octet-stream")
            mime_base.set_payload(attachment_file.read())
            encoders.encode_base64(mime_base)
            # Add header for the attachment
            mime_base.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(mime_base)
    else:
        print("Attachment file not found or path is invalid.")
        return

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(from_email, app_password)  # Login with the app password

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully with attachment.")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()  # Close the server connection




if __name__ == "__main__":
    # Usage example
    subject = "Test Email with Attachment from Python"
    body = "This is a test email with an attachment sent from Python using Gmail SMTP."
    to_email = ""
    from_email = ""
    app_password = ""  # Use the app password generated in your Google account
    attachment_path = "output.csv"  # Replace with the actual file path
    send_email_with_attachment(subject, body, to_email, from_email, app_password, attachment_path)
