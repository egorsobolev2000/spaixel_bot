import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from post.accesses import MAIL, PASSWORD


def read_json(username):
    logs = os.listdir('./post/logs/')
    for file in logs:
        if file.split('$')[0] == username:
            from post.collect_data import JSONFile
            data = JSONFile(f'./post/logs/{file}', d_or_l='load')
            return data


def send(username, message='s'):
    """ Функция опоощения на почту при N событии """

    login = MAIL
    password = PASSWORD

    msg = MIMEMultipart('alternative')
    msg['From'] = login
    msg['To'] = login
    if message == 's':
        msg['Subject'] = f'Новый пользователь @{username} 👍'
        body = f'Зафиксирована активность нового пользователя бота @{username}'
    else:
        msg['Subject'] = f'📮 Новая заявка с бота от @{username}'
        data = read_json(username)
        user_log = ''
        for m in data['messages']:
            user_log += f'{str(m)[1: -1]}<br>'

        body = f'<b>История сообщений пользователя <em>@{username}</em></b><br><br>{user_log}'

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login, password)
    print("Отправка письма...")
    server.send_message(msg)
    server.quit()
    print('\x1b[6;30;42m' + 'Email successfully sent' + '\x1b[0m')
