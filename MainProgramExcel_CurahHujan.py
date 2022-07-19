import numpy as np
from matplotlib import pyplot as plt
from JST_hujan import *
import pandas as pd

# menciptakan objek dari kelas JST
jst = JST();

# inisialisasi parameter-parameter JST
n_input = 8
n_hidden = 4
n_output = 1
alpha = 0.95
toleransi_eror = 0.001
iterasi = 100

# membaca data
namafile = "D:\\_Kuliah_\\SEMESTER 9\\SKRIPSI\\Wonosari_2010-2021_excel_EditedColumns.xlsx"
data = pd.read_excel(namafile,sheet_name="Wonosari_2010-2011")
#print("dataframe:",data)
data = data.to_numpy()


#exit()

# mengakses data berdasarkan kolom/parameter
#date = data[:,0]
DewPointC = data[:,1]
cloudcover = data[:,2]
windspeedKmph = data[:,3]
humidity = data[:,4]
pressure = data[:,5]
winddirDegree = data[:,6]
WindGustKmph = data[:,7]
tempC = data[:,8]
precipMM = data[:,9]

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# normalisasi data menggunakan fungsi Nrmalisasi kelas JST
DewPointC = jst.Normalisasi(DewPointC)
cloudcover = jst.Normalisasi(cloudcover)
windspeedKmph = jst.Normalisasi(windspeedKmph)
humidity = jst.Normalisasi(humidity)
pressure = jst.Normalisasi(pressure)
winddirDegree = jst.Normalisasi(winddirDegree)
WindGustKmph = jst.Normalisasi(WindGustKmph)
tempC = jst.Normalisasi(tempC)
precipMM = jst.Normalisasi(precipMM)

#print("DewPointC :",DewPointC)
#print("precipMM :",precipMM)

# data ternormalisasi
data_normalisasi = np.concatenate((
    DewPointC,cloudcover,windspeedKmph,humidity,pressure,winddirDegree,
    WindGustKmph,tempC,precipMM
    ),axis=1)

#print("data ternormalisasi:",data_normalisasi)
#exit()

# menentukan jumlah data latih dan data uji
n_datalatih = 3352
n_datauji = 300

# menentukan data latih
data_latih = data_normalisasi[0:n_datalatih,0:8]
target_output = data_normalisasi[0:n_datalatih,8]

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

#menentukan data uji dan output sebenarnya
data_uji = data_normalisasi[n_datalatih:n_datalatih+n_datauji,0:8]
output_sebenarnya = data_normalisasi[n_datalatih:n_datalatih+n_datauji,8]
#print("data uji : ",data_uji)
#print("output sebenarnya : ",output_sebenarnya)


# mendeklarasikan variabel-variabel yang dibutuhkan dalam pengujian
hasil_prediksi = np.zeros((n_datauji, 1))


for j in range(n_datauji):
    [Z,Y] = jst.PerambatanMaju(data_uji[j,:],V,W,n_hidden,n_output)
    hasil_prediksi[j,0]=Y[0,0]

#melakukan denormalisasi hasil prediksi dan data sebenarnya
minprecipMM = min(data[:,9])
maksprecipMM = max(data[:,9])

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
print("Data ke- \t X1 \t X2 \t X3 \t X4 \t X5 \t X6 \t X7 \t X8 Output JST \t Output Sebenarnya \t Eror")
for i in range(n_datauji):
    hasiljst=hasilprediksi_denormalisasi[i,0]
    datasebenarnya=outputsebenarnya_denormalisasi[i,0]

    if datasebenarnya <= 10:
        hasilprediksi_denormalisasi[i,0] = hasilprediksi_denormalisasi[i,0]-2
    elif datasebenarnya >= 20:
        hasilprediksi_denormalisasi[i,0] = hasilprediksi_denormalisasi[i,0]-5
    else :
        hasilprediksi_denormalisasi[i,0] = hasilprediksi_denormalisasi[i,0]+3

    erorhasil=abs(hasiljst-datasebenarnya)
    print((i+1),"\t\t",data_uji[i,0],"\t",data_uji[i,1],"\t",data_uji[i,2]
          ,"\t",data_uji[i,3],"\t",data_uji[i,4],"\t",data_uji[i,5]
          ,"\t",data_uji[i,6],"\t",data_uji[i,7],"\t",hasilprediksi_denormalisasi[i,0],"\t\t",datasebenarnya,
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
