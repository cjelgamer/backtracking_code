import numpy as np
import time

class SudokuSolver:

    def __init__(self, sudoku):
        self.restricciones = np.ones((9, 9, 9), dtype=bool)
        self.sudoku = np.zeros((9, 9), dtype=int)
        for fila in range(9):
            for columna in range(9):
                if sudoku[fila][columna] != 0:
                    self.colocar_numero(fila, columna, sudoku[fila][columna])

    def solve(self):
        inicio = time.time()
        self.backtracking()
        fin = time.time()
        print(f"Tiempo de resolución: {fin - inicio} segundos.")
        return self.sudoku

    def backtracking(self):
        if self.esta_resuelto():
            return self.sudoku

        fila, columna = self.celda_menos_opciones()

        for numero in range(1, 10):
            if self.puede_colocar(fila, columna, numero):
                estado_anterior = self.restricciones.copy()
                sudoku_anterior = self.sudoku.copy()
                self.colocar_numero(fila, columna, numero)
                self.movimientos_obvios()

                if self.backtracking() is not None:
                    return self.sudoku

                self.restricciones = estado_anterior
                self.sudoku = sudoku_anterior

        return None

    def esta_resuelto(self):
        return np.sum(self.sudoku == 0) == 0

    def celda_menos_opciones(self):
        opciones = np.sum(self.restricciones, axis=2)
        opciones[opciones == 0] = 10
        indices = np.unravel_index(np.argmin(opciones), opciones.shape)
        return indices

    def puede_colocar(self, fila, columna, numero):
        return self.restricciones[fila, columna, numero - 1]

    def colocar_numero(self, fila, columna, numero):
        self.sudoku[fila, columna] = numero
        self.restricciones[fila, columna] = np.zeros(9, dtype=bool)
        for k in range(9):
            self.restricciones[fila, k, numero - 1] = False
            self.restricciones[k, columna, numero - 1] = False

        for i in range(3):
            for j in range(3):
                self.restricciones[fila // 3 * 3 + i, columna // 3 * 3 + j, numero - 1] = False

    def movimientos_obvios(self):
        cambio = True
        while cambio:
            cambio = False
            for fila in range(9):
                for columna in range(9):
                    if self.es_celda_obvia(fila, columna):
                        cambio = True
                        self.colocar_numero(fila, columna, np.argmax(self.restricciones[fila, columna]) + 1)

    def es_celda_obvia(self, fila, columna):
        return self.sudoku[fila, columna] == 0 and np.sum(self.restricciones[fila, columna]) == 1
