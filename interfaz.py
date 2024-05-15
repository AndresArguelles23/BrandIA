import tkinter as tk
from tkinter import ttk
import subprocess
import os
import threading

# Obtener la ruta del directorio de descargas
ruta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads', 'Lenguajes_senas')

def ejecutar_capturar():
    ejecutar_con_hilo(lambda: ejecutar_comando(os.path.join(ruta_descargas, 'capture_samples.py')), "Capturando muestras...")

def ejecutar_entrenar():
    ejecutar_con_hilo(lambda: ejecutar_comando(os.path.join(ruta_descargas, 'training_model.py')), "Entrenando modelo...")

def ejecutar_evaluar():
    ejecutar_con_hilo(lambda: ejecutar_comando(os.path.join(ruta_descargas, 'evaluate_model.py')), "Evaluando modelo...")

def ejecutar_keypoints():
    ejecutar_con_hilo(lambda: ejecutar_comando(os.path.join(ruta_descargas, 'create_keypoints.py')), "Creando keypoints...")

def ejecutar_con_hilo(funcion, mensaje):
    mensaje_estado.set(mensaje)
    threading.Thread(target=lambda: ejecutar_con_estado(funcion)).start()

def ejecutar_con_estado(funcion):
    try:
        funcion()
        mensaje_estado.set("Listo")
    except Exception as e:
        mensaje_estado.set("Error: " + str(e))

def ejecutar_comando(ruta):
    subprocess.run(["python", ruta], check=True)

def salir():
    root.destroy()

def ajustar_diseno(event):
    ancho = event.width
    alto = event.height
    if ancho < 600 or alto < 400:
        estilo_tamano_botones.configure('TButton', font=('Arial', 10))
    else:
        estilo_tamano_botones.configure('TButton', font=('Arial', 12))

root = tk.Tk()
root.title("BRAND TRADUCTOR DE LSC")
root.geometry("600x400")
# Estilo para ajustar el tamaño de los botones según el tamaño de la ventana
estilo_tamano_botones = ttk.Style()
root.bind("<Configure>", ajustar_diseno)

# Crear botones
boton_capturar = ttk.Button(root, text="Capturar Muestras", command=ejecutar_capturar)
boton_entrenar = ttk.Button(root, text="Entrenar Modelo", command=ejecutar_entrenar)
boton_evaluar = ttk.Button(root, text="Evaluar Modelo", command=ejecutar_evaluar)
boton_keypoints = ttk.Button(root, text="Crear Keypoints", command=ejecutar_keypoints)
boton_salir = ttk.Button(root, text="Salir", command=salir)

# Ajustar disposición de los botones
boton_capturar.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
boton_entrenar.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
boton_evaluar.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
boton_keypoints.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
boton_salir.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

# Crear etiqueta de estado
mensaje_estado = tk.StringVar()
mensaje_estado.set("Listo")
etiqueta_estado = ttk.Label(root, textvariable=mensaje_estado)
etiqueta_estado.pack(pady=5)

root.mainloop()
