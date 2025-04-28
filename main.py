from telegram.ext import Application, CommandHandler, filters, MessageHandler, ConversationHandler

from config import BOT_TOKEN

poem = '''Белеет парус одинокой
В тумане моря голубом!..
Что ищет он в стране далекой?
Как будто в бурях есть покой!'''.split('\n')

'''Что кинул он в краю родном?..
Играют волны — ветер свищет,
И мачта гнется и скрыпит...
Увы! он счастия не ищет
И не от счастия бежит!
Под ним струя светлей лазури,
Над ним луч солнца золотой…
А он, мятежный, просит бури,'''

COUNT = 0

async def start(update, context):
    global COUNT
    COUNT = 1
    await update.message.reply_text(poem[0])

async def stop(update, context):
    global COUNT
    await update.message.reply_text("Игра прервана")
    await update.message.reply_text("Что бы начать с начала введите /start")
    COUNT = len(poem)

async def suphler(update, context):
    await update.message.reply_text(poem[COUNT])

async def print_poem(update, context):
    global COUNT
    try:
        if update.message.text == poem[COUNT]:
            COUNT += 2
            if COUNT <= len(poem):
                await update.message.reply_text(poem[COUNT - 1])
            if COUNT >= len(poem):
                await update.message.reply_text('Я рад, что у нас получилось все рассказать\n'
                                                'Что бы начать с начала введите /start')
        else:
            await update.message.reply_text('Нет, не так')
            await suphler(update, context)
    except IndexError:
        await update.message.reply_text('Нет, не так')



def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("suphler", suphler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, print_poem))

    application.run_polling()


if __name__ == '__main__':
    main()
