import random
import telebot
import conf
import shelvehandler
from sqlhandler import SqlHandler

bot = telebot.TeleBot(conf.token)


@bot.message_handler(commands=['game'])
def game(message):
    db_worker = SqlHandler(conf.db)
    get_random_song = db_worker.select_single_row(random.randint(1, shelvehandler.get_rows_count()))
    bot.send_voice(message.chat.id, get_random_song[1])
    shelvehandler.start_user_game(message.chat.id, get_random_song[2])


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = shelvehandler.get_answer_for_user(message.chat.id)
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button = telebot.types.InlineKeyboardButton('Play 🤔', callback_data='game')
    markup.add(button)
    if not answer:
        bot.send_message(message.chat.id, 'To start a GuessMelodyGame, '
                                          'enter: /game, or press the button',
                         reply_markup=markup)
    else:
        if message.text.lower() == answer.lower():
            bot.send_message(message.chat.id, 'You are right! 🥳', reply_markup=markup)
        else:

            bot.send_message(message.chat.id, 'Wrong answer, play again! 🙈', reply_markup=markup)
        shelvehandler.end_user_game(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'game':
            game(call.message)


if __name__ == '__main__':
    shelvehandler.count_db_rows()
    bot.polling(none_stop=True)
