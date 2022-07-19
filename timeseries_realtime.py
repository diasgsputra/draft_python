import numpy as np
from matplotlib import pyplot as plt
from JST_hujan import *
import pandas as pd
from koneksi_menit import *

# menciptakan objek dari kelas JST
jst = JST();

konek = koneksi();


# inisialisasi parameter-parameter JST
n_input = 7
n_hidden = 14
n_output = 1
alpha = 0.95
toleransi_eror = 0.001
iterasi = 50

# membaca data
namafile = "D:\\_Kuliah_\\SEMESTER 9\\SKRIPSI\\Wonosari_2010-2021_excel_timeseries.xlsx"
data = pd.read_excel(namafile,sheet_name="Wonosari_2010-2011")
print("data sekunder : ",data)
data = data.to_numpy()


#exit()

# mengakses data berdasarkan kolom/parameter
#date = data[:,0]
t5 = data[:,1]
t4 = data[:,2]
t3 = data[:,3]
t2 = data[:,4]
t1 = data[:,5]
humidity = data[:,6]
tempC = data[:,7]
precipMM = data[:,8]

maks_humidity = max(humidity)
min_humidity = min(humidity)

maks_tempC = max(tempC)
min_tempC = min(tempC)

maks_precipMM = max(precipMM)
min_precipMM = min(precipMM)

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# normalisasi data menggunakan fungsi Nrmalisasi kelas JST
t5 = jst.Normalisasi(t5)
t4 = jst.Normalisasi(t4)
t3 = jst.Normalisasi(t3)
t2 = jst.Normalisasi(t2)
t1 = jst.Normalisasi(t1)
humidity = jst.Normalisasi(humidity)
tempC = jst.Normalisasi(tempC)
precipMM = jst.Normalisasi(precipMM)

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# data ternormalisasi
data_normalisasi = np.concatenate((
    t5,t4,t3,t2,t1,humidity,
    tempC,precipMM
    ),axis=1)

#print("data ternormalisasi:",data_normalisasi)
#exit()

# menentukan jumlah data latih dan data uji
n_datalatih = 4267
n_datauji = 50

# menentukan data latih
data_latih = data_normalisasi[0:n_datalatih,0:7]
target_output = data_normalisasi[0:n_datalatih,7]



#print("data latih:",data_latih)
#print("target output:",target_output)
#exit()

# membangkitkan bobot V dan bobot W seara acak
[V,W] = jst.AcakBobot(n_input,n_hidden,n_output)

print('========================================')
print('      PARAMETER JST BACKPROPAGATION     ')
print('========================================')
print('')
print('Neuron Input    : ',n_input)
print('Neuron Hidden   : ',n_hidden)
print('Neuron Output   : ',n_output)
print('Laju Pembelajaran (alpha) : ',alpha)
print('Toleransi eror  : ',toleransi_eror)
print('iterasi         : ',iterasi)
print('Data Latih                 : ')
print(data_latih)
print('')
print('Target Output              : ')
print(target_output)
print('')
print('Bobot V                    : ')
print(V)
print('')
print('Bobot W                    : ')
print(W)
print('')

print('========================================')
print('            PROSES PELATIHAN            ')
eror = np.zeros((n_datalatih,1))
mse = np.zeros((iterasi,1))
jumlah_iterasi = 0

for i in range(iterasi):
    print('iterasi ke-',(i+1))
    for j in range(n_datalatih):
        # pengkodean target keluaran
        #print("target output : ",t_output)
        [Z,Y] = jst.PerambatanMaju(data_latih[j,:],V,W,n_hidden,n_output)
        [W,V] = jst.PerambatanMundur(target_output[j],Y,data_latih[j,:],alpha,Z,W,V)

        eror[j,0]=abs(target_output[j]-Y[0,0])
        
    mse[i,0]=round(sum(eror[:,0])/n_datalatih,3)
    print('MSE : ',mse[i,0])
    
    if mse[i,0] <= toleransi_eror:
        jumlah_iterasi = i+1
        break

    jumlah_iterasi = i+1

#menampilkan grafik konvergensi proses pelatihan
plt.figure()
plt.plot(mse[0:jumlah_iterasi,0])
plt.xlabel('Iterasi ke-i, (0 < i < '+str(jumlah_iterasi)+')')
plt.ylabel('MSE')
plt.title('Grafik konvergensi proses pelatihan')

print('')
print('========================================')
print('            PROSES PENGUJIAN            ')
print('========================================')

realtime = konek.ambil_data()
realtime = np.array(realtime)
print("data realtime dari koneksi : ",realtime)

r_t5 = realtime[:,0]
r_t4 = realtime[:,1]
r_t3 = realtime[:,2]
r_t2 = realtime[:,3]
r_t1 = realtime[:,4]
r_humidity = realtime[:,5]
r_tempC = realtime[:,6]
r_precipMM = realtime[:,7]

