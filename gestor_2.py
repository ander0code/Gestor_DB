from gestor_4 import *
from gestor_3 import *
from tkinter import *
class Crud_General:
    def __init__(self,ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("300x200+850+350")
        self.ventana.title("BackPack")
        self.ventana.iconbitmap("Logo_.ico")
        self.ventana.resizable(False,False)
        def Provedores():
            self.ventana.withdraw()
            Crud_Provedores(self.ventana)
        def Productos():
            self.ventana.withdraw()
            Crud_Productos(self.ventana)

        self.texto = Label(self.ventana)
        self.texto.config(text = "Panel de Control",font=("Ariel",18,"bold"))
        self.texto.place(x=50,y=10)
        self.botton = Button(self.ventana)
        self.botton.config(text="Productos",font=("Ariel",14,"bold"),command=Productos)
        self.botton.place(x=75, y=50, width=150, height=50)

        self.botton2 = Button(self.ventana)
        self.botton2.config(text="Proveedores",font=("Ariel",14,"bold"),command=Provedores)
        self.botton2.place(x=75, y=110, width=150, height=50)

        self.ventana.mainloop()

