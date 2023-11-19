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
                 datos=("SELECT Usuarios.Nombre AS Nombre_Provedor,"
                        "Producto.Codigo_Proveedor,Producto.idProducto,"
                        "Producto.nombreProducto,Producto.precio,"
                        "Producto.stock,"
                        "Producto.descripcion "
                        "FROM Producto "
                        "JOIN Usuarios ON Producto.Codigo_Proveedor = Usuarios.Codigo ")
                 return datos

        except sqlite3.Error as e:
            print(f"Error en mostrar consulta: {e}")
            return []