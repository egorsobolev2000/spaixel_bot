from telegram import ParseMode
from telegram import ReplyKeyboardRemove

from post.collect_data import JSONFile
from post.sendPost import send_to_black_list
from .admin_keyboard import admin_keyboard_btns as akbb
from .admin_logic import list_convector, admin_logout
from ..keyboard.keyboard_logic import get_base_keyboard_btns


def del_user(username, file):
    """ Функция удаляет пользователя из списка """

    user_file = JSONFile(file, d_or_l='load')
    user_file['users'].remove(username)
    JSONFile(file, user_file)


def add_user(username, file):
    """ Функция добавляет пользователя в список """

    user_file = JSONFile(file, d_or_l='load')
    user_file['users'].append(username)
    JSONFile(file, user_file)


def get_users_list(update, file, who='Администраторы'):
    user_file = JSONFile(file, d_or_l='load')
    user_list = list_convector(user_file['users'])
    update.message.reply_text(
        text=f'<em><b>{who} сейчас:</b></em>\n\n'
             f'{user_list}',
        parse_mode=ParseMode.HTML,
    )


def try_me_ban(update, context, username):
    """ Функция вызывается при попытке
        забанить главного админа """

    update.message.reply_text(
        text='Ах ты гандон, прочь с глаз',
        reply_markup=ReplyKeyboardRemove(),
    )
    # Записую пользователя в ЧС
    send_to_black_list(username, update, context)


