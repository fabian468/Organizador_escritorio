import os
import shutil
import threading
import time
import sqlite3
import tkinter as tk

running = False
thread = None 

def obtener_ruta_db():
    return os.path.join(os.path.dirname(__file__), 'config.db')

def iniciar_db():
    conn = sqlite3.connect(obtener_ruta_db())  
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuraciones (
                        id INTEGER PRIMARY KEY,
                        carpeta_destino TEXT NOT NULL,
                        palabra_clave TEXT NOT NULL, 
                        ordenando BOOLEAN NOT NULL
                    )''')
    conn.commit()
    conn.close()

def guardar_configuracion_bd(carpeta_destino, palabra_clave, ordenando=True):
    conn = sqlite3.connect(obtener_ruta_db())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO configuraciones (carpeta_destino, palabra_clave, ordenando) VALUES (?, ?, ?)", 
                   (carpeta_destino, palabra_clave, ordenando))
    conn.commit()
    conn.close()

def cargar_configuraciones():
    conn = sqlite3.connect(obtener_ruta_db())
    cursor = conn.cursor()
    cursor.execute("SELECT carpeta_destino, palabra_clave, ordenando, id FROM configuraciones")
    configuraciones = cursor.fetchall()
    conn.close()
    return configuraciones

def eliminar_configuracion_bd(idConfig):
    conn = sqlite3.connect(obtener_ruta_db())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM configuraciones WHERE id = ?", (idConfig,))
    conn.commit()
    conn.close()
    actualizar_interfaz()
    iniciar_organizacion(True)

def editar_ordenando_por_id(config_id, nuevo_ordenando):
    conn = sqlite3.connect(obtener_ruta_db())
    cursor = conn.cursor()
    cursor.execute("UPDATE configuraciones SET ordenando = ? WHERE id = ?", 
                   (nuevo_ordenando, config_id))
    conn.commit()
    conn.close()
    actualizar_interfaz()
    iniciar_organizacion(True)

#========================================================================

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

def organizar_escritorio(config=[]):
    desktop_path = r"C:\Users\fabia\OneDrive\Escritorio"
    os.chdir(desktop_path)
    while running:
        for carpeta_destino, palabra_clave, ordenar, _ in config:
            if ordenar:
                crear_carpeta(carpeta_destino)
                mover_archivos(palabra_clave, carpeta_destino)
        time.sleep(3)

def iniciar_organizacion(val=False):
    configs = cargar_configuraciones()
    global running, thread
    if val: 
        running = False
    if not running:
        running = True
        thread = threading.Thread(target=organizar_escritorio, args=(configs,))
        thread.start()

def detener_organizacion():
    global running, thread
    running = False
    if thread and thread.is_alive():
        thread.join()

def agregar_configuracion():
    carpeta_destino = entry_carpeta_destino.get()
    palabra_clave = entry_palabra_clave.get()
    guardar_configuracion_bd(carpeta_destino, palabra_clave, ordenando=True)
    iniciar_organizacion(True)
    actualizar_interfaz()
    

#========================================================================

def crear_interfaz(root):
    tk.Label(root, text="Organizador de Escritorio").pack()

    tk.Label(root, text="Palabra clave para mover:").pack()
    global entry_palabra_clave
    entry_palabra_clave = tk.Entry(root)
    entry_palabra_clave.insert(0, "proyecto")
    entry_palabra_clave.pack()

    tk.Label(root, text="Carpeta destino:").pack()
    global entry_carpeta_destino
    entry_carpeta_destino = tk.Entry(root)
    entry_carpeta_destino.insert(0, "NuevaCarpeta")
    entry_carpeta_destino.pack()

    tk.Button(root, text="Agregar", command=agregar_configuracion).pack()
    tk.Button(root, text="Detener todos", command=detener_organizacion).pack()

    global configuracion_frame
    configuracion_frame = tk.Frame(root)
    configuracion_frame.pack()
    actualizar_interfaz()

    iniciar_organizacion()

def actualizar_interfaz():
    for widget in configuracion_frame.winfo_children():
        widget.destroy()

    configs = cargar_configuraciones()
    for carpeta, palabra, ordenando, id in configs:
        texto_config = f"Destino: {carpeta}, Clave: {palabra}, Activo: {'Sí' if ordenando else 'No'}"
        
        frame = tk.Frame(configuracion_frame)
        frame.pack(anchor="w", pady=2)

        label = tk.Label(frame, text=texto_config)
        label.pack(side="left")

        boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda id=id: eliminar_configuracion_bd(id))
        boton_eliminar.pack(side="right")
        
        if ordenando:
            boton_parar = tk.Button(frame, text="parar",background="red",  command=lambda id=id: editar_ordenando_por_id(id , False))
            boton_parar.pack(side="right")
        else:
            boton_empezar = tk.Button(frame,  text="Empezar",background="green",  command=lambda id=id: editar_ordenando_por_id(id , True))
            boton_empezar.pack(side="right")



#====================================================================

iniciar_db()

root = tk.Tk()

root.minsize(600, 500)
root.title("Organizador de archivos")
crear_interfaz(root)

root.mainloop()
