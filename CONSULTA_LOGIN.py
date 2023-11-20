from Connexion_DB import *
import sqlite3
class Login:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()
    def verificacion(self,nombreUsuario,claveUsuario):
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre=? AND Clave=?",
                                  (nombreUsuario, claveUsuario))
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos

        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []