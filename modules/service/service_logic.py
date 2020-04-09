from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from .service_btn import *


def get_service_inline_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(SERVICE_TITLE[CB_B_SITE_DEVELOPMENT], callback_data=CB_B_SITE_DEVELOPMENT),
        ],

        [
            InlineKeyboardButton(SERVICE_TITLE[CB_B_BOT_DEVELOPMENT], callback_data=CB_B_BOT_DEVELOPMENT),
        ],
        [
            InlineKeyboardButton(SERVICE_TITLE[CB_B_DESIGN_DEVELOPMENT], callback_data=CB_B_DESIGN_DEVELOPMENT),
        ],
        [
            InlineKeyboardButton(SERVICE_TITLE[CB_B_LOGO_DEVELOPMENT], callback_data=CB_B_LOGO_DEVELOPMENT),
        ],
        [
            InlineKeyboardButton(SERVICE_TITLE[CB_B_DESIGN_VK_GROUPS], callback_data=CB_B_DESIGN_VK_GROUPS),
        ],
        [
            InlineKeyboardButton(SERVICE_TITLE[CB_B_MARKETING], callback_data=CB_B_MARKETING),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

