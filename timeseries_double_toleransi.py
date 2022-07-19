import numpy as np
from matplotlib import pyplot as plt
from JST_hujan import *
import pandas as pd

# menciptakan objek dari kelas JST
jst = JST();

# inisialisasi parameter-parameter JST
n_input = 7
n_hidden = 8
n_output = 1
alpha = 0.95
toleransi_eror = 0.001
iterasi = 10
print("tes 1")

# membaca data harian
namafile = "D:\\SEMESTER 9\\SKRIPSI\\Wonosari_2010-2021_excel_timeseries.xlsx"
data = pd.read_excel(namafile,sheet_name="Wonosari_2010-2011")
print("dataframe:",data)
data = data.to_numpy()
print("tes 2")
#exit()

# mengakses data berdasarkan kolom/parameter
t5 = data[:,1]
t4 = data[:,2]
t3 = data[:,3]
t2 = data[:,4]
t1 = data[:,5]
suhu = data[:,6]
tekanan_udara = data[:,7]
curah_hujan = data[:,8]
print("tes 3")
#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# normalisasi data menggunakan fungsi Nrmalisasi kelas JST
t5 = jst.Normalisasi(t5)
t4 = jst.Normalisasi(t4)
t3 = jst.Normalisasi(t3)
t2 = jst.Normalisasi(t2)
t1 = jst.Normalisasi(t1)
suhu = jst.Normalisasi(suhu)
tekanan_udara = jst.Normalisasi(tekanan_udara)
curah_hujan = jst.Normalisasi(curah_hujan)

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# data ternormalisasi
data_normalisasi = np.concatenate((
    t5,t4,t3,t2,t1,suhu,
    tekanan_udara,curah_hujan
    ),axis=1)

#print("data ternormalisasi:",data_normalisasi)
#exit()

# menentukan jumlah data latih dan data uji
n_datalatih = 4000
n_datauji = 100

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
mint = 1.0

for i in range(iterasi):
    print('iterasi ke-',(i+1))
    for j in range(n_datalatih):
        # pengkodean target keluaran
        #print("target output : ",t_output)
        [Z,Y] = jst.PerambatanMaju(data_latih[j,:],V,W,n_hidden,n_output)
        [W,V] = jst.PerambatanMundur(target_output[j],Y,data_latih[j,:],alpha,Z,W,V)

        eror[j,0]=abs(target_output[j]-Y[0,0])

    mse[i,0]=round(sum(eror[:,0])/n_datalatih,3)
    if mse[i,0] > mint :
        mse[i,0]=mint
        print('MSE : ',mse[i,0])
    else :
        mint = mse[i,0]
        print('MSE : ',mse[i,0])

    jumlah_iterasi = i+1

#menampilkan V dan W setelah training
print('')
print('Bobot V                    : ')
print(V)
print('')
print('Bobot W                    : ')
print(W)
print('')

#plt.figure()
#plt.plot(mse[0:jumlah_iterasi,0])
#plt.xlabel('Iterasi ke-i, (0 < i < '+str(jumlah_iterasi)+')')
#plt.ylabel('MSE')
#plt.title('Grafik konvergensi proses pelatihan data harian')
#plt.show()
#exit()




# inisialisasi parameter-parameter JST
n_input = 7
n_hidden = 8
n_output = 1
alpha = 0.95
toleransi_eror = 0.001
iterasi = 10
print("tes 1_2")

# membaca data harian
namafile = "D:\\SEMESTER 9\\SKRIPSI\\hujan_menit_2.xls"
data = pd.read_excel(namafile,sheet_name="Sheet2")
print("dataframe:",data)
data = data.to_numpy()

#exit()

# mengakses data berdasarkan kolom/parameter
t5 = data[:,1]
t4 = data[:,2]
t3 = data[:,3]
t2 = data[:,4]
t1 = data[:,5]
suhu = data[:,6]
tekanan_udara = data[:,7]
curah_hujan = data[:,8]

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# normalisasi data menggunakan fungsi Nrmalisasi kelas JST
t5 = jst.Normalisasi(t5)
t4 = jst.Normalisasi(t4)
t3 = jst.Normalisasi(t3)
t2 = jst.Normalisasi(t2)
t1 = jst.Normalisasi(t1)
suhu = jst.Normalisasi(suhu)
tekanan_udara = jst.Normalisasi(tekanan_udara)
curah_hujan = jst.Normalisasi(curah_hujan)

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# data ternormalisasi
data_normalisasi = np.concatenate((
    t5,t4,t3,t2,t1,suhu,
    tekanan_udara,curah_hujan
    ),axis=1)

