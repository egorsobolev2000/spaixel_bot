from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from .admin_keyboard_btns import *


def get_admin_keyboard_btns():
    """ Добавляет админскую клавиатуру бота """
    keyboard = [
        [
            KeyboardButton(WATCH_USER_LIST),
        ],
        [
            KeyboardButton(WATCH_ADMIN_LIST),
            KeyboardButton(WATCH_BLACK_LIST),
        ],
        [
            KeyboardButton(GET_USER_FROM_B_L),
            KeyboardButton(SEND_USER_TO_B_L),
        ],
        [
            KeyboardButton(DO_VIP_USER),
            KeyboardButton(DEL_VIP_USER),
        ],
        [
            KeyboardButton(BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
