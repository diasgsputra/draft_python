import numpy as np
from matplotlib import pyplot as plt
from JST import *

# menciptakan objek dari kelas JST
jst = JST();

# inisialisasi parameter-parameter JST
n_input = 3
n_hidden = 3
n_output = 2
alpha = 0.95
toleransi_eror = 0.001
iterasi = 1000

#inisialisasi data latih
data = np.array([[0.034, 0.5, 0.239, 0, 0],
                 [0.483, 0.112, 0.142, 0, 1],
                 [0.569, 1, 0.458, 0, 0],
                 [0.103, 0.378, 1, 0, 0],
                 [0, 0.106, 0.048, 0, 1],
                 [0.103, 0.020, 0.034, 1, 0],
                 [0.103, 0.031, 0.078, 1, 0],
                 [0.052, 0.031, 0.678, 1, 1],
                 [1, 0, 0, 1, 1],
                 [0.086, 0.041, 0.048, 1, 0],
                 [0.103, 0.306, 0.198, 0, 0],
                 [0.276, 0, 0.511, 1, 1]])

# menentukan jumlah data latih dan data uji
n_datalatih = 8
n_datauji = 4

#menentukan data latih dan target output
data_latih = data[0:n_datalatih, 0:3]
target_output = data[0:n_datalatih, 3:5]

#inisialisasi bobot V dan bobot W
V = np.array([[0.1, 0.1, 0.1],
              [0.2, 0.35, 0.1],
              [0.3, 0.27, 0.25],
              [0.1, 0.4, 0.35]])
W = np.array([[0.1, 0.1],
              [0.1, 0.25],
              [0.2, 0.2],
              [0.25, 0.15]])

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
print(data)
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
eror = np.zeros([n_datalatih,1])
mse = np.zeros([iterasi,1])
jumlah_iterasi = 0

for i in range(iterasi):
    print('iterasi ke-',(i+1))
    for j in range(n_datalatih):
        [Z,Y] = jst.PerambatanMaju(data_latih[j,:],V,W,n_hidden,n_output)
        [W,V] = jst.PerambatanMundur(target_output[j],Y,data_latih[j,:],alpha,Z,W,V)
        eror[j,0]=sum(abs(target_output[j]-Y[0]))**2

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
data_uji = data[n_datalatih:n_datalatih+n_datauji,0:3]
output_sebenarnya = data[n_datalatih:n_datalatih+n_datauji,3:5]
hasil_prediksi = np.zeros((n_datauji, n_output))
keterangan_jenisgempa=[]

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

#menampilkan hasil prediksi
print("Data ke- \t X1 \t X2 \t X3 \t Output JST \t Output Sebenarnya \t Jenis Gempa Hasil Prediksi")
for i in range(n_datauji):
    print((i+1),"\t\t",data_uji[i,0],"\t",data_uji[i,1],"\t",data_uji[i,2],"\t ",
          str(int(hasil_prediksi[i,0]))+' '+str(int(hasil_prediksi[i,1])),"\t\t ",
          str(int(output_sebenarnya[i,0]))+' '+str(int(output_sebenarnya[i,1])),
          "\t\t\t",keterangan_jenisgempa[i])

plt.show()
