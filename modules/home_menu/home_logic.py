from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from .home_menu_btn import *


def get_base_inline_keyboard():
    """ Получить клавиатуру для сообщения
        Клавиатура будет видна ПОД каждым сообщением, где ее прикрепили
    """
    # Каждый список внутри "keyboard" -- это один горизонтальный ряд кнопок

    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец
        # Сколько кнопок столько и столбцов

        [
            InlineKeyboardButton(MAIN_INLINE_BUTTON[CB_B_BRIF_LIST], callback_data=CB_B_BRIF_LIST),
            InlineKeyboardButton(MAIN_INLINE_BUTTON[CB_B_SERVICES], callback_data=CB_B_SERVICES),
        ],

        [
            InlineKeyboardButton(MAIN_INLINE_BUTTON[CB_B_FAQ], callback_data=CB_B_FAQ),
        ],
        [
            InlineKeyboardButton(text="💭 Отзывы", url="https://vk.com/topic-157919190_41216100"),
            InlineKeyboardButton(text="🖥 Перейти на сайт", url="https://vk.com/spaixel"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_main_inline_menu(update):
    """ Функция отправляет пользователю сообщение
    с прикрепленным главным меню """
    update.message.reply_text(
        text='Услуги и их описание с которыми можно ознакомиться 👇',
        reply_markup=get_base_inline_keyboard(),
    )