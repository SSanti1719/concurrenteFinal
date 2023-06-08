## Este Script contiene la solución al problema los espacios vacíos en el dotplot utilizando MPI.

from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import time
from Bio import SeqIO

begin = time.time()


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

cant_muestras = 150


def merge_sequences_from_fasta(file_path):
    sequences = []  # List to store all sequences
    for record in SeqIO.parse(file_path, "fasta"):
        # `record.seq` gives the sequence
        sequences.append(str(record.seq))
    return "".join(sequences)

SecuenciaLTR = "CACTAGACTAGACTAGCNAGCTACGCATGGCTACNCTACGACAGCTAGCTANCTATCNACTACNAGCTACTAGCTANNNACTANCTCGACTACGACTACACTGACCACTAGAC"*cant_muestras
file_path_1 = "E_coli.fna"
file_path_2 = "Salmonella.fna"
Secuencia1 = merge_sequences_from_fasta(file_path_1)
Secuencia2 = merge_sequences_from_fasta(file_path_2)
 # estas son las secuencias que se van a utilizar para el dotplot
Secuencia1=Secuencia1[0:10000]
Secuencia2=Secuencia2[0:10000]

"""Secuencia1 = "ACGTCGTCGAGCTAGCATCGATCAGNNNCATCATCNACTATACNNNNCATCATCATCTACTGCTACGACTACGAGAGAGCTACGACTACG"*cant_muestras
Secuencia2 = "NGCNATCACGATGCATGCACTACGATCGACAGCATCGATCGATGCATCATGCATCGNATGCNTGASCSATCGACGTANGCACTGACNTGA"*cant_muestras
Secuencia2 = Secuencia1"""


# Dividir la secuencia1 en chunks, uno por cada proceso.
chunks = np.array_split(range(len(Secuencia1)), size)

dotplot = np.empty([len(chunks[rank]),len(Secuencia2)],dtype=np.int8)

for i in range(len(chunks[rank])):
    for j in range(len(Secuencia2)):
        if Secuencia1[chunks[rank][i]] == Secuencia2[j]:
            dotplot[i,j] = np.int8(1)
        else:
            dotplot[i,j] = np.int8(0)

"""plt.figure(figsize=(10,10))
plt.imshow(dotplot, cmap='Greys',aspect='auto')
plt.savefig(f"ResultadoMPI_{rank}.png")"""

# gather data from all processes onto the root process
dotplot = comm.gather(dotplot, root=0)

# The root process prints the results and generates the plot.
if rank == 0: 
    #print("La matriz de resultado tiene tamaño: ", dotplot.shape)
    
    # merge the gathered data into a single array
    merged_data = np.vstack(dotplot)


    end = time.time()
    print(f"Tiempo total de ejecución: {end-begin} segundos")
    """for i in range(size):
        print(np.shape(dotplot[i]))"""

    plt.figure(figsize=(10,10))
    plt.imshow(merged_data[:500,:500], cmap='Greys',aspect='auto')
    plt.savefig(f"ResultadoMPI_{size}.png")