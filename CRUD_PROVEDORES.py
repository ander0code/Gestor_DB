from Connexion_DB import *

class CRUD_Provedores:
    @staticmethod
    def agregar_proveedor(textadd_id,textadd_nombre,textadd_telefono,textadd_empresa):
        id = textadd_id.get()
        nombre = textadd_nombre.get()
        telefono = textadd_telefono.get()
        empresa = textadd_empresa.get()
        bs = Base_Datos()

        try:
            bs.cursor.execute(
                "INSERT INTO Proveedores (idProveedor, nombre, numero_telefono, empresa) VALUES (?, ?, ?, ?)",
                (id, nombre, telefono, empresa))
            bs.conexion.commit()
            print("agregado exitosamente")
            return True
        except sqlite3.Error as e:
            print("problemas {} ".format(e))


    @staticmethod
    def mostrar_proveedores():
        bs = Base_Datos()
        try:
            bs.cursor.execute("SELECT * FROM Proveedores")
            resultados = bs.cursor.fetchall()

            return resultados

        except sqlite3.Error as e:
            mb.showerror("Error", "Error al obtener la lista de proveedores: " + str(e))
            return []