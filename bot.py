import telebot
import config
import db

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Тестовый бот для DSP Labs')


@bot.message_handler(content_types=['audio'])
def save_audio(message):
    audio_url = "https://api.telegram.org/file/bot{}/{}".format(config.TOKEN,
                                                                bot.get_file(message.audio.file_id).file_path)
    user_id = message.from_user.id
    wav_file = db.add_audio(audio_url, user_id)
    bot.send_audio(message.chat.id, wav_file)


@bot.message_handler(content_types=['photo'])
def save_photo(message):
    photo_url = "https://api.telegram.org/file/bot{}/{}".format(config.TOKEN,
                                                                bot.get_file(message.photo[-1].file_id).file_path)
    user_id = message.from_user.id
    photo_with_rectangle = db.add_photo(photo_url, user_id)
    if not photo_with_rectangle:
        bot.send_message(message.chat.id, 'Лица не найдены')
    else:
        bot.send_photo(message.chat.id, photo_with_rectangle)


if __name__ == '__main__':
    bot.polling(timeout=1)