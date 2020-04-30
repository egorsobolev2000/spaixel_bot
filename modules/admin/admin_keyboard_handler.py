from telegram import ParseMode
from telegram import ReplyKeyboardRemove

from post.collect_data import JSONFile
from post.sendPost import send_to_black_list
from .admin_keyboard import admin_keyboard_btns as akbb
from .admin_logic import list_convector, admin_logout
from ..keyboard.keyboard_logic import get_base_keyboard_btns


def remove_from_admins(update, context, username, admin_file):
    """ Функция удаляет пользователя из списка админов"""

    admin_file['users'].remove(username)
    JSONFile('./modules/admin/admin.json', admin_file)


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
                 f'Всего пользователей — {len(all_user_list["users"])}\n'
                 f'В черном списке — {len(black_list.keys())}\n',
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
        admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')
        user_list = list_convector(admin_file['users'])
        update.message.reply_text(
            text='<em><b>Администраторы сейчас:</b></em>\n\n'
                 f'{user_list}',
            parse_mode=ParseMode.HTML,
        )

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
                 'Пришли сообщение в таком формате ``` @unban username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Сделать админом пользователя
    elif update.message.text == akbb.DO_VIP_USER:
        update.message.reply_text(
            text='Какого пользователя назначить администратором?\n'
                 'Пришли сообщение в таком формате ``` @admin username ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Удалить админа
    elif update.message.text == akbb.DEL_VIP_USER:
        update.message.reply_text(
            text='Какого пользователя удалить администраторов?\n'
                 'Пришли сообщение в таком формате ``` @lower username ```',
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
    # 👇 Обработка ответов при специфических командах 👇
    # --------------------------------------------------------------

    elif update.message.text[0] == '@':
        msg = update.message.text.split()
        admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')

        if msg[0][1:] == 'ban':
            if msg[1] == 'sobolev_eg':
                try_me_ban(update, context, update.effective_user.username)
                remove_from_admins(update, context, update.effective_user.username, admin_file)
                # Завершаю сеанс администратора
                admin_logout(update, context)
            else:
                try:
                    if msg[1] in admin_file['users']:
                        remove_from_admins(update, context, msg[1], admin_file)
                        update.message.reply_text(
                            text='Понял, забираю у него права администратора'
                        )

                    # Записую пользователя в ЧС
                    send_to_black_list(msg[1], update, context)

                    update.message.reply_text(
                        text='Записую его в список гандонов'
                    )
                except Exception as e:
                    update.message.reply_text(
                        text=f'Не удалось заблокировать пользователя\n'
                             f'Ошибка: {e}',
                    )

        elif msg[0][1:] == 'unban':
            user_ban_list = JSONFile('./post/BLACK_LIST.json', d_or_l='load')
            user_ban_list.pop(msg[1])
            JSONFile('./post/BLACK_LIST.json', user_ban_list)

            user_list = JSONFile(f'./post/logs/USERS.json', d_or_l='load')
            user_list['users'].append(msg[1])
            JSONFile(f'./post/logs/USERS.json', user_list)

            update.message.reply_text(
                text='Хорошо, достал его в списка гандонов'
            )

        elif msg[0][1:] == 'admin':
            try:
                # Записую нового админа в список
                admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')
                admin_file['users'].append(msg[1])
                JSONFile('./modules/admin/admin.json', admin_file)

                update.message.reply_text(
                    text=f'Пользователь @{msg[1]} теперь имеет права администратора',
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                update.message.reply_text(
                    text=f'Не удалось добавить администратора\n'
                         f'Ошибка: {e}',
                )

        elif msg[0][1:] == 'lower':
            admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')

            if msg[1] == 'sobolev_eg':
                try_me_ban(update, context, update.effective_user.username)
                remove_from_admins(update, context, update.effective_user.username, admin_file)
                # Завершаю сеанс администратора
                admin_logout(update, context)
            else:
                try:
                    # Удаляю админа из списка
                    remove_from_admins(update, context, update.effective_user.username, admin_file)
                    update.message.reply_text(
                        text=f'Пользователь @{msg[1]} теперь не имеет прав администратора',
                        parse_mode=ParseMode.HTML
                    )
                except Exception as e:
                    update.message.reply_text(
                        text=f'Не удалось удалить администратора\n'
                             f'Ошибка: {e}',
                    )

