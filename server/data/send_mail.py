import smtplib, ssl
from email.mime.text import MIMEText
from os import getenv


def send_email(receiver_email:str, user_email:str, user_id:int):
    host = 'smtp.gmail.com'
    port = 465

    username = getenv('EMAIL')
    password =getenv('APPKEY_eLearning')

    receiver = getenv('EMAIL') #receiver_email    
    context = ssl.create_default_context()

    message = f'''\
Subject: Approval needed\n
        User with ID: {user_id}. and email {user_email} waiting for approval!
        You can approve his register with click on the link http://127.0.0.1:8000/users/login
        '''

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def send_multiple_email(recipients_emails:list[str], user_email:str, user_id:int):
    host = 'smtp.gmail.com'
    port = 587

    username = getenv('EMAIL')
    password =getenv('APPKEY_eLearning')

    #recipients = " .".join(recipients)
    recipients = [
   "rdimitrov877@gmail.com",
   "rd94@icloud.com"
   ]

    message = MIMEText(f'''
        User with ID: user_id. and email user_email waiting for approval!
        You can approve his register with click on the link
        ''')
    message['Subject'] = 'Aproval needed'
    message["From"] = username
    message["To"] = " .".join(recipients)

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipients, message.as_string())
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