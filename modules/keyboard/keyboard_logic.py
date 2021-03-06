from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from .keyboard_btn import *


def get_base_keyboard_btns():
    """ Добавляет клавиатуру бота """
    keyboard = [
        [
            KeyboardButton(GET_MAIN_BOT_MENU),
        ],
        [
            KeyboardButton(MANAGER_MESSAGE),
        ],
        [
            KeyboardButton(CONTACT_LEFT),
            KeyboardButton(REQ_BTN),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def get_back_keyboard():
    keyboard = [
        [
            KeyboardButton(BACK),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )