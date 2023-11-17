import sqlite3
from Connexion_DB import Base_Datos

class Crud_Proveedor:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()

    def mostrar_proveedores(self):
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Rol = 'Proveedor'")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []

    def Obetener_proveedores(self):
        try:
            self.miCursor.execute("SELECT Codigo,Nombre FROM Usuarios WHERE Rol = 'Proveedor'")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []

    def mostrar_productos_proveedor(self, codigo_proveedor):
        try:
            self.miCursor.execute("SELECT Usuarios.Nombre, Producto.* FROM Producto "
                             "JOIN Usuarios ON Producto.Codigo_Proveedor = Usuarios.Codigo "
                             "WHERE Usuarios.Codigo = ?", (codigo_proveedor,))
            productos = self.miCursor.fetchall()
            self.db.close()
            return productos
        except sqlite3.Error as e:
            print(f"Error en mostrar lista de Productos: {e}")
            return []

    def buscar_proveedores(self, nombre_proveedor):
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre LIKE ? AND Rol = 'Proveedor'",
                             (nombre_proveedor + '%',))

            proveedores = self.miCursor.fetchall()
            self.db.close()

            return proveedores
        except sqlite3.Error as e:
            print(f"Error en la consulta: {e}")
            return []