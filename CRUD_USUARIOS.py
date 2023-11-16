from Connexion_DB import *
import sqlite3
class Crud_Usuarios:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()

    def Mostrar_Usuarios(self):
        try:
            self.miCursor.execute("SELECT * FROM Usuarios")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []