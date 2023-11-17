from Connexion_DB import *
import sqlite3
class Consulta_Historial:
    def __init__(self):
        self.db = Base_Datos().conexion
        self.miCursor = self.db.cursor()


    def Cargar_Historial(self):
        try:
            self.miCursor.execute("SELECT * FROM Historial")
            datos = self.miCursor.fetchall()
            self.db.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error en mostrar proveedor: {e}")
            return []


    def Registro_Historial(self,fecha_hora_actual,accion,usuario):
        try:
            self.miCursor.execute("INSERT INTO Historial (fecha_hora, accion, usuario) VALUES (?, ?, ?)",
                             (fecha_hora_actual, accion, usuario))
            self.db.commit()
            print("Registro ejecutado exitosamente")
            return True

        except sqlite3.Error as e:
            print("problemas {} ".format(e))

    def borrar_tabla(self):
        try:
            self.miCursor.execute("DELETE FROM Historial")
            self.db.commit()
            self.db.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al borrar la tabla Historial: {e}")
            return []
