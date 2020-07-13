import sqlite3
import config
import os
import requests
from pydub import AudioSegment
import cv2


def create_db():
    file = open(config.DB_NAME, 'wb')
    file.close()
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE audio 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            path TEXT,
            user_id INTEGER)""")
    cursor.execute("""CREATE TABLE photo 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            path TEXT,
            user_id INTEGER)""")
    if not os.path.exists('audio'):
        os.mkdir('audio')
    if not os.path.exists('photo'):
        os.mkdir('photo')
    cursor.close()
    conn.close()


def add_audio(audio_url, user_id):
    file_name = audio_url.split('/')[-1]
    resp = requests.get(audio_url)
    with open(f"audio/{file_name}", 'wb') as audio_file:
        audio_file.write(resp.content)
    song = AudioSegment.from_file(f"audio/{file_name}", format=file_name.split('.')[1])
    song.set_frame_rate(16000)
    wav_file_name = 'audio/{}.wav'.format(file_name.split('.')[0])
    song.export(wav_file_name, format="wav")
    os.remove(file_name)
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    query = """INSERT INTO audio (path, user_id) VALUES (?, ?)"""
    cursor.execute(query, [wav_file_name, int(user_id)])
    conn.commit()
    cursor.close()
    conn.close()
    wav_sound = open(wav_file_name, 'rb')
    return wav_sound


def add_photo(photo_url, user_id):
    file_name = photo_url.split('/')[-1]
    resp = requests.get(photo_url)
    image_path = f"photo/{file_name}"
    with open(image_path, 'wb') as photo_file:
        photo_file.write(resp.content)
    if not check_photo(image_path):
        os.remove(image_path)
        return
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    query = """INSERT INTO photo (path, user_id) VALUES (?, ?)"""
    cursor.execute(query, [image_path, int(user_id)])
    conn.commit()
    cursor.close()
    conn.close()
    file_photo = open("photo_with_rectangle.jpg", 'rb')
    return file_photo


def check_photo(image_path):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10)
    )
    if len(faces) == 0:
        return False
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
    cv2.imwrite("photo_with_rectangle.jpg", image)
    return True


if __name__ == '__main__':
    create_db()
