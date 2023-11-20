import os
import sqlite3
class Base_Datos:
    def __init__(self):
        self.Base_de_datos = "whatislove.db"
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta = os.path.join(self.directorio_actual, self.Base_de_datos)
        if os.path.exists(self.ruta):
            self.conexion = sqlite3.connect(self.ruta)
            self.cursor = self.conexion.cursor()
            print("Conectado a la base de datos.")
        else:
            print("La base de datos no se encontró")

