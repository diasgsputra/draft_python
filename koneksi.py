import mysql.connector
import time

class koneksi :
    def ambil_data(self):
        try:
            time.sleep(0.5)
            mydb = mysql.connector.connect(
                host="103.102.153.194",
                user="db_dan",
                password="dan1313",
                database="db_dan"
            )
    
            mycursor = mydb.cursor()
            mycursor.execute("SELECT h, t, ch FROM loghujan WHERE id_alat = 'C001' ORDER BY id DESC LIMIT 1")
            #mycursor.execute("SELECT * FROM loghujan WHERE id_alat = 'C001' ORDER BY id DESC LIMIT 1")
            myresult = mycursor.fetchone()
            return myresult
        except:
            print("ambil data gagal")
        
        
            
