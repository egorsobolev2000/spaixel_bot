from post.collect_data import JSONFile
from modules.mailing.mailing_keyboard.mailing_keyboard_logic import get_mailing_keyboard_btns


def mailing_user(func):
    """ Функция ДЕКОРАТОР которая проверяет доступна ли ему
        возможность делать рассылку и если ДА включает
        режим рассылки """

    def wrapped(update, context):
        mailing_file = JSONFile('./modules/mailing/mailing.json', d_or_l='load')
        if update.effective_user.username in mailing_file['users']:
            mailing_file['status'] = 'ON'
            JSONFile('./modules/mailing/mailing.json', mailing_file)
            return func(update, context)
        else:
            update.message.reply_text(
                text='Нет прав для использования этой команды'
            )

    return wrapped


def mailing_mode(update, context):
    update.message.reply_text(
        text='Приветствую в режиме рассылки.\n'
             'Что будем делать?',
        reply_markup=get_mailing_keyboard_btns()
    )


def mailing_logout():
    """ Функция завершает использование режима админа """
    mailing_file = JSONFile('./modules/mailing/mailing.json', d_or_l='load')
    mailing_file['status'] = 'OFF'
    JSONFile('./modules/mailing/mailing.json', mailing_file)