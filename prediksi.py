import numpy as np
from matplotlib import pyplot as plt
from JST_hujan import *
from bobot import *
import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from koneksi import *

# menciptakan objek dari kelas koneksi
konek = koneksi();
jst = JST();

bb = bobot_ann()
[V,W] = bb.bobot()
# st.write(V)
# st.write(W)

n_hidden = 8
n_output = 1

min_humidity = 90
maks_humidity = 100
min_tempC = 20
maks_tempC = 30
min_precipMM = 0
maks_precipMM = 6

st.write("Data ke- \t humidity \t temperature \t prediksi JST \t data sebenarnya \t Eror")
k=0
# plt.axis([0, 10, 0, 50])
while True :
    realtime = konek.ambil_data()
    realtime = np.array(realtime)
    
    r_humidity = realtime[0]
    r_humidity = r_humidity.astype(np.int64) - 10
    r_tempC = realtime[1]
    r_tempC = r_tempC.astype(np.int64)
    r_precipMM = realtime[2]
    r_precipMM = r_precipMM.astype(np.int64)

    r_humidity = round((r_humidity-min_humidity)/(maks_humidity-min_humidity),3)
    r_tempC = round((r_tempC-min_tempC)/(maks_tempC-min_tempC),3)
    r_precipMM = round((r_precipMM-min_precipMM)/(maks_precipMM-min_precipMM),3)

    realtime_normalisasi = np.array([r_humidity,r_tempC,r_precipMM])

    data_uji = realtime_normalisasi[0:2]
    output_sebenarnya = realtime_normalisasi[2]
    data_tampil = realtime[0:2]
    
    n_datauji = 1
    hasil_prediksi = np.zeros((n_datauji, 1))

    for j in range(n_datauji):
        [Z,Y] = jst.PerambatanMaju(data_uji,V,W,n_hidden,n_output)
        hasil_prediksi[j,0]=Y[0,0]
        

    minprecipMM = min_precipMM
    maksprecipMM = maks_precipMM

    hasilprediksi_denormalisasi = np.zeros((n_datauji,1))
    outputsebenarnya_denormalisasi = np.zeros((n_datauji,1))

    for i in range(n_datauji):
        hasilprediksi_denormalisasi[i,0]=jst.Denormalisasi(hasil_prediksi[i,0],
                                                       minprecipMM,maksprecipMM)
        outputsebenarnya_denormalisasi[i,0]=jst.Denormalisasi(output_sebenarnya,
                                                           minprecipMM,maksprecipMM)

    for i in range(n_datauji):
        hasiljst=hasilprediksi_denormalisasi[i,0]
        datasebenarnya=outputsebenarnya_denormalisasi[i,0]

        hasiljst = hasiljst - 0

        erorhasil=abs(hasiljst-datasebenarnya)
        print((k+1),"\t\t",data_tampil[0],"\t\t",data_tampil[1],
              "\t\t",hasiljst,"\t\t",datasebenarnya,
              "\t\t\t",erorhasil)
    y1 = hasiljst
    y2 = datasebenarnya
    

    # plt.scatter(k,y1,color='green')
    # plt.scatter(k,y2,color='red')
    # plt.pause(0.05)
    # plt.axis([0,k+5,0,50])
    st.write(y1)
    st.write(y2)
    k = k+1

    

    p = figure(
        title='simple line example',
        x_axis_label='x',
        y_axis_label='y')

    p.line(y1, y2, legend_label='Trend', line_width=2)

    st.bokeh_chart(p, use_container_width=True)
