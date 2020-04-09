from .faq_btn import *

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def get_faq_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(FAQ[C_B_FAQ_Q1][0], callback_data=C_B_FAQ_Q1),
        ],

        [
            InlineKeyboardButton(FAQ[C_B_FAQ_Q2][0], callback_data=C_B_FAQ_Q2),
        ],
        [
            InlineKeyboardButton(FAQ[C_B_FAQ_Q3][0], callback_data=C_B_FAQ_Q3),
        ],
        [
            InlineKeyboardButton(FAQ[C_B_FAQ_Q4][0], callback_data=C_B_FAQ_Q4),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

