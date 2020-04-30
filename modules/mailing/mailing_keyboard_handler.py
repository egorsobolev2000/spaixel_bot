from telegram import ParseMode

from bot_logic import send_sticker
from post.collect_data import JSONFile

from ..mailing.msg_mailing import start_mailing
from ..mailing.mailing_logic import mailing_logout
from ..keyboard.keyboard_logic import get_base_keyboard_btns
from ..mailing.mailing_keyboard import mailing_keyboard_btns as mkbb


def mailing_keyboard_handler(update, context):
    if update.message.text == mkbb.PREP_MAILING_TEXT:
        update.message.reply_text(
            text='Хорошо, пришли мне текст будущей рассылки в таком формате'
                 '``` @mailing some_text ```',
            parse_mode=ParseMode.MARKDOWN
        )

    # Начать рассылку
    elif update.message.text == mkbb.DO_MAILING:
        # Отправка стикера
        sti = open('static/stickers/hmmm.tgs', 'rb')
        send_sticker(update, context, sti)

        update.message.reply_text(
            text='В какой город пошли Егор и Валентин в 2018 году, '
                 'в первый день когда приехали в Крым?',
        )

    # Проверка
    elif update.message.text.lower() == 'партенит':
        mailing_file = JSONFile('./modules/mailing/mailing.json', d_or_l='load')
        if mailing_file['text'] != "":
            sd, usr_l, ubl = start_mailing(True, context, mailing_file['text'])
            update.message.reply_text(
                text=f'Рассылка завершена\n\n'
                     f'Успешно доставленно — <em><b>{sd}</b></em>\n'
                     f'Из — <em><b>{usr_l}</b></em>\n'
                     f'В черном списке — <em><b>{ubl}</b></em>',
                parse_mode=ParseMode.HTML,
            )
        else:
            update.message.reply_text(
                text='Вначале введи текст рассылки',
            )

    # Выход из режима рассылки
    elif update.message.text == mkbb.BACK:
        mailing_logout()
        update.message.reply_text(
            text='Выход из режима рассылки',
            reply_markup=get_base_keyboard_btns()
        )

    elif update.message.text.split()[0] == '@mailing':
        msg = update.message.text.split()
        msg = msg[1:]
        mailing_text = ' '.join(msg)
        mailing_file = JSONFile('./modules/mailing/mailing.json', d_or_l='load')
        mailing_file['text'] = mailing_text
        JSONFile('./modules/mailing/mailing.json', mailing_file)
        update.message.reply_text(
            text='Угу, записал 🖊',
            reply_markup=get_base_keyboard_btns()
        )


