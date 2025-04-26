from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN

room = {
    'enter': 'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб! И проходите в первый зал - Зал Афины',
    'exit': 'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!',
    1: 'В данном зале представлено искусство, посвящённое мудрости, войне и стратегии, вдохновлённое богиней Афиной.\n'
       'Из него вы можете:\n'
       '/room_2 пойти во 2 зал - Зал Посейдона,\n'
       '/exit выйти из музея',
    2: 'В данном зале представлено морское наследие Древней Греции и почитание бога морей Посейдона.\n'
       'Из него вы можнтн попасть:\n'
       '/room_3 3 зал - Зал Диониса',
    3: 'В данном зале представлено веселье, виноделие и театральные традиции под покровительством Диониса.\n'
       'Из него вы можнтн попасть:\n'
       '/room_1 1 зал - Зал Афины,\n'
       '/room_4 4 зал - Зал Аполлона',
    4: 'В данном зале представлено искусство, музыка и пророчества, связанные с богом света Аполлоном.\n'
       'Из него вы можетн попасть:\n'
       '/room_1 в 1 зал - Зал Афины'
}

base_keyboard = [['/enter']]
first_room = [['/exit', '/room_2', ]]
second_room = [['/room_3']]
third_room = [['/room_1', '/room_4']]
fourth_room = [['/room_1']]

base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)
first_room_markup = ReplyKeyboardMarkup(first_room, one_time_keyboard=False)
second_room_markup = ReplyKeyboardMarkup(second_room, one_time_keyboard=False)
third_room_markup = ReplyKeyboardMarkup(third_room, one_time_keyboard=False)
fourth_room_markup = ReplyKeyboardMarkup(fourth_room, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text('Привет! Я бот-экскурсовод! Предлагаю тебе отправиться в музей')
    await update.message.reply_text(
        "<blockquote><code>/room_{number}: перейти в зал номер{number}\n"
        "/exit: выйти из музея\n"
        "/enter: войти в музей</code></blockquote>",
        reply_markup=base_markup,
        parse_mode='HTML'
    )


async def enter(update, context):
    await update.message.reply_text(room['enter'], reply_markup=fourth_room_markup)


async def exit_musem(update, context):
    await update.message.reply_text(room['exit'], reply_markup=base_markup)


async def room_1(update, context):
    await update.message.reply_text(room[1], reply_markup=first_room_markup)


async def room_2(update, context):
    await update.message.reply_text(room[2], reply_markup=second_room_markup)


async def room_3(update, context):
    await update.message.reply_text(room[3], reply_markup=third_room_markup)


async def room_4(update, context):
    await update.message.reply_text(room[4], reply_markup=fourth_room_markup)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Старт
    application.add_handler(CommandHandler("start", start))

    # Переключение вход, выход
    application.add_handler(CommandHandler("enter", enter))
    application.add_handler(CommandHandler("exit", exit_musem))

    # Перейти в комноту 1, 2, 3, 4
    application.add_handler(CommandHandler("room_1", room_1))
    application.add_handler(CommandHandler("room_2", room_2))
    application.add_handler(CommandHandler("room_3", room_3))
    application.add_handler(CommandHandler("room_4", room_4))

    application.run_polling()


if __name__ == '__main__':
    main()
