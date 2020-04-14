from telegram import Update
from telegram import ParseMode
from telegram import ChatAction
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardRemove

from debug import log_error
from inline.data import INLINE_DATA
from modules.keyboard import keyboard_btn as kbb, keyboard_logic as kbl
from modules.home_menu.home_logic import get_main_inline_menu
from modules.home_menu.home_menu_btn import *
from modules.brif import brif_btn, brif_logic
from modules.faq import faq_btn as fb, faq_logic as fl
from modules.service import service_btn as sb, service_logic as sl
from post.collect_data import info_collector

brif_status_check = ['brif_status_OFF']


@log_error
def keyboard_btns_handler(update, context):
    """ Обработка запросов с клавиатуры
    бота + стандартный ответ бота """


# --------------------------------------------------------------
# 👇 Логика ответов бота для кнопок меню главной клавиатуры 👇
# --------------------------------------------------------------

    # Обращение к главному меню
    if update.message.text == kbb.GET_MAIN_BOT_MENU:
        get_main_inline_menu(update)

    # Если человек хочет связаться с менеджером
    elif update.message.text == kbb.MANAGER_MESSAGE:
        update.message.reply_text(
            text='@sobolev_eg',
            parse_mode=ParseMode.HTML,
        )

    # Если запрашивает контактные данные
    elif update.message.text == kbb.CONTACT_LEFT:
        update.message.reply_text(
            text=INLINE_DATA.get('Контакты'),
            parse_mode=ParseMode.HTML,
        )


# --------------------------------------------------------------
# 👇 Логика ответов бота при заполнении брифа 👇
# --------------------------------------------------------------

    # ВОПРОС №2
    elif update.message.text == brif_btn.Q_2:
        update.message.reply_text(
            text='<b>Выбери из предложенного списка какой функционал '
                 'необходим для твоего сайта или напиши свой вариант. </b>',
            reply_markup=brif_logic.get_brif_list_inline_keyboard(),
            parse_mode=ParseMode.HTML,
        )

        update.message.reply_text(
            text='Или напиши свой вариант и отправь его мне.',
            reply_markup=brif_logic.create_brif_list_keyboard('next', brif_btn.Q_3),
            parse_mode=ParseMode.HTML,
        )

    # ВОПРОС №3
    elif update.message.text == brif_btn.Q_3:
        update.message.reply_text(
            text='<b>Приведи пожалуйста примеры понравившихся сайтов, '
                 'если таких есть. </b>',
            reply_markup=brif_logic.create_brif_list_keyboard('next', brif_btn.Q_4),
            parse_mode=ParseMode.HTML,
        )

    # ВОПРОС №4
    elif update.message.text == brif_btn.Q_4:
        update.message.reply_text(
            text='<b> Есть ли у тебя разработанный фирменный стиль?</b>',
            reply_markup=brif_logic.create_brif_list_keyboard('next', brif_btn.Q_5),
            parse_mode=ParseMode.HTML,
        )

    # ВОПРОС №5
    elif update.message.text == brif_btn.Q_5:
        update.message.reply_text(
            text='<b>Желаемый бюджет проекта?</b>',
            reply_markup=brif_logic.create_brif_list_keyboard('next', brif_btn.LAST_Q_6),
            parse_mode=ParseMode.HTML,
        )

    # ВОПРОС №6
    elif update.message.text == brif_btn.LAST_Q_6:
        update.message.reply_text(
            text='<b>Необходима ли разработка логотипа?</b>',
            reply_markup=brif_logic.create_brif_list_keyboard('finish'),
            parse_mode=ParseMode.HTML,
        )

    # Если человек прерывает заполнение брифа
    elif update.message.text == brif_btn.ABORT_FILLING:
        sti = open('static/stickers/wtf.tgs', 'rb')
        # Создаю видимость печати пока загружаются данные
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id,
            action=ChatAction.TYPING
        )
        # Отправка стикера
        context.bot.send_sticker(
            chat_id=update.effective_message.chat_id,
            sticker=sti
        )
        update.message.reply_text(
            text='Заполнение брифа прервано...\n\n'
                 'Но я немного расстроился 😞\n',
            reply_markup=kbl.get_base_keyboard_btns(),
            parse_mode=ParseMode.HTML,
        )
        get_main_inline_menu(update)

    # Полное завершение заполнения брифа
    elif update.message.text == brif_btn.FINISH:
        # Выключение режима заполнения брифа
        brif_status_check[0] = 'brif_status_OFF'

        sti = open('static/stickers/not_bad.tgs', 'rb')
        # Создаю видимость печати пока загружаются данные
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id,
            action=ChatAction.TYPING
        )
        # Отправка стикера
        context.bot.send_sticker(
            chat_id=update.effective_message.chat_id,
            sticker=sti
        )
        update.message.reply_text(
            text='Поздравляю! Бриф-лист успешно заполнен!',
            reply_markup=kbl.get_base_keyboard_btns(),
            parse_mode=ParseMode.HTML,
        )
        get_main_inline_menu(update)


