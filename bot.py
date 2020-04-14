import os
import conf
from telegram import Bot

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent

from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import InlineQueryHandler
from telegram.utils.request import Request
from inline.search import Searcher, regex

from colors import ColorsPrint
from bot_logic import *
from post.collect_data import info_collector
from modules.home_menu.home_logic import get_main_inline_menu
from modules.keyboard.keyboard_logic import get_base_keyboard_btns
from post.collect_data import JSONFile

search = Searcher()


@log_error
def inline_handler(update: Update, context: CallbackContext):
    """ Функкия логики и доступности Inline режима """

    users = JSONFile('./inline/inline_user.json', d_or_l='load')
    user = update.inline_query.from_user.username

    # Проверка -> Должен ли этот пользователь вызывать Inline режим
    if user in users.get('users'):
        query = update.inline_query.query
        query = query.strip().lower()
        # Очистка запроса от мусора
        query = regex.sub('', query)

        results = []
        titles = search.parse_query(query)

        # Выводить список только когда пользователь начал
        # что-то печатать (не вываливает огромный список вариантов)
        if query != '':
            for i, title in enumerate(titles):
                results.append(
                    InlineQueryResultArticle(
                        id=i + 1,
                        title=f'{title} - использовать?',
                        input_message_content=InputTextMessageContent(
                            message_text=search.get_answer(title),
                            parse_mode=ParseMode.HTML,
                        ),
                    )
                )

        # Ничего не нашлось
        if query and not results:
            results.append(
                InlineQueryResultArticle(
                    id=999,
                    title='Ничего не нашлось',
                    input_message_content=InputTextMessageContent(
                        message_text=f'Ничего не нашлось по запросу "{query}"',
                    ),
                )
            )

        update.inline_query.answer(
            results=results,
            cache_time=10,
        )


@log_error
def do_start(update: Update, context: CallbackContext):
    sti = open('static/stickers/hello.tgs', 'rb')
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
    # Создаю видимость печати пока загружаются данные
    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id,
        action=ChatAction.TYPING
    )
    update.message.reply_text(
        text=f"Привет, {update.message.chat.first_name}! 👋\nЯ <b>{context.bot.get_me().first_name}</b>.\nС радостью отвечу "
             f"на твои вопросы.",
        reply_markup=get_base_keyboard_btns(),
        parse_mode=ParseMode.HTML,
    )

    # Прикрепил к приветственному сообщению главное меню
    get_main_inline_menu(update)
    info_collector(update.message)
    print(f'Обработка команды `/start` — ', ColorsPrint('OK', 'suc').do_colored())


@log_error
def do_echo(update: Update, context: CallbackContext):
    # Вызываю обработчик всех возможных введенных ключевых слов с клавиатуры
    keyboard_btns_handler(update, context)
    info_collector(update.message)


@log_error
def do_help(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Здесь будет информация о боте",
    )
    print(f'Обработка команды `/help` — ', ColorsPrint('OK', 'suc').do_colored())


@log_error
def main():
    req = Request(
        connect_timeout=0.5,
    )
    bot = Bot(
        request=req,
        token=conf.TOKEN,
        # base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    os.system('clear')
    print(ColorsPrint('Запускаем бота...', 'att').do_colored())
    print(f'\nСоединение с {bot.get_me().first_name} — ', ColorsPrint('OK', 'suc').do_colored())

    # Обработчики команд
    dp = updater.dispatcher

    dp.add_handler(InlineQueryHandler(inline_handler))
    dp.add_handler(CommandHandler("start", do_start))
    dp.add_handler(CommandHandler("help", do_help))
    dp.add_handler(MessageHandler(Filters.text, do_echo))
    dp.add_handler(CallbackQueryHandler(callback=main_callback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
