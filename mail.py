# mail.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send a verification email
def send_verification_email(to, verification_link):
    try:
        # Create a multi-part message to include both plain text and HTML content
        message = MIMEMultipart("alternative")
        
        # Email subject and sender information
        message["Subject"] = "Email Verification"
        message["From"] = "angel.assist.2.0@gmail.com"
        message["To"] = to

        # Plain text content (fallback)
        text_content = f"""
        Hello,

        Thank you for registering with Chat with PDFs. To complete your registration, please verify your email address by clicking the link below:
        
        {verification_link}

        If you did not request this verification, please ignore this email.

        Best regards,
        Chat with PDFs
        """

        # HTML content with a hyperlink
        html_content = f"""
        <html>
        <head></head>
        <body>
            <p>Hello,</p>
            <p>Thank you for registering with Chat with PDFs. To complete your registration, please verify your email address by clicking the link below:</p>
            <p><a href="{verification_link}">Verify My Email</a></p>
            <p>If you did not request this verification, please ignore this email.</p>
            <p>Best regards,<br>Chat with PDFs</p>
        </body>
        </html>
        """

        # Attach both plain text and HTML parts to the message
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)

        # Create SMTP session
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()  # Upgrade to secure connection

        # Login to Gmail account
        session.login("angel.assist.2.0@gmail.com", "dkpj jbgs tflh rlaz")  # Avoid storing passwords in plaintext

        # Send the email
        session.sendmail(message["From"], message["To"], message.as_string())
        session.quit()  # Cleanly close the SMTP session

        print("Verification email sent successfully.")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")  # Provide more detailed error information
        return False

# Example use of send_verification_email
# send_verification_email("prasaddhaneshwar22@gmail.com", "https://chatpdfhome.streamlit.app/")
# sendEmail('prasaddhaneshwar22@gmail.com', 'hii')
