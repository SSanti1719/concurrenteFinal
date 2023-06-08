# Análisis de Rendimiento de Dotplot Secuencial vs. Paralelización
Proyecto diseñado para analizar tres formas de implementación (Secuencial, Paralela, mpi4py) de un dotplot utilizado para la comparación de dos secuencias de ADN
# Instalacion 
Para ejecutar el programa se debe configurar un entorno de desarrollo en Python con los siguientes comandos:
- Inicie un entorno virtual en python en la carpeta raíz del repo con el siguiente comando.
    py -m venv venv
- Active el entorno virtual del proyecto si está en la terminal de windows con el siguiente comando.
   venv\Scripts\activate
## Uso
1.	Los archivos FASTA que contienen las secuencias de ADN deben estar en la misma carpeta que el programa principal
2.	Para ejecutar el programa se usa el siguiente comando:
multiprocessing1.py
3.	El programa comenzara su ejecución mostrando los tiempos que tarda en ejecutar los dotplot y posteriormente mostrara en pantalla los diferentes graficos de los análisis respectivos.
4.	Al finalizar se generara un archivo .svg con la imagen de la matriz de puntos dotplot.svg
