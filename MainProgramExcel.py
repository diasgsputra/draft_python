import numpy as np
from matplotlib import pyplot as plt
from JST import *
import pandas as pd

# menciptakan objek dari kelas JST
jst = JST();

# inisialisasi parameter-parameter JST
n_input = 3
n_hidden = 5
n_output = 2
alpha = 0.95
toleransi_eror = 0.001
iterasi = 10

# membaca data
namafile = "D:\\_Kuliah_\\SEMESTER 9\\SKRIPSI\\data.xlsx"
data = pd.read_excel(namafile,sheet_name="Sheet1")
#print("dataframe:",data)
data = data.to_numpy()
#print("numpy:",data)
#exit()

# mengakses data berdasarkan kolom/parameter
amplitudo = data[:,0]
sp = data[:,1]
periode = data[:,2]
jenis_gempa = data[:,3]

# normalisasi data menggunakan fungsi Nrmalisasi kelas JST
amplitudo = jst.Normalisasi(amplitudo)
sp = jst.Normalisasi(sp)
periode = jst.Normalisasi(periode)


# data ternormalisasi
data_normalisasi = np.concatenate((amplitudo,sp,periode),axis=1)

# menentukan jumlah data latih dan data uji
n_datalatih = 170
n_datauji = 30

# menentukan data latih
data_latih = data_normalisasi[0:n_datalatih,0:3]
target_output = jenis_gempa[0:n_datalatih]

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
        t_output = np.zeros((1,2),dtype=int)
        if target_output[j] == 'Tektonik Jauh':
            t_output[0,0]=0
            t_output[0,1]=0
        elif target_output[j] == 'Tektonik Lokal':
            t_output[0,0]=0
            t_output[0,1]=1
        elif target_output[j] == 'Vulkanik A':
            t_output[0,0]=1
            t_output[0,1]=0
        elif target_output[j] == 'Hembusan':
            t_output[0,0]=1
            t_output[0,1]=1
        
        [Z,Y] = jst.PerambatanMaju(data_latih[j,:],V,W,n_hidden,n_output)
        [W,V] = jst.PerambatanMundur(t_output[0,:],Y,data_latih[j,:],alpha,Z,W,V)

        eror[j,0]=sum(abs(t_output[0,:]-Y[0]))**2
        print("target output : ",t_output[0,:])
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
data_uji = data_normalisasi[n_datalatih:n_datalatih+n_datauji,0:3]
output_sebenarnya = jenis_gempa[n_datalatih:n_datalatih+n_datauji]

# mendeklarasikan variabel-variabel yang dibutuhkan dalam pengujian
hasil_prediksi = np.zeros((n_datauji, n_output))
keterangan_jenisgempa=[]
jumlahprediksibenar = 0

for j in range(n_datauji):
    [Z,Y] = jst.PerambatanMaju(data_uji[j,:],V,W,n_hidden,n_output)
    hasil_prediksi[j,0]=round(Y[0,0])
    hasil_prediksi[j,1]=round(Y[0,1])

    if hasil_prediksi[j,0] == 0 and hasil_prediksi[j,1]==0:
        keterangan_jenisgempa.append('Tektonik Jauh')
    elif hasil_prediksi[j,0]==0 and hasil_prediksi[j,1]==1:
        keterangan_jenisgempa.append('Tektonik Lokal')
    elif hasil_prediksi[j,0]==1 and hasil_prediksi[j,1]==0:
        keterangan_jenisgempa.append('Vulkanik A')
    elif hasil_prediksi[j,0]==1 and hasil_prediksi[j,1]==1:
        keterangan_jenisgempa.append('Hembusan')

    # menentukan berapa jumlah data hasil prediksi yang benar
    if(output_sebenarnya[j]==keterangan_jenisgempa[j]):
        jumlahprediksibenar+=1

#menampilkan hasil prediksi
print("Data ke- \t X1 \t X2 \t X3 \t Output JST \t Output Sebenarnya \t Jenis Gempa Hasil Prediksi")
for i in range(n_datauji):
    # pengkodean output sebenarnya
    output = np.zeros((1,2),dtype=int)

    if output_sebenarnya[i] == 'Tektonik Jauh':
        output[0,0]=0
        output[0,1]=0
    elif output_sebenarnya[i] == 'Tektonik Lokal':
        output[0,0]=0
        output[0,1]=1
    elif output_sebenarnya[i] == 'Vulkanik A':
        output[0,0]=1
        output[0,1]=0
    elif output_sebenarnya[i] == 'Hembusan':
        output[0,0]=1
        output[0,1]=1
        
    print((i+1),"\t\t",data_uji[i,0],"\t",data_uji[i,1],"\t",data_uji[i,2],"\t ",
          str(int(hasil_prediksi[i,0]))+' '+str(int(hasil_prediksi[i,1])),"\t\t ",
          str(int(output[0,0]))+' '+str(int(output[0,1])),
          "\t\t\t",keterangan_jenisgempa[i])
# menghitung persentase akurasi
akurasi = jumlahprediksibenar/n_datauji*100
print('Akurasi : ',round(akurasi,3),' %')
plt.show()
