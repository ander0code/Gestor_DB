from Connexion_DB import *
import sqlite3
import bcrypt

class Crud_Usuarios:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()


    def Mostrar_Usuarios(self):
        try:
            self.miCursor.execute("SELECT Codigo,Nombre,Rol FROM Usuarios")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []

    def Ultimo_Usuario(self):
        try:
            self.miCursor.execute("SELECT MAX(Codigo) FROM Usuarios")
            datos = self.miCursor.fetchall()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []


    def Guardar_Usuario(self,datos):
        try:
            self.miCursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)", datos)
            self.db.commit()
            print("agregado exitosamente")
            return True


        except sqlite3.Error as e:
            print(f"Error en modificar proveedor: {e}")

    def Buscar_Usuario(self,busqueda):
        if busqueda:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre LIKE ?",('%' +busqueda + '%',))
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        else:
            self.miCursor.execute("SELECT * FROM Usuarios")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos

    def Modificar_Usuario(self, codigo_usuario, datosModificarUsuarios):
        try:
            self.miCursor.execute(
                "UPDATE Usuarios SET Nombre=?, Hash=?, Rol=? WHERE Codigo=?",
                (datosModificarUsuarios[0], datosModificarUsuarios[1], datosModificarUsuarios[2], codigo_usuario)
            )
            self.db.commit()
            print("Actualizado exitosamente")
            return True
        except sqlite3.Error as e:
            print("Problemas: {}".format(e))
            return False

    def Verifica_Usuario(self, codigo_usuario, contrasena_confirmacion):
        try:
            self.miCursor.execute("SELECT Hash FROM Usuarios WHERE Codigo=?", (codigo_usuario,))
            hash_encriptado = self.miCursor.fetchone()

            if hash_encriptado and self.verificar_contrasena(contrasena_confirmacion, hash_encriptado[0]):
                return True
            else:
                return False

        except sqlite3.Error as e:
            print(f"Error en verificar usuario: {e}")
            return False
    def verificar_contrasena(self,contrasena, hashed):
        contrasena_encoded = contrasena.encode('utf-8')
        return bcrypt.checkpw(contrasena_encoded, hashed)

    def Borrar_Usuario(self, id_usuario):
        try:
            self.miCursor.execute("DELETE FROM Usuarios WHERE Codigo=?", (id_usuario,))
            self.db.commit()
            print("Borrado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))
            return False
        finally:
            self.db.close()

