from Connexion_DB import *
from tkinter import messagebox as mb

class Crud_Proveedor:

    def __init__(self, base_datos):
        self.bs = base_datos

    def ingresarProveedor(self, id, nombre, telefono, empresa):
        try:
            self.bs.cursor.execute(
                "INSERT INTO Proveedores (idProveedor, nombre, numero_telefono, empresa) VALUES (?, ?, ?, ?)",
                (id, nombre, telefono, empresa))
            self.bs.conexion.commit()
            mb.showinfo("Éxito", "Proveedor agregado con éxito.")
        except sqlite3.Error as e:
            mb.showerror("Error", "Error al agregar el proveedor: " + str(e))

    def mostrar_proveedores(self):
        try:
            self.bs.cursor.execute("SELECT * FROM Proveedores")
            resultados = self.bs.cursor.fetchall()

            return resultados

        except sqlite3.Error as e:
            mb.showerror("Error", "Error al obtener la lista de proveedores: " + str(e))
            return []
