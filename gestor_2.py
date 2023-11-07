from tkinter import *
class Crud_General:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("300x100+850+350")
        self.ventana.title("BackPack")
        self.ventana.minsize(200,100)

        self.botton = Button()
        self.botton.config(text="Productos",font=("Ariel",10,"bold"))
        self.botton.place(x=100, y=10, width = 100, height = 30 )

        self.botton2 = Button()
        self.botton2.config(text="Proveedores",font=("Ariel",10,"bold"))
        self.botton2.place(x=100, y=50, width = 100, height = 30 )

        self.ventana.mainloop()