# --------------------------------------------------------------
# 👇 Логика ответов бота при отправки других пользовательских сообщений 👇
# --------------------------------------------------------------

    # Если человек хочет вернуться в главное меню
    elif update.message.text == kbb.BACK:
        update.message.reply_text(
            text="Возврат в <b>главное меню</b> ",
            reply_markup=kbl.get_base_keyboard_btns(),
            parse_mode=ParseMode.HTML,
        )

        # Вызов функции которая возвращает главное меню
        get_main_inline_menu(update)

    else:
        if brif_status_check[0] == 'brif_status_ON':
            pass
        else:
            update.message.reply_text(
                text='Не совсем понял твое сообщение... ☹️\n\n'
                     'Попробуй воспользоваться'
                     'подготовленными кнопками с <b>клавиатуры</b> или '
                     'функциями из <b>главного меню</b>',
                parse_mode=ParseMode.HTML,
            )


@log_error
def main_callback_handler(update: Update, context: CallbackContext):
    """ Обработчик ВСЕХ кнопок при заполнении БРИФА """

    query = update.callback_query
    data = query.data
    username = query.message.chat
    info_collector(username, 'a', data)

# --------------------------------------------------------------
# 👇 Логика ответов бота при работе с БРИФОМ 👇
# --------------------------------------------------------------

    if data == CB_B_BRIF_LIST:
        # Включение режима заполнения брифа
        brif_status_check[0] = 'brif_status_ON'

        context.bot.delete_message(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
        )

        context.bot.send_message(
            text='<em>Используйте кнопки ниже, для перехода к след. вопросу '
                 'или прерывания заполнения.</em>',
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )

        context.bot.send_message(
            text='<b>Напишите предварительную структуру сайта: основные разделы, '
                 'подразделы. Кратко опишите их функциональное назначение и '
                 'дайте характеристику содержание каждого из разделов.</b>',
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=brif_logic.create_brif_list_keyboard('next', brif_btn.Q_2),
            parse_mode=ParseMode.HTML,
        )


# --------------------------------------------------------------
# 👇 Логика ответов бота при работе с разделом УСЛУГИ 👇
# --------------------------------------------------------------

    elif data == CB_B_SERVICES:
        query.edit_message_text(
            text='Подготовил для тебя наш список услуг 😎',
            inline_message_id=update.callback_query.inline_message_id,
            reply_markup=sl.get_service_inline_keyboard(),
        )
        context.bot.send_message(
            text='Более подробно с услугами можно ознакомиться на нашем <a href="https://spaixel.com">сайте</a>',
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=kbl.get_back_keyboard(),
            parse_mode=ParseMode.HTML,
        )

    elif data == sb.CB_B_SITE_DEVELOPMENT \
            or data == sb.CB_B_BOT_DEVELOPMENT \
            or data == sb.CB_B_DESIGN_DEVELOPMENT \
            or data == sb.CB_B_LOGO_DEVELOPMENT \
            or data == sb.CB_B_DESIGN_VK_GROUPS \
            or data == sb.CB_B_MARKETING:

        context.bot.send_message(
            text=sb.SERVICE_INFO[sb.FIST_EX],
            chat_id=update.callback_query.message.chat_id,
        )

# --------------------------------------------------------------
# 👇 Логика ответов бота при работе с разделом FAQ 👇
# --------------------------------------------------------------

    # Первое сообщение при вызове раздела FAQ
    elif data == CB_B_FAQ:
        query.edit_message_text(
            text='Это вопросы которые нам задают чаще всего 👀',
            inline_message_id=update.callback_query.inline_message_id,
            reply_markup=fl.get_faq_inline_keyboard(),
        )
        context.bot.send_message(
            text='<em> Если ты не найдешь здесь ответа на свой вопрос,'
                 'ты всегда можешь обратиться к менеджеру или разработчику'
                 'в моем главном меню </em>',
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=kbl.get_back_keyboard(),
            parse_mode=ParseMode.HTML,
        )

    # FAQ №1
    elif data == fb.C_B_FAQ_Q1:
        context.bot.send_message(
            text=fb.FAQ[fb.C_B_FAQ_Q1][1],
            chat_id=update.callback_query.message.chat_id,
            reply_markup=fl.get_faq_inline_keyboard(),
            parse_mode=ParseMode.HTML,
        )

    # FAQ №2
    elif data == fb.C_B_FAQ_Q2:
        context.bot.send_message(
            text=fb.FAQ[fb.C_B_FAQ_Q2][1],
            chat_id=update.callback_query.message.chat_id,
            reply_markup=fl.get_faq_inline_keyboard(),
            parse_mode=ParseMode.HTML,
        )

    # FAQ №3
    elif data == fb.C_B_FAQ_Q3:
        context.bot.send_message(
            text=fb.FAQ[fb.C_B_FAQ_Q3][1],
            chat_id=update.callback_query.message.chat_id,
            reply_markup=fl.get_faq_inline_keyboard(),
            parse_mode=ParseMode.HTML,
        )

    # FAQ №4
    elif data == fb.C_B_FAQ_Q4:
        context.bot.send_message(
            text=fb.FAQ[fb.C_B_FAQ_Q4][1],
            chat_id=update.callback_query.message.chat_id,
            reply_markup=fl.get_faq_inline_keyboard(),
            parse_mode=ParseMode.HTML,
        )