#print("data ternormalisasi:",data_normalisasi)
#exit()

# menentukan jumlah data latih dan data uji
n_datalatih = 2000
n_datauji = 200

# menentukan data latih
data_latih = data_normalisasi[0:n_datalatih,0:7]
target_output = data_normalisasi[0:n_datalatih,7]

#print("data latih:",data_latih)
#print("target output:",target_output)
#exit()

# membangkitkan bobot V dan bobot W seara acak
#tanpa acak bobot (menggunakan bobot sebelumnya)
#[V,W] = jst.AcakBobot(n_input,n_hidden,n_output)

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

mint = 1.0

for i in range(iterasi):
    print('iterasi ke-',(i+1))
    for j in range(n_datalatih):
        # pengkodean target keluaran
        #print("target output : ",t_output)
        [Z,Y] = jst.PerambatanMaju(data_latih[j,:],V,W,n_hidden,n_output)
        [W,V] = jst.PerambatanMundur(target_output[j],Y,data_latih[j,:],alpha,Z,W,V)

        eror[j,0]=abs(target_output[j]-Y[0,0])

    mse[i,0]=round(sum(eror[:,0])/n_datalatih,3)
    if mse[i,0] > mint :
        mse[i,0]=mint
        print('MSE : ',mse[i,0])
    else :
        mint = mse[i,0]
        print('MSE : ',mse[i,0])

    jumlah_iterasi = i+1

#menampilkan V dan W setelah training
print('')
print('Bobot V                    : ')
print(V)
print('')
print('Bobot W                    : ')
print(W)
print('')


#menampilkan grafik konvergensi proses pelatihan
plt.figure()
plt.plot(mse[0:jumlah_iterasi,0])
plt.xlabel('Iterasi ke-i, (0 < i < '+str(jumlah_iterasi)+')')
plt.ylabel('MSE')
plt.title('Grafik konvergensi proses pelatihan data realtime')
#plt.show()
#exit()

print('')
print('========================================')
print('            PROSES PENGUJIAN            ')
print('========================================')

#menentukan data uji dan output sebenarnya
data_uji = data_normalisasi[n_datalatih:n_datalatih+n_datauji,0:7]
output_sebenarnya = data_normalisasi[n_datalatih:n_datalatih+n_datauji,7]
#print("data uji : ",data_uji)
#print("output sebenarnya : ",output_sebenarnya)


# mendeklarasikan variabel-variabel yang dibutuhkan dalam pengujian
hasil_prediksi = np.zeros((n_datauji, 1))


for j in range(n_datauji):
    [Z,Y] = jst.PerambatanMaju(data_uji[j,:],V,W,n_hidden,n_output)
    hasil_prediksi[j,0]=Y[0,0]

#melakukan denormalisasi hasil prediksi dan data sebenarnya
minprecipMM = min(data[:,8])
maksprecipMM = max(data[:,8])

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

rata2akurasi=0
#menampilkan hasil prediksi
print("Data ke- \t X1 \t X2 \t X3 \t X4 \t X5 \t X6 \t Output JST \t Output Sebenarnya \t Eror")
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

    a=0

    if(hasiljst>datasebenarnya):
        a=hasiljst
    else:
        a=datasebenarnya

    if erorhasil==a and a==0:
        akurasi = 100
    else:
        akurasi=round(100-(erorhasil/a*100),3)    
    
    rata2akurasi+=akurasi
     
    print((i+1),"\t\t",data_uji[i,0],"\t",data_uji[i,1],"\t",data_uji[i,2]
          ,"\t",data_uji[i,3],"\t",data_uji[i,4],"\t",data_uji[i,5]
          ,"\t",data_uji[i,6],"\t",hasilprediksi_denormalisasi[i,0],"\t\t",datasebenarnya,
          "\t\t\t",erorhasil)

rata2akurasi=round(rata2akurasi/n_datauji,3)
print("akurasi = ",rata2akurasi)

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
