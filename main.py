from datetime import datetime

from telegram.ext import CommandHandler, Application

BOT_TOKEN = 'Token'


async def date(update, context):
    """Отправляет сообщение когда получена команда /date"""
    await update.message.reply_text(f'Текущая дата {datetime.today().strftime('%d.%m.%Y')}')


async def time(update, context):
    """Отправляет сообщение когда получена команда /time"""
    await update.message.reply_text(f'Текущее время {datetime.today().strftime('%H:%M:%S')}')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("date", date))
    application.add_handler(CommandHandler("time", time))
    application.run_polling()


if __name__ == '__main__':
    main()
