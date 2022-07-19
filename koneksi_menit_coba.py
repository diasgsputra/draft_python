import mysql.connector
import time
import numpy as np


data = np.zeros((10, 3))
print(data)
data_t = np.zeros((5,8))
print(data_t)
menit = 0;
    
mydb = mysql.connector.connect(
    host="103.102.153.194",
    user="db_dan",
    password="dan1313",
    database="db_dan"
)
    
mycursor = mydb.cursor()
while menit < 10:
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

h=9
while h>0:
    data[h,2]=data[h,2]-data[h-1,2]
    data[h,0]=data[h,0]-10
    h=h-1
data[h,2]=0
data[h,0]=data[h,0]-10

g=0
while g<10:
    if np.isnan(data[g,2]):
        data[g,0]=data[g-1,0]
        data[g,1]=data[g-1,1]
        data[g,2]=data[g-1,2]
    g = g+1
            
                    

print("data selisih curah hujan : ",data)
    
i=5
j=0
while i < 10:
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

