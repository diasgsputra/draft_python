import mysql.connector
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
    cursor = mydb.cursor()
    #cursor.execute("SELECT id, id_alat, waktu, t, h, ldr, hujan, ch FROM loghujan WHERE id_alat = 'C001' AND waktu LIKE '%00'")
    cursor.execute("SELECT * FROM loghujan WHERE id_alat = 'C001' AND waktu LIKE '%00'")
    #workbook = Workbook('outfile.xlsx')
    #sheet = workbook.add_worksheet()
    #for r, row in enumerate(cursor.fetchall()):
    #    for c, col in enumerate(row):
    #        sheet.write(r, c, col)

    with open('outfile3.csv','w') as f:
        writer = csv.writer(f)
        for row in cursor.fetchall():
            writer.writerow(row)



