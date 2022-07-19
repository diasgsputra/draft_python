import mysql.connector
import time

class koneksi :
    
    while True :

        mydb = mysql.connector.connect(
            host="103.102.153.194",
            user="db_dan",
            password="dan1313",
            database="db_dan"
        )
    
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, id_alat, waktu, t, h, ldr, hujan, ch FROM loghujan WHERE id_alat = 'C001' ORDER BY id DESC LIMIT 1")
        myresult = mycursor.fetchone()

        print(myresult)
        
        time.sleep(1)
