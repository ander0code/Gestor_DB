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
            self.miCursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)",(datos))

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
    def Modificar_Usuario(self,txtCodeProductoModifyProduct,datosModificarUsuarios):
        try:
            self.miCursor.execute(
                "UPDATE Usuarios SET Nombre=?,Clave=?,Rol=? WHERE Codigo="+ txtCodeProductoModifyProduct,
                datosModificarUsuarios
            )
            self.db.commit()
            self.db.close()
            print("actualizado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))

    def Verifica_Usuario(self,consulta):
        try:
            self.miCursor.execute("SELECT Clave FROM Usuarios WHERE Codigo=?",(consulta,))
            datos = self.miCursor.fetchone()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []
    def Borrar_Usuario(self,id_usuario):
        try:
            self.miCursor.execute("DELETE FROM Usuarios WHERE Codigo=?", (id_usuario,))
            self.db.commit()
            print("Borrado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))
