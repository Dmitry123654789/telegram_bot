from json import loads
from random import choice

from telegram.ext import Application, CommandHandler, filters, MessageHandler

from config import BOT_TOKEN

QUESTIONS = {}
GAME = False

user_questions = {}
last_questions = ''


async def start(update, context):
    if QUESTIONS:
        await update.message.reply_text('''Хотите ли вы пройти опрос?\n/yes Да\n/no нет''')


async def yes(update, context):
    global GAME, user_questions, last_questions
    GAME = True
    res = choice(list(list(QUESTIONS.keys())))
    user_questions = {res: ''}
    last_questions = res
    await update.message.reply_text("Первый вопрос")
    await update.message.reply_text(res)


async def no(update, context):
    await update.message.reply_text("Ну и ладно")


async def stop(update, context):
    global GAME
    GAME = False
    await update.message.reply_text("Игра прервана")


async def load_question(update, context):
    global last_questions, user_questions, GAME, QUESTIONS
    if not GAME:
        try:
            for res in loads(update.message.text)['test']:
                QUESTIONS[res['question']] = res['response']
            return await update.message.reply_text("Вопросы записаны")
        except Exception as e:
            return await update.message.reply_text(f"Вопросы не записаны\nКод ошибки {str(e)}")

    user_questions[last_questions] = update.message.text.strip()
    if len(user_questions) == len(list(QUESTIONS.keys())) or len(user_questions) == 10:
        GAME = False
        count_true_answer = len([ansew for key, ansew in user_questions.items() if ansew == QUESTIONS[key]])
        await update.message.reply_text(
            f"Всего вопросов в тесте было {len(user_questions)}\nПравильный ответов {count_true_answer}")
        return await update.message.reply_text(f"Хотите пройти тест снова?\n/yes Да\n/no нет")

    res = choice(list(QUESTIONS.keys()))
    while res in user_questions.keys():
        res = choice(list(QUESTIONS.keys()))
    user_questions[res] = ''
    last_questions = res
    await update.message.reply_text(res)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("yes", yes))
    application.add_handler(CommandHandler("no", no))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, load_question))

    application.run_polling()


if __name__ == '__main__':
    main()
