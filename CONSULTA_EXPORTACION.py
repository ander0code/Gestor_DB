from Connexion_DB import *
import sqlite3
class Consulta_Exportacion:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()

    def Obtener_Datos_Exportar(self,dato):
        try:
            if dato == "Historial":
                datos=("SELECT * FROM Historial")

                return datos
            elif dato == "Producto":
                 datos=("SELECT Usuarios.Nombre AS Proveedor, "
                        "Producto.Codigo_Proveedor AS IdProveedor, "
                        "Producto.nombreProducto, "
                        "Producto.idProducto, "
                        "Producto.precio, "
                        "Producto.stock, "
                        "Producto.descripcion AS Categoria "
                        "FROM Producto "
                        "JOIN Usuarios ON Producto.Codigo_Proveedor = Usuarios.Codigo"
                        )
                 return datos

        except sqlite3.Error as e:
            print(f"Error en mostrar consulta: {e}")
            return []