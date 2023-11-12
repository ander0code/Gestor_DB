from Connexion_DB import *
class inicio_seccion:
    @staticmethod
    def login(tex_input1,tex_input2):
        bs = Base_Datos()
        try:
            id = tex_input1.get()
            contra = tex_input2.get()
            bs.cursor.execute("SELECT * FROM usuarios WHERE Id = ? AND contrasenna = ? ", (id, contra))
            return bs.cursor.fetchall()
        except sqlite3.Error as e:
            print("error al iniciar secion {}".format(e))

    @staticmethod
    def agregar_registro(ID_registro,CONTRA_registro):
        try:
            bs = Base_Datos()
            id = ID_registro.get()
            contra =CONTRA_registro.get()
            bs.cursor.execute(
                "INSERT INTO usuarios (Id, contrasenna) VALUES (?, ?)",
                (id,contra))
            bs.conexion.commit()
            return True
        except sqlite3.Error as e:
            print("error al iniciar secion {}".format(e))

