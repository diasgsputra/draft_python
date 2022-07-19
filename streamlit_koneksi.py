import streamlit as st
import mysql.connector
import time
import numpy as np

class koneksi :
    i=0
    while True :

        mydb = mysql.connector.connect(
            host="103.102.153.194",
            user="db_dan",
            password="dan1313",
            database="db_dan"
        )
    
        mycursor = mydb.cursor()
        mycursor.execute("SELECT t, h, ch FROM loghujan WHERE id_alat = 'C001' ORDER BY id DESC LIMIT 1")
        myresult = mycursor.fetchone()

        #data[i]=np.array(myresult)
        st.write(myresult)
        #st.line_chart(data=myresult, width=10, height=10, use_container_width=True)
        #st.write(data[i])
        #time.sleep(1)
        i=i+1
