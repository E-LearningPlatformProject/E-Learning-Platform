import smtplib, ssl
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