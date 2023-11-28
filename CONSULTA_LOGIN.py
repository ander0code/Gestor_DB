from Connexion_DB import *
import sqlite3
import bcrypt
class Login:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()
    def verificacion(self,nombreUsuario,claveUsuario):
        global Hash
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre=?", (nombreUsuario,))
            datos = self.miCursor.fetchall()
            for row in datos:
                Hash = row[3]

                # Verificar la contraseña ingresada con el hash almacenado
            if self.verificar_contrasena(claveUsuario, Hash):
                return datos
            else:
                return []

        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []
    def verificar_contrasena(self,contrasena, hashed):
        contrasena_encoded = contrasena.encode('utf-8')
        return bcrypt.checkpw(contrasena_encoded, hashed)