import numpy as np 
import pandas as pd 
import csv
from math import sqrt

matriz1 = np.asarray( pd.read_csv("iris.csv", sep=',', header= None).values )
 
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

def distancias(mPrueba, mApren, k):
    clsificado = []
    matriz = np.delete(mPrueba, 4)
    clases = []
    patron = list(matriz)
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
    return nueva

def metodo_uno(matriz1,iteracion):
    i = int(iteracion)
    matriz_prueba = np.asarray( matriz1[i])
    matriz_apren = np.asarray (np.delete(matriz1, i, axis=0))
    return matriz_apren, matriz_prueba
    
def metodo_dos():
    mNueva = []   
    k = int(input("Introduce el valor de K: "))     
    for i in range(int(matriz1.shape[0])):
        matrizAprendizaje, matrizPrueba = metodo_uno(matriz1, i)
        clas = distancias(matrizPrueba, matrizAprendizaje, k)
        mNueva.append(clas)
    final = np.asarray(mNueva)
    return final
        
final = metodo_dos() 
print(final)