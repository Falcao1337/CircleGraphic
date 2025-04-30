import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math

class PolygonTransformer:
    def __init__(self, root):
        self.root = root
        self.root.title("Transformador de Polígonos")
        
        # Configurações iniciais
        self.num_sides = 3
        self.scale_factor = 1.0
        self.rotation_angle = 0
        self.translation_x = 0
        self.translation_y = 0
        self.shear_x = 0
        self.shear_y = 0
        
        # Criar figura matplotlib
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        
        # Criar canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=10)
        
        # Controles
        controls_frame = ttk.Frame(self.root)
        controls_frame.grid(row=0, column=0, sticky="n", padx=10)
        
        # Número de lados
        ttk.Label(controls_frame, text="Número de lados:").pack()
        self.sides_var = tk.StringVar(value="3")
        sides_entry = ttk.Entry(controls_frame, textvariable=self.sides_var)
        sides_entry.pack()
        
        # Botões de transformação
        ttk.Label(controls_frame, text="\nTranslação").pack()
        ttk.Button(controls_frame, text="↑", command=lambda: self.translate(0, 0.1)).pack()
        ttk.Button(controls_frame, text="↓", command=lambda: self.translate(0, -0.1)).pack()
        ttk.Button(controls_frame, text="←", command=lambda: self.translate(-0.1, 0)).pack()
        ttk.Button(controls_frame, text="→", command=lambda: self.translate(0.1, 0)).pack()
        
        ttk.Label(controls_frame, text="\nRotação").pack()
        ttk.Button(controls_frame, text="Girar +", command=lambda: self.rotate(10)).pack()
        ttk.Button(controls_frame, text="Girar -", command=lambda: self.rotate(-10)).pack()
        
        ttk.Label(controls_frame, text="\nEscala").pack()
        ttk.Button(controls_frame, text="Aumentar", command=lambda: self.scale(1.1)).pack()
        ttk.Button(controls_frame, text="Diminuir", command=lambda: self.scale(0.9)).pack()
        
        ttk.Label(controls_frame, text="\nCisalhamento").pack()
        ttk.Button(controls_frame, text="X +", command=lambda: self.shear(0.1, 0)).pack()
        ttk.Button(controls_frame, text="X -", command=lambda: self.shear(-0.1, 0)).pack()
        ttk.Button(controls_frame, text="Y +", command=lambda: self.shear(0, 0.1)).pack()
        ttk.Button(controls_frame, text="Y -", command=lambda: self.shear(0, -0.1)).pack()
        
        # Botão para criar círculo/elipse
        ttk.Button(controls_frame, text="Criar Círculo (100 lados)", 
                  command=lambda: self.set_sides(100)).pack(pady=10)
        
        # Atualizar o polígono inicial
        self.sides_var.trace("w", self.update_sides)
        self.draw_polygon()
    
    def get_polygon_points(self):
        points = []
        radius = 1
        for i in range(self.num_sides):
            angle = (2 * math.pi * i / self.num_sides) + math.radians(self.rotation_angle)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append([x, y, 1])  # Coordenadas homogêneas
        return np.array(points)
    
    def apply_transformation(self, points):
        # Matriz de translação
        T = np.array([
            [1, 0, self.translation_x],
            [0, 1, self.translation_y],
            [0, 0, 1]
        ])
        
        # Matriz de escala
        S = np.array([
            [self.scale_factor, 0, 0],
            [0, self.scale_factor, 0],
            [0, 0, 1]
        ])
        
        # Matriz de cisalhamento
        Sh = np.array([
            [1, self.shear_x, 0],
            [self.shear_y, 1, 0],
            [0, 0, 1]
        ])
        
        # Aplicar transformações
        transformed_points = points.dot(T.T).dot(S.T).dot(Sh.T)
        return transformed_points
    
    def draw_polygon(self):
        self.ax.clear()
        points = self.get_polygon_points()
        transformed_points = self.apply_transformation(points)
        
        # Desenhar o polígono
        x = transformed_points[:, 0]
        y = transformed_points[:, 1]
        x = np.append(x, x[0])  # Fechar o polígono
        y = np.append(y, y[0])
        self.ax.plot(x, y, 'b-')
        
        # Configurar limites e aspecto
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        
        self.canvas.draw()
    
    def translate(self, dx, dy):
        self.translation_x += dx
        self.translation_y += dy
        self.draw_polygon()
    
    def rotate(self, angle):
        self.rotation_angle += angle
        self.draw_polygon()
    
    def scale(self, factor):
        self.scale_factor *= factor
        self.draw_polygon()
    
    def shear(self, sx, sy):
        self.shear_x += sx
        self.shear_y += sy
        self.draw_polygon()
    
    def set_sides(self, num):
        self.sides_var.set(str(num))
    
    def update_sides(self, *args):
        try:
            new_sides = int(self.sides_var.get())
            if new_sides >= 3:
                self.num_sides = new_sides
                self.draw_polygon()
        except ValueError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonTransformer(root)
    root.mainloop()