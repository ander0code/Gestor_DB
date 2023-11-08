from gestor_2 import *
from tkinter import *
from tkinter import messagebox as mb
from Connexion_DB import *
# -------------------------------------
bs = Base_Datos()
# -------------------------------------
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
        ventana.withdraw()
        Crud_General(ventana)
    else:
        mb.showerror("ERROR","Datos no encontrados")
#-------------------------------------
def registrar_botton():
    global ID_registro, CONTRA_registro, pantalla_new
    pantalla_new = Toplevel(ventana)
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
    bs.cursor.execute(
        "INSERT INTO usuarios (Id, contrasenna) VALUES (?, ?)",
        (id,contra))
    bs.conexion.commit()
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
bs.cursor.execute("SELECT Id FROM usuarios;")
resultados = bs.cursor.fetchall()
if len(resultados) >0:
    registBoton.destroy()
    ventana.geometry("280x130+850+350")
#-------------------------------------
ventana.mainloop()


