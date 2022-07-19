import numpy as np
from JST import *

# menciptakan objek dari kelas JST
jst = JST();

#inisialisasi parameter-parameter JST
n_input = 3
n_hidden = 3
n_output = 2
alpha = 0.3
toleransi_eror = 0.1
iterasi = 1

#inisialisasi data latih
data = np.array([[0.034,0.5,0.239]])

#inisialisasi target output
target_output = np.array([[0,0]])

# inisialisasi bobot V dan bobot W
V = np.array([[0.1, 0.1, 0.1],
             [0.2, 0.35, 0.1],
             [0.3, 0.27, 0.25],
             [0.1, 0.4, 0.35]])
W = np.array([[0.1, 0.1],
              [0.1, 0.25],
              [0.2, 0.2],
              [0.25, 0.15]])

print('--------------------------------------------------------')
print('           PARAMETER JST BACKPROPAGATION                ')
print('--------------------------------------------------------')
print('')
print('Neuron Input               : ',n_input)
print('Neuron Hidden              : ',n_hidden)
print('Neuron Output              : ',n_output)
print('Laju Pembelajaran (alpha)  : ',alpha)
print('Toleransi Eror             : ',toleransi_eror)
print('Iterasi                    : ',iterasi)
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


print('--------------------------------------------------------')
print('               PROSES PELATIHAN                         ')
n_datalatih=data.shape[0]
for i in range(iterasi):
    print('Iterasi ke-',(i+1))
    for j in range(n_datalatih):
        [Z,Y] = jst.PerambatanMaju(data[j,0:3],V,W,n_hidden,n_output)
        [W,V] = jst.PerambatanMundur(target_output[0],Y,data[j,0:3],alpha,Z,W,V)
        print('Z : ')
        print(Z)
        print('')
        print('Y : ')
        print(Y)
        print('')
        print('Bobot W baru : ')
        print(W)
        print('')
        print('Bobot V baru : ')
        print(V)
        print('')
