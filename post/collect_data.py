import os
import json
import datetime

from post.sendPost import send


def JSONFile(path, data='data', d_or_l='dump'):
    """ Функция непосредственного вызова и
        работы с JSON файлом """

    if d_or_l == 'dump':
        with open(path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=3)

    if d_or_l == 'load':
        with open(path, "r") as read_file:
            load_data = json.load(read_file)
        return load_data


def writeJSONFile(update):
    """ Функция посредник -> создает
        шаблон JSON профиля пользователя """

    d = datetime.datetime.today()

    if update.from_user.username is None:
        update.from_user.username = f'anonymous{update.from_user.id}'

    data = {
        "username": str(update.from_user.username),
        "chat_id": str(update.from_user.id),
        "first_name": str(update.from_user.first_name),
        "last_name": str(update.from_user.last_name),
        "language_code": str(update.from_user.language_code),
        "messages": [{f'{d.hour}:{d.minute}:{d.second}': update.text}],
        "actions": [],
    }

    # Вызываю запись в JSON файл
    JSONFile(f'./post/logs/{update.from_user.username}${d}.json', data)


def editJSONFile(username, key, value):
    """ Функция посредник -> редактирует
        шаблон JSON профиля пользователя """

    d = datetime.datetime.today()
    logs = os.listdir('./post/logs/')
    for file in logs:
        if file.split('$')[0] == username:
            data = JSONFile(f'./post/logs/{file}', d_or_l='load')
            data.get(key).append({f'{d.hour}:{d.minute}:{d.second}': value})
            # Вызываю запись в JSON файл
            JSONFile(f'./post/logs/{file}', data)
            break


def info_collector(update, context, m_or_a='m', data='data', full_update='full_update'):

    def action_controller(un):
        users = JSONFile('./post/logs/USERS.json', d_or_l='load')

        if un in users.get('users'):
            print('Пользователь уже был добавлен')
            if m_or_a == 'm':
                message = update.text
                editJSONFile(un, 'messages', message)
            elif m_or_a == 'a':
                action = data
                editJSONFile(un, 'actions', action)
        else:
            print(f'Создается файл для {username}')
            send(username, full_update, context)
            writeJSONFile(update)
            users.get('users').append(username)
            # Вызываю запись в JSON файл
            JSONFile('./post/logs/USERS.json', users)

    if m_or_a == 'a':
        username = update.username
        if username is None:
            username = f'anonymous{update.id}'
        action_controller(username)
    elif m_or_a == 'm':
        username = update.from_user.username
        if username is None:
            username = f'anonymous{update.from_user.id}'
        action_controller(username)

    print('------------------------------------------')
