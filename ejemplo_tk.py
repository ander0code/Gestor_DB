from tkinter import *
import os
import sqlite3
ventana = Tk()
ventana.geometry("300x500+850+350")
ventana.title("BackPack")
ventana.minsize(200, 100)
#---------------------------------------------------
nombre_base_datos = "DB_Gestor_proyecyo.db"
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_base_datos = os.path.join(directorio_actual, nombre_base_datos)

conexion = sqlite3.connect(ruta_base_datos)
cursor = conexion.cursor()
cursor.execute("SELECT nombre FROM Proveedores;")
resultados = cursor.fetchall()
print(len(resultados))
#-----------------------------
def botones_seleccionables():
    panel_control = IntVar()
    panel_control.set(-1)
    # Itera sobre los resultados de la consulta y crea botones de radio para cada fila
    for i, fila in enumerate(resultados):
        x = 100  # La posición horizontal se mantiene constante
        y = 10 + i * 30
        nombre = fila[0]  # Suponiendo que el nombre está en la primera posición de cada fila
        button = Radiobutton(ventana, variable=panel_control, value=i, text=nombre)
        button.place(x = x, y = y,width =100,height=50 )
    #-------------------------------
    ventana.mainloop()
botones_seleccionables()

def Resolucion_pantalla(event):
    print(f"{event.width}x{event.height}" )
ventana.bind("<Configure>",Resolucion_pantalla)
