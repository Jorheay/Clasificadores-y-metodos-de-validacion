import numpy as np 
import pandas as pd 
import csv
from math import sqrt

matriz1 = np.asarray( pd.read_csv("Iris.csv", sep=',', header= None).values )
valor_k = int(input("Ingresa el valor de K : ")) 

def calcDist(m, patron):
    pat = np.delete(patron, 4)
    suma = 0 
    for i in range(len(m)):
        suma += ((m[i] - float(pat[i])) ** 2)
    distancia = sqrt(suma)
    
    return distancia

#Fase de Aprendizaje 
def promedio(matriz):
    #vamos a eliminar la columna final
    matriz2 = np.delete(matriz, 4, axis=1)
    filas = len(matriz2)
    columnas = len(matriz2[0])
    M = []
    for i in range(columnas):
        suma = sum([filas[i] for filas in matriz2])
        sm = (suma / filas)
        M.append(sm)


        
    return M

    
    
def calcula_represen(matriz):
    matriz_setosa = np.asarray([fila for fila in matriz if fila[4] == 'Iris-setosa'])
    matriz_versi = np.asarray([fila for fila in matriz if fila[4] == 'Iris-versicolor'])
    matriz_vir = np.asarray([fila for fila in matriz if fila[4] == 'Iris-virginica']) 
    #m1,m2,m3 son los patrones representantes 
    
    m1 = list(promedio(matriz_setosa))
    #m1.append('Iris-setosa')
    m2 = list(promedio(matriz_versi))
    #m2.append('Iris-versicolor')
    m3 = list(promedio(matriz_vir))
    #m3.append('Iris-virginica')
    #print("El valor de m1: ",m1)
    #print("El valor de m2: ",m2)
    #print("El valor de m3: ",m3)

  
    return m1, m2, m3

    

def distancias_entrePuntos(patron, m ):
    suma = 0
    for i in range(len(patron)):
        suma += ((patron[i] - m[i])**2)
        
        
    distancia = sqrt(suma)

    return distancia



def comparacion(dis1,dis2,dis3):
    menor=0
    if(dis1 < dis2 and dis1 < dis3): 
        menor= 1
    elif(dis2 < dis1 and dis2 < dis3):
        menor = 2
    elif(dis3 < dis1 and dis3 < dis2):
        menor = 3
    
    
    return menor


def clasificador (m1,m2,m3,matrizprue):
    aux = []
    matriz = np.delete(matrizprue, 4, axis = 1)
    for i in range(len(matriz)): 
        distancia1 = distancias_entrePuntos(m1, list(matriz[i]))
        distancia2 = distancias_entrePuntos(m2, list(matriz[i]))
        distancia3 = distancias_entrePuntos(m3, list(matriz[i]))
        comp = comparacion(distancia1,distancia2,distancia3)
        if comp == 1:
            auxi = list(matriz[i])
            auxi.append('Iris-setosa')
            aux.append(auxi)
        elif comp == 2:
            auxi = list(matriz[i])
            auxi.append('Iris-versicolor')
            aux.append(auxi)
        elif comp == 3:
            auxi = list(matriz[i])
            auxi.append('Iris-virginica')
            aux.append(auxi)
            
    matrizClasificada = np.asarray(aux)

    return matrizClasificada  



def cuantificador(matrizClasificada, matrizprue):
    matriz1 = np.delete(matrizprue, (0,1,2,3), axis=1)
    matriz2 = np.delete(matrizClasificada, (0,1,2,3), axis=1)
    aciertos = 0
    errores = 0
    for i in range(len(matriz1)):
        if matriz1[i] == matriz2[i]:
            aciertos += 1
        else:
            errores += 1
                
                
    #print("Numero de aciertos: ",aciertos)
    #print("Numero de errores: ",errores)            
    return aciertos 

def rendimento(aciertos, matrizprue): 
    numPatrones = len(matrizprue)
    exito = (aciertos / numPatrones) * 100 
    
    #print("Rendimeinto: ",exito,"%")
    return  exito

def metodo(matriz1, valor_k, iteracion):
    
    matrizCA, matrizCP = [] , []
    
    clase1, clase2, clase3 = np.vsplit(matriz1, 3)
    matriz1 = np.vsplit(clase1, valor_k)
    matriz2 = np.vsplit(clase2, valor_k)
    matriz3 = np.vsplit(clase3, valor_k)
    contador = 0
    for m1 in matriz1: 
        if contador == iteracion:
            matrizCP.append(m1)
        else:
            matrizCA.append(m1)
        contador = contador + 1
    contador = 0
    for m2 in matriz2: 
        if contador == iteracion:
            matrizCP.append(m2)
        else:
            matrizCA.append(m2)
        contador = contador + 1
    contador = 0
    for m3 in matriz3:
        if contador == iteracion: 
            matrizCP.append(m3)
        else: 
            matrizCA.append(m3)
        contador = contador + 1
    return matrizCA, matrizCP

def recorre(): 
    suma = 0
    for i in range(valor_k): 
        matrizCA, matrizCP = metodo(matriz1, valor_k, i)
        Conjunto_Apren = np.array(matrizCA)
        Conjunto_Prueba = np.array(matrizCP)
        apren = np.concatenate((Conjunto_Apren), axis = 0)
        prueba = np.concatenate((Conjunto_Prueba), axis = 0)
        m1, m2, m3 = calcula_represen(apren)
        clasificacion = clasificador(m1, m2, m3, prueba) 
        aciertos = cuantificador(clasificacion, prueba) 
        suma += rendimento(aciertos, prueba)
        total = (suma/ valor_k)
    print("Porcentaje de exito: ", total , "%")
        #print("\n Conjunto de Prueba ", i+1, "\n", prueba)
        #print("\n Conjunto clacificado es  ", i+1, "\n", clasificacion) 

if len(matriz1) % valor_k == 0: 
    recorre()
else:
    print("Ingresa otro valor que sea Divisible")