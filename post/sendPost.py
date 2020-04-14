import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from post.accesses import MAIL, PASSWORD


def send(username):

    login = MAIL
    password = PASSWORD

    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = login
    msg['Subject'] = f'Новый пользователь бота @{username}'
    body = f'Зафиксирована активность нового пользователя бота @{username}'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login, password)
    print("Отправка письма...")
    server.send_message(msg)
    server.quit()
    print('\x1b[6;30;42m' + 'Email successfully sent' + '\x1b[0m')
