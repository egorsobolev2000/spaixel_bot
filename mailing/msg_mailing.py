import os

from colors import ColorsPrint


def start_mailing(status, context, mailing_text):
    if status:
        from post.collect_data import JSONFile
        logs = os.listdir('./post/logs/')
        black_list = JSONFile(f'./post/BLACK_LIST.json', d_or_l='load')
        print('-' * 20)
        print(ColorsPrint('Начинаю рассылку\n', "inf").do_colored())
        print('-' * 20)

        # кол-во успешных рассылок
        sd = 0
        # кол-во щаблокированных пользователей
        bu = 0

        for file in logs:
            if file != 'USERS.json' and file != 'POST_BAN.json':
                try:
                    data = JSONFile(f'./post/logs/{file}', d_or_l='load')
                    # Проверка, нет ли этого пользователя в черном списке
                    if data['username'] not in black_list.keys():
                        chat_id = data['chat_id']
                        context.bot.send_message(
                            chat_id=chat_id,
                            text=mailing_text,
                        )
                        print(f"Доставка пользователю {file.split('$')[0]} — ", ColorsPrint("OK", "suc").do_colored())
                        print('-' * 20)
                        sd += 1
                    else:
                        bu += 1
                except Exception as e:
                    print(f"Доставка пользователю {file.split('$')[0]} — ", ColorsPrint("Ошибка", "err").do_colored(),
                          f'{e}')
                    print('-' * 20)
        print(ColorsPrint("\nРассылка успешно завершена", "inf").do_colored())

        return sd, str(len(logs) - (2 + bu)), bu
