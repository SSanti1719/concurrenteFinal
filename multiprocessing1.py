import numpy as np
import time
import matplotlib.pyplot as plt
import multiprocessing as mp
from tqdm import tqdm # esta librería es para mirar el progreso de un for
from Bio import SeqIO

def merge_sequences_from_fasta(file_path):
    sequences = []  # List to store all sequences
    for record in SeqIO.parse(file_path, "fasta"):
        # `record.seq` gives the sequence
        sequences.append(str(record.seq))
    return "".join(sequences)



def draw_dotplot(matrix,fig_name='dotplot.svg'):
  plt.figure(figsize=(5,5))
  plt.imshow(matrix, cmap='Greys',aspect='auto')

  plt.ylabel("Secuencia 1")
  plt.xlabel("Secuencia 2")
  plt.savefig(fig_name)

def worker(args):
    i, Secuencia1, Secuencia2 = args
    return [Secuencia1[i] == Secuencia2[j] for j in range(len(Secuencia2))]

def parallel_dotplot(Secuencia1, Secuencia2,threads):
    with mp.Pool(processes=threads) as pool:
        result = pool.map(worker, [(i, Secuencia1, Secuencia2) for i in range(len(Secuencia1))])
    return result

def dotplot_secuencial(sec1, sec2):
  dotplot = np.empty([len(sec1),len(sec2)],dtype=np.int8)
  #print("La matriz de resultado tiene tamaño: ", dotplot.shape)

  for i in range(dotplot.shape[0]):
    for j in range(dotplot.shape[1]):
      if sec1[i] == sec2[j]:
        dotplot[i,j] = 1
      else:
        dotplot[i,j] = 0

  return dotplot

def dotplot_multiprocessing(sec1,sec2,threads):
  dotplot = np.array(parallel_dotplot(sec1, sec2,threads), dtype=np.int8)
  return dotplot


if __name__ == '__main__':
    file_path_1 = "E_coli.fna"
    file_path_2 = "Salmonella.fna"

    merged_sequence_1 = merge_sequences_from_fasta(file_path_1) # estas son las secuencias que se van a utilizar para el dotplot
    merged_sequence_2 = merge_sequences_from_fasta(file_path_2)

    merged_sequence_1=merged_sequence_1[0:20000]
    merged_sequence_2=merged_sequence_2[0:20000]

    print("longitud Archivo 1:", len(merged_sequence_1))
    print("longitud Archivo 2:", len(merged_sequence_2))

    Secuencia1 = merged_sequence_1
    Secuencia2 = merged_sequence_2
    # Veamos el tiempo con 1 procesador
    # begin_secuencial = time.time()
    # dotplot_secuencial=dotplot_secuencial(Secuencia1, Secuencia2)
    # end_secuencial = time.time()

    # print(f"el tiempo secuencial es: {end_secuencial-begin_secuencial} ")

    # begin_paralelo = time.time()
    # dotplot_parallel=dotplot_multiprocessing(Secuencia1, Secuencia2,6)
    # end_paralelo = time.time()
    # print(f"el tiempo paralelo es: {end_paralelo-begin_paralelo} ")

    n_proc = [2,4,6,8]
    times = []  
    for i in n_proc:
        
        begin_paralelo = time.time()
        dotplot_multiprocessing(Secuencia1, Secuencia2,i)
        end_paralelo = time.time()
        times.append(end_paralelo-begin_paralelo)   
        print("Dotplot con ",i," procesadores, tiempo: ",end_paralelo-begin_paralelo)

    # plt.figure(figsize=(5,5))
    # plt.plot(n_proc,times)  
    # plt.xlabel("Número de procesadores")
    # plt.ylabel("Tiempo de ejecución")
    # plt.show()

    # acel = [times[0]/i for i in times]
    # efic = [acel[i]/n_proc[i] for i in range(len(n_proc))]
    # print("Aceleración: ",acel)
    # print("Eficiencia: ",efic)

    # plt.figure(figsize=(10,5))
    # plt.subplot(1,2,1)
    # plt.plot(n_proc,times)
    # plt.xlabel("Número de procesadores")
    # plt.ylabel("Tiempo de ejecución")
    # plt.subplot(1,2,2)
    # plt.plot(n_proc,acel)
    # plt.plot(n_proc,efic)
    # plt.xlabel("Número de procesadores")
    # plt.ylabel("Aceleración y eficiencia")
    # plt.legend(["Aceleración","Eficiencia"])
    # plt.show()

    # print("Aceleración Maxima: ",max(acel))
    # draw_dotplot(dotplot_secuencial[:500,:500 ],fig_name='dotplot_secuencial.svg')
    # draw_dotplot(dotplot_parallel[:500,:500 ],fig_name='dotplot_parallel.svg')