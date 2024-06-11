import smtplib, ssl
from email.mime.text import MIMEText
from os import getenv

def send_email(receiver_email:str, user_email:str):
    host = 'smtp.gmail.com'
    port = 465

    username = getenv('EMAIL')
    password =getenv('APPKEY_eLearning')

    receiver = getenv('EMAIL') #receiver_email    
    context = ssl.create_default_context()

    message = f'''\
Subject: Approval needed\n
        User with email {user_email} waiting for approval!
        Please login into your account and aprove it!
        '''

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def send_multiple_email(recipients_emails:list[str], course_title:str):
    host = 'smtp.gmail.com'
    port = 587

    username = getenv('EMAIL')
    password =getenv('APPKEY_eLearning')

    #recipients = " .".join(recipients_emails)

    message = MIMEText(f'''
        Course {course_title} has been deleted from E-Learning!
        ''')
    message['Subject'] = 'Removed Course'
    message["From"] = username
    message["To"] = " ,".join(recipients_emails)

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipients_emails, message.as_string())
    server.quit()



#recipients = [
#   "example@example.com",
#   "example1@example.com",
#   "example2@example.com",
#]
#s = smtplib.SMTP("smtp.gmail.com", 587)
#s.starttls()
#s.login("yourmail@gmail.com", "password")
#msg = MIMEText("""your body text""")
#sender = "yourmail@gmail.com"
#msg["Subject"] = "Mail subject"
#msg["From"] = sender
#msg["To"] = " .".join(recipients)
#s.sendmail(sender, recipients, msg.as_string())
#s.quit()