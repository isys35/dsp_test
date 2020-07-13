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
    song = AudioSegment.from_mp3(f"audio/{file_name}")
    song.export('audio/{}.wav'.format(file_name.split('.')[0]), format="wav")
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    query = """INSERT INTO audio (git path, user_id) VALUES (?, ?)"""
    cursor.execute(query, [f"audio/{file_name}", int(user_id)])
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_db()
