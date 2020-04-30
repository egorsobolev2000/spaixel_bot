from post.collect_data import JSONFile
from .admin_keyboard.admin_keyboard_logic import get_admin_keyboard_btns


def admin(func):
    """ Функция ДЕКОРАТОР которая проверяет является
        ли человек админом и если ДА включает
        режим администратора """

    def wrapped(update, context):
        admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')
        if update.effective_user.username in admin_file['users']:
            admin_file['status'] = 'ON'
            JSONFile('./modules/admin/admin.json', admin_file)
            return func(update, context)
        else:
            update.message.reply_text(
                text='Нет прав для использования этой команды'
            )
    return wrapped


def admin_logic(update, context):
    update.message.reply_text(
        text='Приветствую в режиме администратора.\n'
             'Что будем делать?',
        reply_markup=get_admin_keyboard_btns()
    )


def admin_logout(update, context):
    """ Функция завершает использование режима админа """
    admin_file = JSONFile('./modules/admin/admin.json', d_or_l='load')
    admin_file['status'] = 'OFF'
    JSONFile('./modules/admin/admin.json', admin_file)


def list_convector(lst):
    """ Функция конвертирует список в строку и в столбец """
    user_list = ''
    for n, user in enumerate(lst, 1):
        user_list += f'{n}. {user}\n'
    return user_list

