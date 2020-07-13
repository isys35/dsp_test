import telebot
import config
import db
import requests
import cv2

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
    check_photo(photo_url)


def check_photo(photo_url):
    file_name = photo_url.split('/')[-1]
    resp = requests.get(photo_url)
    image_path = f"photo/{file_name}"
    with open(image_path, 'wb') as photo_file:
        photo_file.write(resp.content)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10)
    )
    print(faces)


if __name__ == '__main__':
    bot.polling(timeout=1)