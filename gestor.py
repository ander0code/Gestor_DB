from gestor_2 import *
from tkinter import *
from tkinter import messagebox as mb
from Connexion_DB import *

class Software:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("280x150+850+350")
        self.ventana.title("BackPack")
        self.ventana.resizable(False,False)
        self.ventana.iconbitmap("Logo_.ico")
        self.bs = Base_Datos()
        #-------------------------------------
        self.tex_pantalla = Label(text="ID")
        self.tex_pantalla.config(font=("Ariel",10,"bold"))
        self.tex_pantalla.pack()
        self.tex_input1 = Entry()
        self.tex_input1.pack()
        #-------------------------------------
        self.tex_pantalla = Label(text="Password")
        self.tex_pantalla.config(font=("Ariel",10,"bold"))
        self.tex_pantalla.pack()
        self.tex_input2 = Entry(show="*")
        self.tex_input2.pack()
        # -------------------------------------
        def login():
            id = self.tex_input1.get()
            contra = self.tex_input2.get()
            self.tex_input1.delete(0, "end")
            self.tex_input2.delete(0, "end")
            self.bs.cursor.execute("SELECT * FROM usuarios WHERE Id = ? AND contrasenna = ? ",(id,contra))
            if self.bs.cursor.fetchall():
                self.ventana.withdraw()
                mb.showinfo("Acceso Admitido", "Acaba de Ingresar al Gestor.")
                Crud_General(self.ventana)
            else:
                mb.showerror("ERROR","Datos no encontrados")
        #-------------------------------------
        def registrar_botton():
            global ID_registro, CONTRA_registro, pantalla_new
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
            registBoton.config(text="registrarse", font=("Ariel", 10, "bold"),command=agregar_registro)
            CONTRA_registro = Entry(pantalla_new)
            textowrite.pack()
            texto1.pack()
            ID_registro.pack()
            texto2.pack()
            CONTRA_registro.pack()
            registBoton.pack()
        #-------------------------------------
        def agregar_registro():
            id = ID_registro.get()
            contra =CONTRA_registro.get()
            self.bs.cursor.execute(
                "INSERT INTO usuarios (Id, contrasenna) VALUES (?, ?)",
                (id,contra))
            self.bs.conexion.commit()
            mb.showinfo("Éxito", "usuario agregado con éxito.")
            registBoton.destroy()
            pantalla_new.withdraw()
        #-------------------------------------

        #-------------------------------------
        loginBoton = Button()
        loginBoton.config(text="login",font=("Ariel",10,"bold"),command=login)
        #tex_input2.delete(0,"end")
        loginBoton.place(x=100, y=90, width = 80, height = 20 )
        #-------------------------------------
        registBoton = Button()
        registBoton.config(text="registrarse",font=("Ariel",10,"bold"),command=registrar_botton)
        registBoton.place(x=98, y=120, width = 85, height = 25 )
        self.bs.cursor.execute("SELECT Id FROM usuarios;")
        #-------------------------------------
        resultados = self.bs.cursor.fetchall()
        if len(resultados) >0:
            registBoton.destroy()
            self.ventana.geometry("280x130+850+350")
        #-------------------------------------
        self.ventana.mainloop()
Software()


