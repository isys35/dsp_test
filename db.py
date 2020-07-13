import sqlite3
import config
import os
import requests
from pydub import AudioSegment

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
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    query = """INSERT INTO audio (path, user_id) VALUES (?, ?)"""
    cursor.execute(query, [wav_file_name, int(user_id)])
    conn.commit()
    cursor.close()
    conn.close()
    wav_sound = open(wav_file_name, 'rb')
    return wav_sound


if __name__ == '__main__':
    create_db()
