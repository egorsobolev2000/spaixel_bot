import os
import re
import json
import datetime


def createJSONFile(update):
    d = datetime.datetime.today()

    data = {
        "username": str(update.from_user.username),
        "first_name": str(update.from_user.first_name),
        "last_name": str(update.from_user.last_name),
        "language_code": str(update.from_user.language_code),
    }

    with open(f'./post/logs/{update.from_user.username}${d}.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=2)


def message_collector(update):
    username = update.from_user.username
    # name.split('$')[0]
    logs = os.listdir('./post/logs/')
    if len(logs) == 0:
        print('Создается файл')
        createJSONFile(update)
    else:
        for f in logs:
            if f.split('$')[0] == username:
                print('Файл уже был создан')
            elif f.split('$')[0] != username:
                print('Создается файл')
                createJSONFile(update)

