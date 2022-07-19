import numpy as np
from matplotlib import pyplot as plt
from JST_hujan import *
import pandas as pd
from koneksi import *

# menciptakan objek dari kelas koneksi
konek = koneksi();

# menciptakan objek dari kelas JST
jst = JST();

# inisialisasi parameter-parameter JST
n_input = 2
n_hidden = 2
n_output = 1
alpha = 0.95
toleransi_eror = 0.001
iterasi = 1

# membaca data
namafile = "D:\\_Kuliah_\\SEMESTER 9\\SKRIPSI\\Wonosari_2010-2021_excel_EditedColumns.xlsx"
data = pd.read_excel(namafile,sheet_name="Wonosari_2010-2011")
data = data.to_numpy()

# mengakses data berdasarkan kolom/parameter
humidity = data[:,4]
tempC = data[:,8]
precipMM = data[:,9]

maks_humidity = max(humidity)
min_humidity = min(humidity)

maks_tempC = max(tempC)
min_tempC = min(tempC)

maks_precipMM = max(precipMM)
min_precipMM = min(precipMM)

humidity = jst.Normalisasi(humidity)
tempC = jst.Normalisasi(tempC)
precipMM = jst.Normalisasi(precipMM)

# data ternormalisasi
data_normalisasi = np.concatenate((
    humidity,tempC,precipMM
    ),axis=1)

# menentukan jumlah data latih dan data uji
n_datalatih = 3352
n_datauji = 300

# menentukan data latih
data_latih = data_normalisasi[0:n_datalatih,0:2]
target_output = data_normalisasi[0:n_datalatih,2]

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

print("Data ke- \t humidity \t temperature \t prediksi JST \t data sebenarnya \t Eror")
k=0
plt.axis([0, 10, 0, 50])
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

    #if datasebenarnya <= 10:
     #   hasiljst = hasiljst-4
    #elif datasebenarnya >= 20:
     #   hasiljst = hasiljst-5
    #else :
     #   hasiljst = hasiljst+3

        hasiljst = hasiljst - 0

        erorhasil=abs(hasiljst-datasebenarnya)
        print((k+1),"\t\t",data_tampil[0],"\t\t",data_tampil[1],
              "\t\t",hasiljst,"\t\t",datasebenarnya,
              "\t\t\t",erorhasil)
    y1 = hasiljst
    y2 = datasebenarnya
    

    plt.scatter(k,y1,color='green')
    plt.scatter(k,y2,color='red')
    plt.pause(0.05)
    plt.axis([0,k+5,0,50])

    k = k+1

plt.show()
