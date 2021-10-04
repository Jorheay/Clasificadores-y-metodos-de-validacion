# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 13:22:08 2021

@author: gamak
"""
import numpy as np 
import pandas as pd 
import csv
from math import sqrt

matriz1 = np.asarray( pd.read_csv("Iris.csv", sep=',', header= None).values )
 
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
    #aux = []
    matriz = np.delete(matrizprue, 4)
    distancia1 = distancias_entrePuntos(m1, list(matriz))
    distancia2 = distancias_entrePuntos(m2, list(matriz))
    distancia3 = distancias_entrePuntos(m3, list(matriz))
    comp = comparacion(distancia1,distancia2,distancia3)
    if comp == 1:
        auxi = list(matriz)
        auxi.append('Iris-setosa')
        return auxi
        #aux.append(auxi)
    elif comp == 2:
        auxi = list(matriz)
        auxi.append('Iris-versicolor')
        return auxi
        #aux.append(auxi)
    elif comp == 3:
        auxi = list(matriz)
        auxi.append('Iris-virginica')
        return auxi
        #aux.append(auxi)
            
    #matrizClasificada = np.asarray(aux)

    #return aux  



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
                
                
    print("Numero de aciertos: ",aciertos)
    print("Numero de errores: ",errores)            
    return aciertos, errores 

def rendimento(aciertos, matrizprue): 
    numPatrones = len(matrizprue)
    exito = (aciertos / numPatrones) * 100 
    
    print("Rendimeinto: ",exito,"%")
    return  exito

def metodo_uno(matriz1,iteracion):
    i = int(iteracion)
    matriz_prueba = np.asarray( matriz1[i])
    matriz_apren = np.asarray (np.delete(matriz1, i, axis=0))
    return matriz_apren, matriz_prueba
    

def metodo_dos():  
    lista = []    
    
    for i in range(int(matriz1.shape[0])):
        matrizAprendizaje, matrizPrueba = metodo_uno(matriz1, i)
        #eliminar = np.delete(matrizPrueba, 4, axis=1)
        m1, m2, m3 = calcula_represen(matrizAprendizaje)
        clasificacion = clasificador(m1, m2, m3, matrizPrueba)
        lista.append(clasificacion)
    mat = np.asarray(lista)
    #print(mat)  
    return mat      
     
                
nueva = metodo_dos() 

aciertos, errores = cuantificador(nueva, matriz1)

rendimento(aciertos, matriz1)












