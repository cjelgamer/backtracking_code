import tkinter as tk
from tkinter import messagebox
import time
import numpy as np


class NReinasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema de N-Reinas")
        self.root.geometry("700x700")
        self.root.configure(bg="#2C3E50")

        # Título de la aplicación
        self.title_label = tk.Label(
            root,
            text="N-Reinas",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.title_label.pack(pady=5)

        # Entrada para el número de reinas
        self.input_frame = tk.Frame(root, bg="#2C3E50")
        self.input_frame.pack(pady=5)

        self.label = tk.Label(
            self.input_frame,
            text="N:",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.label.grid(row=0, column=0, padx=5)

        self.n_entry = tk.Entry(self.input_frame, width=5, font=("Arial", 10))
        self.n_entry.grid(row=0, column=1, padx=5)

        # Slider para controlar la velocidad
        self.speed_label = tk.Label(
            root,
            text="Velocidad:",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.speed_label.pack(pady=5)

        self.speed_slider = tk.Scale(
            root,
            from_=1,
            to=1000,
            orient=tk.HORIZONTAL,
            bg="#34495E",
            fg="#ECF0F1",
            length=250,
            font=("Arial", 8)
        )
        self.speed_slider.set(200)  # Valor inicial
        self.speed_slider.pack()

        # Botón para mostrar el tablero inicial
        self.show_button = tk.Button(
            root,
            text="Tablero",
            command=self.inicializar_tablero,
            font=("Arial", 10),
            bg="#1ABC9C",
            fg="#2C3E50",
            relief="raised",
            bd=2,
            cursor="hand2"
        )
        self.show_button.pack(pady=5)

        # Botón para resolver
        self.solve_button = tk.Button(
            root,
            text="Resolver",
            command=self.iniciar_resolucion,
            font=("Arial", 10),
            bg="#E74C3C",
            fg="#ECF0F1",
            relief="raised",
            bd=2,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.solve_button.pack(pady=5)

        # Mostrar las iteraciones
        self.iteration_label = tk.Label(
            root,
            text="Iteraciones: 0",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.iteration_label.pack(pady=10)

        # Canvas para el tablero
        self.canvas = None
        self.tablero = None
        self.n = 0
        self.solucion_encontrada = False  # Para controlar el bucle
        self.iterations = 0  # Contador de iteraciones

    def inicializar_tablero(self):
        try:
            # Obtener el número de reinas
            self.n = int(self.n_entry.get())
            if self.n < 1:
                raise ValueError("El número de reinas debe ser mayor o igual a 1.")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return

        # Limpiar el canvas si ya existe
        if self.canvas:
            self.canvas.destroy()

        # Crear el tablero inicial
        self.tablero = np.zeros((self.n, self.n), dtype=int)
        self.mostrar_tablero(self.tablero, self.n)
        self.solve_button.config(state=tk.NORMAL)  # Activar botón de resolución
        self.solucion_encontrada = False  # Reiniciar el estado de solución
        self.iterations = 0  # Reiniciar el contador de iteraciones
        self.iteration_label.config(text=f"Iteraciones: {self.iterations}")  # Actualizar la interfaz

    def iniciar_resolucion(self):
        self.solucion_encontrada = self.resolver_reinas(self.tablero, 0, self.n)
        if not self.solucion_encontrada:
            messagebox.showinfo("Sin Solución", "No hay solución para el número de reinas ingresado.")

    def resolver_reinas(self, tablero, col, N):
        # Caso base: todas las reinas están colocadas
        if col >= N:
            return True

        # Intentar colocar una reina en cada fila de la columna actual
        for i in range(N):
            self.iterations += 1  # Incrementar el contador de iteraciones
            self.iteration_label.config(text=f"Iteraciones: {self.iterations}")  # Actualizar la interfaz

            if self.es_seguro(tablero, i, col, N):
                # Colocar una reina
                tablero[i][col] = 1
                self.mostrar_tablero(tablero, N)
                self.root.update()  # Actualizar la interfaz gráfica
                time.sleep(self.speed_slider.get() / 1000)  # Ajustar velocidad

                # Intentar colocar reinas en las siguientes columnas
                if self.resolver_reinas(tablero, col + 1, N):
                    return True

                # Si no es posible, retirar la reina (backtracking)
                tablero[i][col] = 0
                self.mostrar_tablero(tablero, N)
                self.root.update()
                time.sleep(self.speed_slider.get() / 1000)

        return False

    def es_seguro(self, tablero, fila, col, N):
        # Verificar la misma columna hacia arriba
        for i in range(col):
            if tablero[fila][i] == 1:
                return False

        # Verificar la diagonal superior izquierda
        for i, j in zip(range(fila, -1, -1), range(col, -1, -1)):
            if tablero[i][j] == 1:
                return False

        # Verificar la diagonal superior derecha
        for i, j in zip(range(fila, N), range(col, -1, -1)):
            if tablero[i][j] == 1:
                return False

        return True

    def mostrar_tablero(self, tablero, n):
        # Obtener las dimensiones de la ventana disponibles
        max_width = self.root.winfo_width() - 20
        max_height = self.root.winfo_height() - 270

        # Asegurar que el tablero sea cuadrado y se ajuste al espacio
        cell_size = min(max_width // n, max_height // n)
        tablero_size = cell_size * n

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.root, width=tablero_size, height=tablero_size, bg="#2C3E50", highlightthickness=0)
        self.canvas.pack(pady=5)

        # Dibujar el tablero
        for i in range(n):
            for j in range(n):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "#ECF0F1" if (i + j) % 2 == 0 else "#34495E"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#2C3E50")
                if tablero[i][j] == 1:
                    self.canvas.create_oval(
                        x1 + cell_size * 0.2,
                        y1 + cell_size * 0.2,
                        x2 - cell_size * 0.2,
                        y2 - cell_size * 0.2,
                        fill="#E74C3C"
                    )


# Ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    app = NReinasApp(root)
    root.mainloop()
