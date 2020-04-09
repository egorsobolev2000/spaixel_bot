from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from .brif_btn import *


def create_brif_list_keyboard(type_, next_q='',):
    """ Создает Inline кнопку для перехода к след. вопросу"""

    if type_ == 'next':
        keyboard = [
            [
                KeyboardButton(next_q),
            ],
            [
                KeyboardButton(ABORT_FILLING),
            ],
        ]

    elif type_ == 'finish':
        keyboard = [
            [
                KeyboardButton(FINISH),
            ],
            [
                KeyboardButton(ABORT_FILLING),
            ],
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def get_brif_list_inline_keyboard():
    """ Получить клавиатуру для сообщения
        Клавиатура будет видна ПОД каждым сообщением, где ее прикрепили
    """
    # Каждый список внутри "keyboard" -- это один горизонтальный ряд кнопок

    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец
        # Сколько кнопок столько и столбцов

        [
            InlineKeyboardButton(BRIF_TITLES[CB_B_ONLINE_PAYMENT], callback_data=CB_B_ONLINE_PAYMENT),
            InlineKeyboardButton(BRIF_TITLES[CB_B_INTERACTIVE_MAP], callback_data=CB_B_INTERACTIVE_MAP),
        ],

        [
            InlineKeyboardButton(BRIF_TITLES[CB_B_CITY_DEFINITION], callback_data=CB_B_CITY_DEFINITION),
            InlineKeyboardButton(BRIF_TITLES[CB_B_SLIDERS], callback_data=CB_B_SLIDERS),
        ],
        [
            InlineKeyboardButton(BRIF_TITLES[CB_B_SITE_EARCH], callback_data=CB_B_SITE_EARCH),
            InlineKeyboardButton(BRIF_TITLES[CB_B_SUBSCRIPTION], callback_data=CB_B_SUBSCRIPTION),
        ],
        [
            InlineKeyboardButton(BRIF_TITLES[CB_B_PERSONAL_AREA], callback_data=CB_B_PERSONAL_AREA),
            InlineKeyboardButton(BRIF_TITLES[CB_B_COST_CALCULATOR], callback_data=CB_B_COST_CALCULATOR),
        ],
        [
            InlineKeyboardButton(BRIF_TITLES[CB_B_NEWS_BLOG], callback_data=CB_B_NEWS_BLOG),
            InlineKeyboardButton(BRIF_TITLES[CB_B_REVIEWS], callback_data=CB_B_REVIEWS),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