def admin_keyboard_handler(update, context):
    """ Обработка всех запросов в режиме админа """

    # --------------------------------------------------------------
    # 👇 Обработка ответов на запросы с клавиатуры 👇
    # --------------------------------------------------------------

    # Посмотреть список пользователей бота
    if update.message.text == akbb.WATCH_USER_LIST:
        all_user_list = JSONFile('./post/logs/USERS.json', d_or_l='load')
        black_list = JSONFile(f'./post/BLACK_LIST.json', d_or_l='load')
        user_list = list_convector(all_user_list['users'])
        update.message.reply_text(
            text='<em><b>Список пользователей:</b></em>\n\n'
                 f'{user_list}\n\n'
                 f'<em><b>Всего пользователей</b></em> — {len(all_user_list["users"])}\n'
                 f'<em><b>В черном списке</b></em> — {len(black_list.keys())}\n',
            parse_mode=ParseMode.HTML,
        )

    # Посмотреть кто в черном списке
    elif update.message.text == akbb.WATCH_BLACK_LIST:
        user_ban_list = JSONFile('./post/BLACK_LIST.json', d_or_l='load')
        user_list = list_convector(user_ban_list.keys())
        update.message.reply_text(
            text='<em><b>В черном списке:</b></em>\n\n'
                 f'{user_list if user_list != "" else "В черном списке никого нет"}',
            parse_mode=ParseMode.HTML,
        )

    # Посмотреть кто сейчас имеет права админа
    elif update.message.text == akbb.WATCH_ADMIN_LIST:
        get_users_list(update, './modules/admin/admin.json', 'Администраторы')

    # Посмотреть кто сейчас имеет права модератора
    elif update.message.text == akbb.WATCH_MODERATOR_LIST:
        get_users_list(update, './modules/mailing/mailing.json', 'Модераторы')

    # Заблокировать кого-то
    elif update.message.text == akbb.SEND_USER_TO_B_L:
        update.message.reply_text(
            text='Какого пользователя заблокировать?\n'
                 'Пришли сообщение в таком формате ``` @ban username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Разблокировать кого-то
    elif update.message.text == akbb.GET_USER_FROM_B_L:
        update.message.reply_text(
            text='Какого пользователя разблокировать?\n'
                 'Пришли сообщение в таком формате: ``` @unban username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Сделать модератором кого-то
    elif update.message.text == akbb.ADD_MODERATOR:
        update.message.reply_text(
            text='Окей, какого пользователя назначить модератором?\n'
                 'Пришли сообщение в таком формате: ``` @amu username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Удалить модератора
    elif update.message.text == akbb.DEL_MODERATOR:
        update.message.reply_text(
            text='Окей, какого модератора удалить?\n'
                 'Пришли сообщение в таком формате: ``` @dmu username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Сделать админом пользователя
    elif update.message.text == akbb.DO_VIP_USER:
        update.message.reply_text(
            text='Какого пользователя назначить администратором?\n'
                 'Пришли сообщение в таком формате: ``` @admin username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Удалить админа
    elif update.message.text == akbb.DEL_VIP_USER:
        update.message.reply_text(
            text='Какого пользователя удалить администраторов?\n'
                 'Пришли сообщение в таком формате: ``` @lower username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Выход из режима админа
    elif update.message.text == akbb.BACK:
        admin_logout(update, context)
        update.message.reply_text(
            text='Выход из режима администратора',
            reply_markup=get_base_keyboard_btns()
        )

    # --------------------------------------------------------------
    # 👇 Обработка специфических командах 👇
    # --------------------------------------------------------------

    elif update.message.text[0] == '@':
        msg = update.message.text.split()
        if len(msg) > 1:
            admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')

            if msg[0][1:] == 'ban':
                if msg[1] == 'sobolev_eg':
                    try_me_ban(update, context, update.effective_user.username)
                    del_user(update.effective_user.username, './modules/admin/admin.json')
                    # Завершаю сеанс администратора
                    admin_logout(update, context)
                else:
                    try:
                        if msg[1] in admin_file['users']:
                            del_user(msg[1], './modules/admin/admin.json')
                            update.message.reply_text(
                                text='Понял, забираю у него права администратора'
                            )

                        # Записую пользователя в ЧС
                        send_to_black_list(msg[1], update, context)
                        del_user(msg[1], './post/logs/USERS.json')

                        update.message.reply_text(
                            text='Записую его в список гандонов'
                        )
                    except Exception as e:
                        update.message.reply_text(
                            text=f'Не удалось заблокировать пользователя\n'
                                 f'Ошибка: {e}',
                        )

            elif msg[0][1:] == 'unban':
                # Удаляю из ЧС
                user_ban_list = JSONFile('./post/BLACK_LIST.json', d_or_l='load')
                user_ban_list.pop(msg[1])
                JSONFile('./post/BLACK_LIST.json', user_ban_list)
                # Записую к обычным пользователям
                add_user(msg[1], './post/logs/USERS.json')

                update.message.reply_text(
                    text='Хорошо, достал его в списка гандонов'
                )

            elif msg[0][1:] == 'admin':
                try:
                    # Записую нового админа в список
                    admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')
                    if msg[1] not in admin_file['users']:
                        admin_file['users'].append(msg[1])
                        JSONFile('./modules/admin/admin.json', admin_file)

                        update.message.reply_text(
                            text=f'Пользователь @{msg[1]} теперь имеет права администратора',
                        )
                    elif msg[1] in admin_file['users']:
                        update.message.reply_text(
                            text=f'Пользователь @{msg[1]} уже имеет права администратора',
                        )

                except Exception as e:
                    update.message.reply_text(
                        text=f'Не удалось добавить администратора\n'
                             f'Ошибка: {e}',
                    )

            elif msg[0][1:] == 'lower':

                if msg[1] == 'sobolev_eg':
                    try_me_ban(update, context, update.effective_user.username)
                    del_user(update.effective_user.username, './modules/admin/admin.json')
                    # Завершаю сеанс администратора
                    admin_logout(update, context)
                else:
                    try:
                        # Удаляю админа из списка
                        del_user(msg[1], './modules/admin/admin.json')
                        update.message.reply_text(
                            text=f'Пользователь @{msg[1]} теперь не имеет прав администратора',
                            parse_mode=ParseMode.HTML
                        )
                    except Exception as e:
                        update.message.reply_text(
                            text=f'Не удалось удалить администратора\n'
                                 f'Ошибка: {e}',
                        )

            # Добавить модератора add_mailing_user -> amu
            elif msg[0][1:] == 'amu':
                mailing_file = JSONFile('./modules/mailing/mailing.json', d_or_l='load')
                if msg[1] not in mailing_file['users']:
                    add_user(msg[1], './modules/mailing/mailing.json')
                    update.message.reply_text(
                        text=f'Пользователь @{msg[1]} теперь имеет права модератора'
                    )

                elif msg[1] in mailing_file['users']:
                    update.message.reply_text(
                        text=f'Пользователь @{msg[1]} уже имеет права модератора',
                    )

            # Удалить модератора del_mailing_user -> dmu
            elif msg[0][1:] == 'dmu':
                mailing_file = JSONFile('./modules/mailing/mailing.json', d_or_l='load')
                if msg[1] in mailing_file['users']:
                    del_user(msg[1], './modules/mailing/mailing.json')
                    update.message.reply_text(
                        text=f'Забрал права модератора у @{msg[1]}'
                    )

                elif msg[1] not in mailing_file['users']:
                    update.message.reply_text(
                        text=f'Пользователь @{msg[1]} не имеет прав модератора',
                    )

        else:
            update.message.reply_text(text=f"Введена не верная команда")
