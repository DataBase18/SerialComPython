import tkinter as tk
from tkinter import scrolledtext
 
ESPPAnel  = tk.Frame()

 
# Crear un campo de entrada (Input)
entrada = tk.Entry(ESPPAnel, font=("Arial", 14), width=20)
entrada.pack(pady=10)


# Crear un botón
boton = tk.Button(ESPPAnel, text="Conectar", font=("Arial", 12))
boton.pack(pady=10)

 