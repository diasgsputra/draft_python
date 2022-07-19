import mysql.connector
import time
import numpy as np

class koneksi :
    def ambil_data(self):
        try:
            data = np.zeros((60, 3))
            print(data)
            data_t = np.zeros((55,8))
            print(data_t)
            menit = 0;
    
            mydb = mysql.connector.connect(
                host="103.102.153.194",
                user="db_dan",
                password="dan1313",
                database="db_dan"
            )
    
            mycursor = mydb.cursor()
            while menit < 60:
                smenit = str(menit)
                mycursor.execute(
            
                    "SELECT h, t, ch FROM loghujan WHERE id_alat = 'C001' AND waktu = '2022-01-07 23:"+smenit+":00' "

                    )
                myresult = mycursor.fetchone()

                data[menit] = np.array(myresult)
                print(".", end = " ")
                menit=menit+1
            print(" ")
            print("data awal : ",data)

            h=59
            while h>0:
                data[h,2]=data[h,2]-data[h-1,2]
                data[h,0]=data[h,0]-10
                h=h-1
            data[h,2]=0
            data[h,0]=data[h,0]-10

            g=0
            while g<60:
                if np.isnan(data[g,2]):
                    data[g,0]=data[g-1,0]
                    data[g,1]=data[g-1,1]
                    data[g,2]=data[g-1,2]
                g = g + 1
                    

            print("data selisih curah hujan : ",data)
    
            i=5
            j=0
            while i < 60:
                data_t[j,0]=data[i-5,2]
                data_t[j,1]=data[i-4,2]
                data_t[j,2]=data[i-3,2]
                data_t[j,3]=data[i-2,2]
                data_t[j,4]=data[i-1,2]
                data_t[j,5]=data[i,0]
                data_t[j,6]=data[i,1]
                data_t[j,7]=data[i,2]
                i=i+1
                j=j+1
            print("data dengan time series : ",data_t)
            return data_t
        except:
            print("ambil data gagal")
