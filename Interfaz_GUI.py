from Login import *
from gestor_2 import *
from tkinter import *
from tkinter import messagebox as mb
from Connexion_DB import *

class Software:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("280x150+850+350")
        self.ventana.title("BackPack")
        self.ventana.resizable(False, False)
        self.ventana.iconbitmap("Logo_.ico")
        self.bs = Base_Datos()
        # -------------------------------------
        self.tex_pantalla = Label(text="ID")
        self.tex_pantalla.config(font=("Ariel", 10, "bold"))
        self.tex_pantalla.pack()
        self.tex_input1 = Entry()
        self.tex_input1.pack()
        # -------------------------------------
        self.tex_pantalla = Label(text="Password")
        self.tex_pantalla.config(font=("Ariel", 10, "bold"))
        self.tex_pantalla.pack()
        self.tex_input2 = Entry(show="*")
        self.tex_input2.pack()
            # -------------------------------------
            # -------------------------------------
        id = self.tex_input1.get()
        contra = self.tex_input2.get()
        inicio_seccion.login(id,contra)
        mb.showinfo("acceso permitido","acceso permitido")
        self.ventana.mainloop()

        #-------------------------------------
        def registrar_botton():
            pantalla_new = Toplevel(self.ventana)
            pantalla_new.geometry("300x200+850+350")
            textowrite = Label(pantalla_new, text="El registro solo sera una vez")
            textowrite.config(font=("Ariel", 8, "bold"))
            texto1 = Label(pantalla_new,text="Ingresar ID")
            ID_registro = Entry(pantalla_new)
            texto1.config(font=("Ariel",10,"bold"))
            texto2 = Label(pantalla_new,text="Ingresar Contraseña")
            texto2.config(font=("Ariel", 10, "bold"))
            registBoton = Button(pantalla_new)
            registBoton.config(text="registrarse", font=("Ariel", 10, "bold"),command="")
            CONTRA_registro = Entry(pantalla_new)
            textowrite.pack()
            texto1.pack()
            ID_registro.pack()
            texto2.pack()
            CONTRA_registro.pack()
            registBoton.pack()

        self.loginBoton = Button(self.ventana)
        self.loginBoton.config(text="login", font=("Ariel", 10, "bold"), command="")
        self.loginBoton.place(x=100, y=90, width=80, height=20)
        # -------------------------------------
        self.registBoton = Button(self.ventana)
        self.registBoton.config(text="registrarse", font=("Ariel", 10, "bold"), command=registrar_botton)
        self.registBoton.place(x=98, y=120, width=85, height=25)
        self.bs.cursor.execute("SELECT Id FROM usuarios;")
        resultados = self.bs.cursor.fetchall()
        if len(resultados) > 0:
            self.registBoton.destroy()
            self.ventana.geometry("280x130+850+350")

        self.ventana.mainloop()
        #-------------------------------------
Software()


