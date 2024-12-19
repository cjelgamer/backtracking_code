import cv2 #procesamiento de imágenes
import skimage #mejorando la precisión del reconocimiento
import numpy as np#Para manejar arreglos y matrices
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import pyautogui #escribir los nueros en el sitio web
from SudokuSolver import SudokuSolver


def main():
    # Cambiar al navegador donde está abierto Sudoku.com usando Alt+Tab
    pyautogui.hotkey("alt", "tab", interval=0.1)
    
    # Tomar una captura de pantalla de la pantalla completa
    captura_pantalla = pyautogui.screenshot()
    captura_pantalla = cv2.cvtColor(np.array(captura_pantalla), cv2.COLOR_RGB2BGR)
    
    # Preprocesar la imagen para detectar el Sudoku
    imagen_preprocesada = preprocesar(captura_pantalla)
    contorno_sudoku = encontrar_contorno_sudoku(imagen_preprocesada)
    
    if contorno_sudoku is None:
        print("No se encontró un Sudoku en la imagen.")
        return
    
    # Recortar la cuadrícula del Sudoku
    sudoku_recortado = recortar_cuadricula(captura_pantalla, contorno_sudoku)
    
    # Dividir la cuadrícula en las 81 celdas y detectar los números
    imagenes_celdas = dividir_cuadricula(sudoku_recortado)
    sudoku_inicial = celdas_a_sudoku(imagenes_celdas)
    
    # Resolver el Sudoku
    solucionador = SudokuSolver(sudoku_inicial)
    sudoku_resuelto = solucionador.solve()
    
    # Escribir la solución directamente en el sitio web
    resolver_en_pagina(contorno_sudoku, sudoku_resuelto)


# -- Procesamiento de imagen
def preprocesar(imagen):
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    desenfoque = cv2.GaussianBlur(imagen_gris, (5, 5), 0)
    umbral = cv2.threshold(desenfoque, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return umbral

def encontrar_contorno_sudoku(imagen_preprocesada):
    contornos, _ = cv2.findContours(imagen_preprocesada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cuadrados = [contorno for contorno in contornos if es_cuadrado(contorno)]
    cuadrados = sorted(cuadrados, key=cv2.contourArea, reverse=True)
    if len(cuadrados) == 0:
        return None
    return cuadrados[0]

def es_cuadrado(contorno):
    aproximacion = cv2.approxPolyDP(contorno, 0.01 * cv2.arcLength(contorno, True), True)
    _, _, ancho, alto = cv2.boundingRect(aproximacion)
    razon_aspecto = ancho / float(alto)
    return len(aproximacion) == 4 and abs(razon_aspecto - 1) < 0.1

def recortar_cuadricula(imagen, contorno):
    x, y, ancho, alto = cv2.boundingRect(contorno)
    return imagen[y:y+alto, x:x+ancho]

def dividir_cuadricula(sudoku_recortado):
    imagen = preprocesar(sudoku_recortado)
    imagen = skimage.segmentation.clear_border(imagen)
    imagen = 255 - imagen
    alto, _ = imagen.shape
    tamano_celda = alto // 9
    celdas = []
    for i in range(9):
        for j in range(9):
            celda = imagen[i*tamano_celda:(i+1)*tamano_celda, j*tamano_celda:(j+1)*tamano_celda]
            celda = cv2.resize(celda, (55, 55), interpolation=cv2.INTER_AREA)
            celdas.append(celda)
    return celdas


# -- Modelo de aprendizaje automático
def celdas_a_sudoku(celdas):
    modelo_knn = crear_modelo_knn()
    sudoku = np.zeros((81), dtype=int)
    for i, celda in enumerate(celdas):
        sudoku[i] = predecir_digito(celda, modelo_knn)
    return sudoku.reshape(9, 9)

def predecir_digito(imagen, modelo_knn):
    vector_imagen = imagen.reshape(1, -1)
    prediccion = modelo_knn.predict(vector_imagen)[0]
    return prediccion

def crear_modelo_knn():
    datos = pd.read_csv("dataset.csv")
    X = datos.iloc[:, :-1].values
    y = datos.iloc[:, -1].values
    modelo_knn = KNeighborsClassifier(n_neighbors=1)
    modelo_knn.fit(X, y)
    return modelo_knn


# -- Interacción con la página web
def resolver_en_pagina(contorno, sudoku_resuelto):
    x, y, ancho, alto = cv2.boundingRect(contorno)
    tamano_celda = alto // 9
    for i in range(9):
        for j in range(9):
            pyautogui.click(x + j*tamano_celda + tamano_celda//2, y + i*tamano_celda + tamano_celda//2, _pause=False)
            pyautogui.press(str(sudoku_resuelto[i, j]), _pause=False)


if __name__ == '__main__':
    main()
