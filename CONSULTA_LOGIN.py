from Connexion_DB import *
import sqlite3
from passlib.context import CryptContext
class Login:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()
        self.contexto = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256")
    def verificacion(self,nombreUsuario,claveUsuario):
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre=?", (nombreUsuario,))
            datos = self.miCursor.fetchall()
            for row in datos:
                Hash = row[3]

                # Verificar la contraseña ingresada con el hash almacenado
            if self.contexto.verify(claveUsuario, Hash):
                return datos
            else:
                return []

        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []