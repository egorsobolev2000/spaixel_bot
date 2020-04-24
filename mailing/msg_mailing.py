import os

from colors import ColorsPrint


def start_mailing(status, context, mailing_text):
    if status:
        from post.collect_data import JSONFile
        logs = os.listdir('./post/logs/')
        print('-' * 20)
        print(ColorsPrint('Начинаю рассылку\n', "inf").do_colored())
        print('-' * 20)
        for file in logs:
            if file != 'USERS.json' and file != 'POST_BAN.json':
                try:
                    data = JSONFile(f'./post/logs/{file}', d_or_l='load')
                    chat_id = data['chat_id']
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=mailing_text,
                    )
                    print(f"Доставка пользователю {file.split('$')[0]} — ", ColorsPrint("OK", "suc").do_colored())
                    print('-' * 20)

                except Exception as e:
                    print(f"Доставка пользователю {file.split('$')[0]} — ", ColorsPrint("Ошибка", "err").do_colored(),
                          f'\n {e}')
                    print('-' * 20)
        print(ColorsPrint("\nРассылка успешно завершена", "inf").do_colored())
