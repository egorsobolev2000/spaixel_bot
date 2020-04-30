from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from .mailing_keyboard_btns import *


def get_mailing_keyboard_btns():
    """ Добавляет админскую клавиатуру бота """
    keyboard = [
        [
            KeyboardButton(PREP_MAILING_TEXT),
        ],
        [
            KeyboardButton(DO_MAILING),
        ],
        [
            KeyboardButton(BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
