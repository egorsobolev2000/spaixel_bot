import os
import time
import smtplib
from email.mime.text import MIMEText
from telegram import ReplyKeyboardRemove
from email.mime.multipart import MIMEMultipart

from post.accesses import MAIL, PASSWORD


def read_json(username):
    from post.collect_data import JSONFile
    """ Функция возвращает загруженный в словарь
        набор данных конкретного пользователя """

    logs = os.listdir('./post/logs/')

    for file in logs:
        if file.split('$')[0] == username:
            data = JSONFile(f'./post/logs/{file}', d_or_l='load')
            return data


def get_format_data(data):
    """ Функция возвращает структурированную стороку
        состоящию из иниформации о действиях пользователя """
    format_string = ''
    for m in data:
        format_string += f'{str(m)[1: -1]}<br>'
    return format_string


def plus_post_bun(post_ban_list, username):
    from post.collect_data import JSONFile
    post_ban_list.get(username)[0] += 1
    JSONFile(f'./post/logs/POST_BAN.json', post_ban_list)


def send_to_black_list(username, update, context):
    from post.collect_data import JSONFile
    user_ban_list = JSONFile('./post/BLACK_LIST.json', d_or_l='load')
    user_ban_list.update({username: time.strftime("%x-%X", time.localtime())})
    JSONFile(f'./post/BLACK_LIST.json', user_ban_list)
    send(username, update, context, 'black_list')


def send(username, update, context, message='new_user'):
    from post.collect_data import JSONFile
    from bot_logic import typing
    from bot_logic import send_sticker
    """ Функция оповещения на почту при N событии """
    post_ban_list = JSONFile('./post/logs/POST_BAN.json', d_or_l='load')
    if username not in post_ban_list.keys() \
            or post_ban_list[username][1].split('-')[0] != time.strftime("%x", time.localtime()) \
            or message == 'black_list':
        login = MAIL
        password = PASSWORD
        msg = MIMEMultipart('alternative')
        msg['From'] = login
        msg['To'] = login
        if message == 'new_user':
            msg['Subject'] = f'Новый пользователь @{username} 👍'
            body = f'Зафиксирована активность нового пользователя бота @{username}'
        elif message == 'request' or 'brif_list':

            data = read_json(username)
            user_msg, user_actions = get_format_data(data['messages']), get_format_data(data['actions'])

            body = f'<b>История сообщений пользователя <em>@{username}</em></b>' \
                   f'<br><br>{user_msg}<br><br>' \
                   f'<b>История действий пользователя</b>' \
                   f'<br><br>{user_actions}<br><br>'
            if message == 'request':
                msg['Subject'] = f'📮 Новая заявка с бота от @{username}'
            elif message == 'brif_list':
                msg['Subject'] = f'Пользователь @{username} заполнил бриф 📜'
            elif message == 'black_list':
                msg['Subject'] = f'⚫️ Пользователь @{username} загремел в черный список ⚫️'

        msg.attach(MIMEText(body, 'html'))
        # Создаю видимость печати пока загружаются данные
        typing(update, context)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(login, password)
        print("Отправка письма...")

        server.send_message(msg)
        server.quit()

        if message != 'new_user' and message != 'black_list':
            post_ban_list.update({username: [1, time.strftime("%x-%X", time.localtime())]})
            JSONFile(f'./post/logs/POST_BAN.json', post_ban_list)

        print('\x1b[6;30;42m' + 'Email successfully sent' + '\x1b[0m')
        return 'Отправил заявку на почту разработчика ✅'
    elif post_ban_list.get(username)[0] == 1:
        print(f'Попытка спама {username}')
        plus_post_bun(post_ban_list, username)
        return 'Ты уже отправлял заявку сегодня'

    elif post_ban_list.get(username)[0] == 2:
        print(f'Попытка спама {username}')
        sti = open('static/stickers/yyyyy.webp', 'rb')
        send_sticker(update, context, sti)
        plus_post_bun(post_ban_list, username)
        return 'Я же сказал, что ты уже отправлял сегодня заявку 🤨\n' \
               'Повторную заявку можно отправить только через 24 часа'

    elif post_ban_list.get(username)[0] == 3:
        print(f'Попытка спама {username}')
        plus_post_bun(post_ban_list, username)
        return 'Так, еще раз и в черный список 😑'

    elif post_ban_list.get(username)[0] == 4:
        print(f'Занесение в черный список пользователя {username}')
        sti = open('static/stickers/FUUUUCK.webp', 'rb')
        send_sticker(update, context, sti)
        update.message.reply_text(
            text='ЧЕРТ! МЕНЯ ДВАЖДЫ ПРОСИТЬ НЕ НУЖНО!',
            reply_markup=ReplyKeyboardRemove(),
        )

        # Удаляю из списка суточного почтового бана
        post_ban_list.pop(username)
        JSONFile(f'./post/logs/POST_BAN.json', post_ban_list)

        # Создаю видимость печати пока загружаются данные
        typing(update, context)
        send_to_black_list(username, update, context)
        return 'Я обиделся на тебя и добавляю тебя в черный список 😡'
