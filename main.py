import sqlite3
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
import os
import pandas as pd
import csv
import telebot
from threading import *
from time import sleep,time

import database as db


token = 'bot api'
bot = telebot.TeleBot(token)
def delete(file):#удаляем созданный CSV файл
    os.remove(file)

data_b = 'book_database.db'

file_name = input("Введите название файла:")



t_1 = Thread(target=db.upload_to_database,args=(data_b,f'{file_name}.xlsx'))



def get_data_from_ean(text):
    strih_code = text
    data_base = sqlite3.connect(data_b)
    curs = data_base.cursor()
    curs.execute(f"SELECT * FROM books WHERE EAN = {strih_code} ")
    x = curs.fetchall()
    data_base.close()
    return x
def get_data_from_name(text):
    strih_code = text
    data_base = sqlite3.connect(data_b)
    curs = data_base.cursor()
    curs.execute(f"SELECT * FROM books WHERE book_name LIKE '{strih_code}%' ")
    x = curs.fetchall()
    data_base.close()
    return x

def send(id,text):
    bot.send_message(id,text)
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'D:/трихкод/'+file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    with open(src, 'rb') as new_file:
        inform = db.get_data_from_photo(new_file)
        for i in inform:
            formated_info = f"Название:{i[0]}\nЦена:{i[2]}\nАвтор:{i[1]}"
            send(message.chat.id,formated_info)
            new_file.close()
            os.remove('D:/трихкод/'+file_info.file_path)



@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет, {message.from_user.first_name}!Отправь мне фото штрихкода книги ил её название!!!"
    send(message.chat.id, mess)
    try:
        t_1.start()
    except:
        pass



@bot.message_handler(content_types=['text'])
def get_text(message):
    if '9' in message.text:
        inform = get_data_from_ean(message.text)
        for i in inform:
            if i[1] == '<не указано>':
                formated_info = f"Название:{i[0]}\nЦена:{i[2]}\nОстаток на складе:{i[4]}"
                send(message.chat.id, formated_info)
            else:
                formated_info = f"Название:{i[0]}\nЦена:{i[2]}\nАвтор:{i[1]}\nОстаток на складе:{i[4]}"
                send(message.chat.id, formated_info)
    else:
        inform = get_data_from_name(message.text)
        for i in inform:
            if i[1] == '<не указано>':
                formated_info = f"Название:{i[0]}\nЦена:{i[2]}\nОстаток на складе:{i[4]}"
                send(message.chat.id, formated_info)
            else:
                formated_info = f"Название:{i[0]}\nЦена:{i[2]}\nАвтор:{i[1]}\nОстаток на складе:{i[4]}"
                send(message.chat.id, formated_info)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        sleep(15)
