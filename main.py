import os
import shutil
import threading
import time
import tkinter as tk

running = False

def filtrar_archivos(palabra_clave):
    files = os.listdir()
    return [file for file in files if file.startswith(palabra_clave)]


def crear_carpeta(nombre_carpeta):
    if not os.path.exists(nombre_carpeta):
        os.mkdir(nombre_carpeta)


def mover_archivos(palabra_clave, carpeta_destino):
    archivos_a_mover = filtrar_archivos(palabra_clave)
    for archivo in archivos_a_mover:
        ruta_archivo = os.path.join(os.getcwd(), archivo)
        ruta_destino = os.path.join(os.getcwd(), carpeta_destino, archivo)
        shutil.move(ruta_archivo, ruta_destino)
        print(f"Archivo '{archivo}' movido a '{carpeta_destino}'.")


def organizar_escritorio(palabra_clave, carpeta_destino , tiempo_espera = 60):
    desktop_path = r"C:\Users\fabia\OneDrive\Escritorio"
    os.chdir(desktop_path)
    crear_carpeta(carpeta_destino)

    while running:
        mover_archivos(palabra_clave, carpeta_destino)
        
        time.sleep(tiempo_espera) 

def iniciar_organizacion():
    global running, thread
    
    if not running:
        print(running)
        running = True
        palabra_clave = entry_palabra_clave.get()
        print(palabra_clave)
        carpeta_destino = entry_carpeta_destino.get()
        print(carpeta_destino)
        thread = threading.Thread(target=organizar_escritorio, args=(palabra_clave, carpeta_destino , 1))
        thread.start()

def detener_organizacion():
    global running
    running = False
    if thread and thread.is_alive():
        thread.join()

def crear_interfaz(root):
    tk.Label(root, text="Organizador de Escritorio").pack()

    # Campo para palabra clave
    tk.Label(root, text="Palabra clave para mover:").pack()

    global entry_palabra_clave

    entry_palabra_clave = tk.Entry(root)
    entry_palabra_clave.insert(0, "proyecto")  # Valor por defecto
    entry_palabra_clave.pack()

    # Campo para carpeta destino
    tk.Label(root, text="Carpeta destino:").pack()
    global entry_carpeta_destino
    entry_carpeta_destino = tk.Entry(root)
    entry_carpeta_destino.insert(0, "NuevaCarpeta")  # Valor por defecto
    entry_carpeta_destino.pack()

    # Botones de iniciar y detener
    tk.Button(root, text="Iniciar", command=iniciar_organizacion).pack()
    tk.Button(root, text="Detener", command=detener_organizacion).pack()


root = tk.Tk()
root.minsize(400,400)
root.title("Organizador de archivos")
crear_interfaz(root)
root.mainloop()
