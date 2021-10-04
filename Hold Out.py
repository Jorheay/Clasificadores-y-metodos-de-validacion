import numpy as np 
import pandas as pd 
import csv
from math import sqrt


matriz = np.asarray( pd.read_csv("iris.csv", sep=',', header= None).values )

#METODO DE VALIDACIÓN
def holdOut(matriz):
    #SEPARA LA MATRIZ 150 x 5 EN 3 MATRICES DE 50 x 5 
    matriz_setosa = np.asarray([fila for fila in matriz if fila[4] == 'Iris-setosa'])
    matriz_versi = np.asarray([fila for fila in matriz if fila[4] == 'Iris-versicolor'])
    matriz_vir = np.asarray([fila for fila in matriz if fila[4] == 'Iris-virginica']) 
    
    #50 X R
    columnas = (matriz_setosa.shape[0]) 
    #print(columnas)
    porcentaje = int(input("introduce el porcentaje: ")) / 100
    #print(porcentaje)
    total = int(columnas * porcentaje)
    #print(total) 

    #TOMAR LOS PRIMEROS 35 DE CADA UNA DE LAS 3 MATRICES (35 X 5)
    setosa = np.asarray([fila for fila in matriz_setosa[0 : total]])
    versi = np.asarray([fila for fila in matriz_versi[0 : total]])
    vir = np.asarray([fila for fila in matriz_vir[0 : total]])

    #CONCATENAR LAS TRES MATRICES GENERANDO (105 X 5)
    aprendizaje = np.asarray(np.concatenate((setosa, versi, vir), axis = 0)) 

    #TOMAR LOS ULTIMOS 15 DE CADA MATRIZ (15 X 5)
    uSetosa = np.asarray([fila for fila in matriz_setosa[total : ]])
    uVersi = np.asarray([fila for fila in matriz_versi[total :]])
    uVir = np.asarray([fila for fila in matriz_vir[total : ]])

    #CONCATENAR LAS MATRICES (45 X 5)
    prueba = np.asarray(np.concatenate((uSetosa, uVersi, uVir), axis = 0))
    
    return aprendizaje, prueba

#Matrices De Prueba Y Aprendizaje
mApren, mPrueba = holdOut(matriz)

def calcDist(m, patron):
    pat = np.delete(patron, 4)
    suma = 0 
    for i in range(len(m)):
        suma += ((m[i] - float(pat[i])) ** 2)
    distancia = sqrt(suma)
    
    return distancia

def votacion(matriz, patron, k):
    setosa = 0
    vir = 0
    ver = 0
    vot = np.asarray([fila for fila in matriz[0 : k]])
    for i in range(len(vot)):
        aux = list(vot[i])
        if aux[1] == 'Iris-setosa' :
            setosa += 1
        elif aux[1] == 'Iris-versicolor' :
            ver += 1
        elif aux[1] == 'Iris-virginica' :
            vir += 1
    
    if(setosa > ver and setosa > vir):
        patron.append('Iris-setosa')
    elif(ver > setosa and ver > vir):
        patron.append('Iris-versicolor')
    elif(vir > setosa and vir > ver):
        patron.append('Iris-virginica')
            
    return patron

def distancias(mPrueba, mApren):
    clsificado = []
    matriz = np.delete(mPrueba, 4, axis = 1)
    k = int(input("Introduce el valor de K: "))
    for i in range(len(matriz)):
        clases = []
        patron = list(matriz[i])
        for j in range(len(mApren)):
            dist = []
            distancia = calcDist(patron, list(mApren[j]))
            dist.append(distancia)
            aux = list(mApren[j])
            dist.append(aux[4])
            clases.append(dist) 
        mClas = np.asarray(clases)
        orden = mClas[np.argsort(mClas[:,0])]
        nueva = votacion(orden, patron, k)
        clsificado.append(nueva)
    final = np.asarray(clsificado)
                      
distancias(mPrueba, mApren)
    