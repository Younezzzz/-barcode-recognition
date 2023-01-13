import sqlite3
import pandas as pd
import os
import csv
import time
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
data_b = 'book_database.db'



def upload_to_database(data_b,file_name):
    while True:

        data_xls = pd.read_excel(file_name, index_col=0)
        data_xls.to_csv('ррц.csv', encoding='utf-8')
        with open('ррц.csv', encoding='utf-8') as r_file:
            reader_object = csv.reader(r_file,delimiter=",")
            try:
                for row in reader_object:   #вывод всех данных из CSV файла в ввиде списков
                    connect = sqlite3.connect(data_b)
                    curs = connect.cursor()
                    curs.execute("""INSERT INTO books VALUES(?,?,?,?,?) """, row)
                    connect.commit()
                    connect.close()
            except:
                for row in reader_object:   #вывод всех данных из CSV файла в ввиде списков
                    connect = sqlite3.connect(data_b)
                    curs = connect.cursor()
                    curs.execute(f"""UPDATE books SET price={row[2]} where EAN = {row[3]}""")
                    curs.execute(f"""UPDATE books SET remainder={row[4]} where EAN = {row[3]}""")
                    connect.commit()
                    connect.close()
        os.remove('ррц.csv')
        print('update')
        time.sleep(3600)


def get_data_from_photo(photo):
    data_b = 'book_database.db'
    image = Image.open(photo).convert("RGBA")
    decoded = decode(image)
    strih_code = decoded[0].data.decode('utf-8')
    print(strih_code)
    data_base = sqlite3.connect(data_b)
    curs = data_base.cursor()
    curs.execute(f"SELECT * FROM books WHERE EAN = {strih_code} ")
    return curs.fetchall()




print(get_data_from_photo('штрих.jpg'))