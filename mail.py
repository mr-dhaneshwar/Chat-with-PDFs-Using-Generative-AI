import smtplib
from email.mime.text import MIMEText


def sendEmail(to, content=""):
    try:
        message = MIMEText("Click here to login--> "+content)
        message['From'] = 'angel.assist.2.0@gmail.com'
        message['To'] = to
        message['Subject'] = 'Verify user'

        # Create SMTP session
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()

        # Login to Gmail account
        session.login('angel.assist.2.0@gmail.com', 'dkpj jbgs tflh rlaz')

        # Send email
        session.sendmail('angel.assist.2.0@gmail.com', to, message.as_string())
        print('Email sended succesfully')
        session.quit()
        return True
    except:
        return False


# sendEmail('prasaddhaneshwar22@gmail.com', 'hii')
