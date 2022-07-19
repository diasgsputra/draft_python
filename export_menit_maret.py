import mysql.connector
import xlwt

import time
import pyodbc
import pandas as pd
from xlsxwriter.workbook import Workbook
import csv

class koneksi :
    
    print("test 0")
    mydb = mysql.connector.connect(
        host="103.102.153.194",
        user="db_dan",
        password="dan1313",
        database="db_dan"
    )
    print("test 1")
    myCursor = mydb.cursor()
    #myCursor.execute("SELECT id, id_alat, waktu, t, h, ldr, hujan, ch FROM loghujan WHERE id_alat = 'C001' AND waktu LIKE '%00' AND waktu >= '2022-01-01'")
    myCursor.execute("SELECT * FROM loghujan WHERE id_alat = 'C001' AND waktu LIKE '%00' AND waktu >= '2021-12-01'")
    

    hasil = myCursor.fetchall()
    
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("hujan")
    index = 0
    for row in hasil:
        sheet1.write(index+1, 0, row[0])
        sheet1.write(index+1, 1, row[1])
        sheet1.write(index+1, 2, row[2])
        sheet1.write(index+1, 3, row[3])
        sheet1.write(index+1, 4, row[4])
        sheet1.write(index+1, 5, row[5])
        sheet1.write(index+1, 6, row[6])
        sheet1.write(index+1, 7, row[7])
        sheet1.write(index+1, 8, row[8])
        sheet1.write(index+1, 9, row[9])
        sheet1.write(index+1, 10, row[10])
        sheet1.write(index+1, 11, row[11])
        index +=1

    book.save("hujan_menit_2.xls")