r_t5 = jst.Normalisasi_realtime(r_t5,min_precipMM,maks_precipMM)
r_t4 = jst.Normalisasi_realtime(r_t4,min_precipMM,maks_precipMM)
r_t3 = jst.Normalisasi_realtime(r_t3,min_precipMM,maks_precipMM)
r_t2 = jst.Normalisasi_realtime(r_t2,min_precipMM,maks_precipMM)
r_t1 = jst.Normalisasi_realtime(r_t1,min_precipMM,maks_precipMM)
r_humidity = jst.Normalisasi_realtime(r_humidity,min_humidity,maks_humidity)
r_tempC = jst.Normalisasi_realtime(r_tempC,min_tempC,maks_tempC)
r_precipMM = jst.Normalisasi_realtime(r_precipMM,min_precipMM,maks_precipMM)

realtime_normalisasi = np.concatenate((
    r_t5,r_t4,r_t3,r_t2,r_t1,r_humidity,
    r_tempC,r_precipMM
    ),axis=1)

print("data realtime setelah normalisasi : ",realtime_normalisasi)


#menentukan data uji dan output sebenarnya
data_uji = realtime_normalisasi[:,0:7]
output_sebenarnya = realtime_normalisasi[:,7]
#print("data uji : ",data_uji)
#print("output sebenarnya : ",output_sebenarnya)

n_datauji = 55

# mendeklarasikan variabel-variabel yang dibutuhkan dalam pengujian
hasil_prediksi = np.zeros((n_datauji, 1))

print("hasil prediksi zero: ",hasil_prediksi)

print("data uji : ",data_uji)


for j in range(n_datauji):
    [Z,Y] = jst.PerambatanMaju(data_uji[j,:],V,W,n_hidden,n_output)
    hasil_prediksi[j,0]=Y[0,0]

#melakukan denormalisasi hasil prediksi dan data sebenarnya
minprecipMM = min_precipMM
maksprecipMM = maks_precipMM

#print("minprecipMM : ",minprecipMM)
#print("maksprecipMM : ",maksprecipMM)

hasilprediksi_denormalisasi = np.zeros((n_datauji,1))
outputsebenarnya_denormalisasi = np.zeros((n_datauji,1))

#print("prediksi denormalisasi : ",hasilprediksi_denormalisasi)
#print("sebenarnya denormalisasi : ",outputsebenarnya_denormalisasi)

for i in range(n_datauji):
    #print("hasil_prediksi[i,0] : ",hasil_prediksi[i,0])
    hasilprediksi_denormalisasi[i,0]=jst.Denormalisasi(hasil_prediksi[i,0],
                                                       minprecipMM,maksprecipMM)
    outputsebenarnya_denormalisasi[i,0]=jst.Denormalisasi(output_sebenarnya[i],
                                                          minprecipMM,maksprecipMM)

#print("hasil prediksi denormalisasi : ",hasilprediksi_denormalisasi)
#print("output sebenarnya : ",outputsebenarnya_denormalisasi)
#exit()

#menampilkan hasil prediksi
print("Data ke- \t X1 \t X2 \t X3 \t X4 \t X5 \t X6 \t X7 \t Output JST \t Output Sebenarnya \t Eror")
for i in range(n_datauji):
    hasiljst=hasilprediksi_denormalisasi[i,0]
    datasebenarnya=outputsebenarnya_denormalisasi[i,0]

    #if datasebenarnya <= 10:
    #    hasilprediksi_denormalisasi[i,0] = hasilprediksi_denormalisasi[i,0]-2
    #elif datasebenarnya >= 20:
    #    hasilprediksi_denormalisasi[i,0] = hasilprediksi_denormalisasi[i,0]-5
    #else :
    #    hasilprediksi_denormalisasi[i,0] = hasilprediksi_denormalisasi[i,0]+3

    erorhasil=abs(hasiljst-datasebenarnya)
    print((i+1),"\t\t",data_uji[i,0],"\t",data_uji[i,1],"\t",data_uji[i,2]
          ,"\t",data_uji[i,3],"\t",data_uji[i,4],"\t",data_uji[i,5]
          ,"\t",data_uji[i,6],"\t",hasilprediksi_denormalisasi[i,0],"\t\t",datasebenarnya,
          "\t\t\t",erorhasil)

#menampilkan grafik konvergensi proses pelatihan
#y1 = hasiljst
#y2 = datasebenarnya
y1 = hasilprediksi_denormalisasi
y2 = outputsebenarnya_denormalisasi
x_tmp = list(range(1,n_datauji+1))
x = np.array([x_tmp]).transpose()

plt.figure()
plt.plot(x,y1,'r',x,y2,'g')
plt.xlabel('Data Uji Ke-i, (0 < i < '+str(n_datauji)+')')
plt.ylabel('Curah Hujan')
plt.title('Grafik Perbandingan Hasil Prediksi JST dan Data Sebenarnya')
plt.legend(('Hasil Prediksi JST', 'Data Sebenarnya'),loc='upper right')
plt.show()
