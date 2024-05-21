import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, message):
    from_email = "spyfact0gmail.com"
    password = "8858439385"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # Use SSL port 
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())