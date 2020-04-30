import os

from colors import ColorsPrint


def remove_from_list(user_list, user):
    """ Функция удаляет пользователя
        из заданного списка """

    from post.collect_data import JSONFile
    user_list['users'].remove(user)
    JSONFile(f'./post/logs/USERS.json', user_list)


def start_mailing(status, context, mailing_text):
    if status:
        from post.collect_data import JSONFile
        logs = os.listdir('./post/logs/')
        black_list = JSONFile(f'./post/BLACK_LIST.json', d_or_l='load')
        user_list = JSONFile(f'./post/logs/USERS.json', d_or_l='load')
        print('-' * 20)
        print(ColorsPrint('Начинаю рассылку\n', "inf").do_colored())
        print('-' * 20)

        # кол-во успешных рассылок
        sd = 0

        for file in logs:
            if file != 'USERS.json' and file != 'POST_BAN.json':
                try:
                    data = JSONFile(f'./post/logs/{file}', d_or_l='load')
                    # Проверка, нет ли этого пользователя в черном списке
                    if data['username'] not in black_list.keys() \
                            and data['username'] in user_list['users']:
                        chat_id = data['chat_id']
                        context.bot.send_message(
                            chat_id=chat_id,
                            text=mailing_text,
                        )
                        print(f"Доставка пользователю {file.split('$')[0]} — ", ColorsPrint("OK", "suc").do_colored())
                        print('-' * 20)
                        sd += 1
                    elif data['username'] not in black_list.keys() \
                            and data['username'] not in user_list['users']:
                        pass
                    else:
                        try:
                            remove_from_list(user_list, file.split('$')[0])
                        except Exception:
                            pass

                except Exception as e:
                    print(f"Доставка пользователю {file.split('$')[0]} — ", ColorsPrint("Ошибка", "err").do_colored(),
                          f'{e}')
                    # Если пользователь недоступен удаляю его из списка пользователей
                    remove_from_list(user_list, file.split('$')[0])

                    print('-' * 20)
        print(ColorsPrint("\nРассылка успешно завершена", "inf").do_colored())

        ubl = JSONFile('./post/BLACK_LIST.json', d_or_l='load')
        ubl = len(ubl)
        return sd, str(len(logs) - (2 + ubl)), ubl
