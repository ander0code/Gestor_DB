from gestor_3 import *
from tkinter import *
class Crud_General:
    def __init__(self,ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("300x100+850+350")
        self.ventana.title("BackPack")
        self.ventana.minsize(200,100)
        def alaraco():
            Crud_Provedores(self.ventana)

        self.botton = Button(self.ventana)
        self.botton.config(text="Productos",font=("Ariel",10,"bold"))
        self.botton.place(x=100, y=10, width = 100, height = 30 )

        self.botton2 = Button(self.ventana)
        self.botton2.config(text="Proveedores",font=("Ariel",10,"bold"),command=alaraco)
        self.botton2.place(x=100, y=50, width = 100, height = 30 )

        self.ventana.mainloop()

