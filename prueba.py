import numpy as np 
import pandas as pd 
import csv
from math import sqrt


#ABRE ARCHIVO .csv Y LO CONVIERTE A UNA MATRIZ 150 x 5
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


#FASE DE APRENDIZAJE
#Calcula M 
def calcM(matriz):
    matri= np.asanyarray(np.delete(matriz, 4, axis = 1))
    filas = len(matri)
    columnas = len(matri[0])
    m = [] 
    for i in range(columnas):
        suma = sum([filas[i] for filas in matri])
        sM = (suma/filas)
        m.append(sM)
    
    return m 

#Calcula Y Retorna Los PatronesRepresentantes Usando calcM
def calcPatRep(matriz):
    matrizSetosa = np.asarray([fila for fila in matriz if fila[4] == 'Iris-setosa'])
    matrizVersi = np.asarray([fila for fila in matriz if fila[4] == 'Iris-versicolor'])
    matrizVir = np.asarray([fila for fila in matriz if fila[4] == 'Iris-virginica'])
    m1 = calcM(matrizSetosa)
    #m1.append('Iris-setosa')
    m2 = calcM(matrizVersi)
    #m2.append('Iris-versicolor')
    m3 = calcM(matrizVir)
    #m3.append('Iris-virginica')
    
    return m1, m2, m3

#PatronesRepresentantes A Partir De La Matriz De Aprendizaje mApren
m1, m2, m3 = calcPatRep(mApren) 


#FASE DE CLASIFICACION
#Calcula La Distancia Entre Dos Puntos
def calcDist(m, patron):
    suma = 0 
    for i in range(len(m)):
        suma += ((m[i] - patron[i]) ** 2)
    distancia = sqrt(suma)
    
    return distancia
        
#Calcula La M Con Menor Distancia Al Patron    
def retornaMenor(d1, d2, d3):
    menor = 0
    if(d1 < d2 and d1 < d3):
        menor = 1
    elif(d2 < d1 and d2 < d3):
        menor = 2
    elif(d3 < d2 and d3 < d1):
        menor = 3
    
    return menor  

#Clasifica El Patron De La Matriz De Prueba 
def asignaClas(matriz, m1, m2, m3):
    matriz2 = np.delete(matriz, 4, axis = 1)
    clase = []
    for i in range(len(matriz2)):
        a = calcDist(m1, list(matriz2[i]))
        b = calcDist(m2, list(matriz2[i]))
        c = calcDist(m3, list(matriz2[i]))
        menor = retornaMenor(a, b, c)
        if menor == 1:
            aux = list(matriz2[i])
            aux.append('Iris-setosa')
            clase.append(aux)
        elif menor == 2:
            aux = list(matriz2[i])
            aux.append('Iris-versicolor')
            clase.append(aux)
        elif menor == 3:
            aux = list(matriz2[i])
            aux.append('Iris-virginica')
            clase.append(aux)
    
    matrizC = np.asarray(clase) 
    return matrizC       
                       
mClasificada = asignaClas(mPrueba, m1, m2, m3) 

#Calcula errores
def errores(mApren, mClasificada):
    a = np.delete(mApren, (0, 1, 2, 3), axis = 1)
    b = np.delete(mClasificada, (0, 1, 2, 3), axis = 1)
    aciertos = 0
    errores = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            aciertos += 1
        else:
            errores += 1
    return aciertos, errores
        
aciertos, errores = errores(mPrueba, mClasificada)
