import sqlite3
from Connexion_DB import Base_Datos

class Crud_Productos:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()

    def mostrar_productos(self):
        try:
            self.miCursor.execute("SELECT * FROM Producto")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []

    def Guardar_Producto(self,txtCodeNewProduc,txtNameNewProduct,
                         txtPrecioNewProduct,txtStockNewProduct,
                         txtDescripcionNewProduct):
        try:

            self.miCursor.execute("INSERT INTO Producto (Codigo_Proveedor,nombreProducto,precio,stock,descripcion) "
                                  "VALUES(?,?,?,?,?)",
                                  (txtCodeNewProduc,txtNameNewProduct,
                                   txtPrecioNewProduct,txtStockNewProduct,
                                   txtDescripcionNewProduct))
            self.db.commit()
            print("agregado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))

    def Buscar_Productos(self,busqueda):
        if busqueda:
            # Consultar DB
            self.miCursor.execute("SELECT * FROM Producto WHERE nombreProducto LIKE ?", ('%'+busqueda + '%',))
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        else:
            # Consulta completa si el campo de búsqueda está vacío
            self.miCursor.execute("SELECT * FROM Producto")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
    def Modificar_Producto(self,txtCodeProductoModifyProduct,datosModificarUsuarios):

        try:
            self.miCursor.execute(
                "UPDATE Producto SET Codigo_Proveedor=?,nombreProducto=?,precio=?,stock = ? ,descripcion=? "
                "WHERE idProducto=" + txtCodeProductoModifyProduct,
                datosModificarUsuarios
            )
            self.db.commit()
            self.db.close()
            print("actualizado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))

    def Borrar_Producto(self,id_producto):
        try:
            self.miCursor.execute("DELETE FROM Producto WHERE idProducto=?", (id_producto,))
            self.db.commit()
            self.db.close()
            print("actualizado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))


