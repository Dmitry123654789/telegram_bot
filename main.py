from requests import get
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, filters, MessageHandler

from config import BOT_TOKEN

translate_keyboard = [['/eng_to_rus', '/rus_to_eng']]
translate_markup = ReplyKeyboardMarkup(translate_keyboard, one_time_keyboard=False)


async def start(update, context):
    context.user_data['last_command'] = ''
    await update.message.reply_text('''Это Бот-переводчик
/eng_to_rus Перевести текст с английского на русский
/rus_to_eng перевести с русского на английский''', reply_markup=translate_markup)


async def translate_text(update, context):
    if context.user_data['last_command'] == 'rus_to_eng':
        lang = 'ru|en'
    elif context.user_data['last_command'] == 'eng_to_rus':
        lang = 'en|ru'
    else:
        return await update.message.reply_text('Что то пошло не так, попробуйте снова выбрать язык перевода')

    text = update.message.text
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": lang
    }
    response = get(url, params=params)
    if response.status_code == 200:
        await update.message.reply_text(response.json()['responseData']['translatedText'])
    else:
        await update.message.reply_text('Что-то пошло не так, попробуйте позже')


async def eng_to_rus(update, context):
    context.user_data['last_command'] = 'eng_to_rus'
    await update.message.reply_text('Введите текст на английском языке для перевода его на русский')


async def rus_to_eng(update, context):
    context.user_data['last_command'] = 'rus_to_eng'
    await update.message.reply_text('Введите текст на русском языке для перевода его на английский')


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("eng_to_rus", eng_to_rus))
    application.add_handler(CommandHandler("rus_to_eng", rus_to_eng))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

    application.run_polling()


if __name__ == '__main__':
    main()
