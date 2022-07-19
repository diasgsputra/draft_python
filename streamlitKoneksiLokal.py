import streamlit as st
import mysql.connector
import time
import numpy as np
import pyautogui as pg
import datetime



class koneksi :
    i=1
    while True :
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mydb = mysql.connector.connect(
            host="103.102.153.194",
            user="db_dias",
            password="dias1234",
            database="db_dias"
        )
    
        mycursor = mydb.cursor()
        # mycursor.execute("SELECT * FROM realtime_hujan")
        # myresult = mycursor.fetchall()
        # data = np.array(myresult)
        # st.write("iterasi ke : "+str(i))
        # st.write(data)
        
        sql = ("INSERT INTO realtime_hujan"
            "(waktu,t5,t4,t3,t2,t1,h,t,ch)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        val = (now, '0', '0', '0', '0', '0', '93', '26', '0')
        mycursor.execute(sql, val)

        mydb.commit()

        st.write(mycursor.rowcount, "record inserted.")

        #st.line_chart(data=myresult, width=10, height=10, use_container_width=True)
        #st.write(data[i])
        time.sleep(1)
        # if i%5==0:
        #     pg.hotkey("ctrl","F5")
        i=i+1
