from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
import telegram
import os
import gdbm
import answer

TG_TOKEN = os.environ['TG_TOKEN']

updater = Updater(TG_TOKEN)


def adminCommand(bot, update):
    pass

def startCommand(bot, update):
    text = """
        Hi! Nice to meet you!
        To get random music genre press /random
    """
    bot.send_message(
        chat_id=update.message.chat_id, 
        text='To get random music genre press /random',
        )

def helpCommand(bot,update):
    text = """
        Commands:\n\nTo get random music genre enter /random\n\nTo assess the genre press ❤️❤️❤️🖤🖤
    """
    bot.send_message(
        chat_id = update.message.chat_id, 
        text = text,
        parse_mode='HTML'
        )
    return None

def randomCommand(bot, update):
    genre = gdbm.get_random_genre(update.message.chat_id)
    current_answer = answer.generate_cart(genre)
    keyboard = answer.generate_keyboard(genre, update.message.chat_id)
    bot.send_message(
        chat_id=update.message.chat_id, 
        text = current_answer,
        reply_markup = keyboard,
        disable_web_page_preview = True,
        parse_mode='HTML'
        )
    return None

def scoreCommand(bot, update):
    query = update.callback_query
    data = query.data
    data = data.split('|')
    genre = gdbm.change_score(data)
    current_answer = answer.generate_cart(genre)
    keyboard = answer.generate_keyboard(genre, data[2])
    query.edit_message_text(
        text = current_answer,
        disable_web_page_preview = True,
        reply_markup = keyboard,
        parse_mode='HTML'
        )
    return None


start_command_handler = CommandHandler('start', startCommand)
help_command_handler = CommandHandler('help', helpCommand)
random_command_handler = CommandHandler('random', randomCommand)
admin_command_handler = CommandHandler('admin', adminCommand)
score_handler = CallbackQueryHandler(callback = scoreCommand)

updater.dispatcher.add_handler(start_command_handler)
updater.dispatcher.add_handler(random_command_handler)
updater.dispatcher.add_handler(help_command_handler)
updater.dispatcher.add_handler(admin_command_handler)
updater.dispatcher.add_handler(score_handler)

updater.start_polling(clean=True)

updater.idle()