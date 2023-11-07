from tkinter import *
from tkinter import messagebox as mb
from Connexion_DB import *
# -------------------------------------
bs = Base_Datos()
# -------------------------------------
ventana = Tk()
ventana.geometry("280x150+850+350")
ventana.title("BackPack")
ventana.resizable(False,False)
#-------------------------------------
tex_pantalla = Label(text="ID")
tex_pantalla.config(font=("Ariel",10,"bold"))
tex_pantalla.pack()
tex_input1 = Entry()
tex_input1.pack()
#-------------------------------------
tex_pantalla = Label(text="Password")
tex_pantalla.config(font=("Ariel",10,"bold"))
tex_pantalla.pack()
tex_input2 = Entry(show="*")
tex_input2.pack()
# -------------------------------------
def login():
    id = tex_input1.get()
    contra = tex_input2.get()
    tex_input1.delete(0, "end")
    tex_input2.delete(0, "end")
    bs.cursor.execute("SELECT * FROM usuarios WHERE Id = ? AND contrasenna = ? ",(id,contra))
    if bs.cursor.fetchall():
        mb.showinfo("Acceso Admitido", "Acaba de Ingresar al Gestor.")
    else:
        mb.showerror("ERROR","Datos no encontrados")
#-------------------------------------
def registrar():
    pantalla_new = Toplevel(ventana)
    pantalla_new.geometry("300x400+850+350")
#-------------------------------------
loginBoton = Button()
loginBoton.config(text="login",font=("Ariel",10,"bold"),command=login)
#tex_input2.delete(0,"end")
loginBoton.place(x=100, y=90, width = 80, height = 20 )
#-------------------------------------
registBoton = Button()
registBoton.config(text="registrarse",font=("Ariel",10,"bold"),command=registrar)
registBoton.place(x=98, y=120, width = 85, height = 25 )
#-------------------------------------
ventana.mainloop()


