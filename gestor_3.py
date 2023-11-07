from tkinter import *
class Crud_Provedor:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("230x150+850+300")
        self.ventana.title("BackPack")
        self.ventana.resizable(False, False)
        # ventana.minsize(600,700)
        self.texto = Label(text="CRUD PROVEDOR")
        self.texto.config(font=("Ariel", 10, "bold"))
        self.texto.pack()


        def agregar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("350x180+850+250")
            pantallaN.grid_columnconfigure(0, weight=1)
            pantallaN.grid_columnconfigure(1, weight=1)

            # ----------------------------------------------------------

            text_datos = Label(pantallaN, text="Ingrese los Datos del Proveedor")
            text_datos.config(font=("Ariel", 10, "bold"))
            text_datos.grid(row=0, column=0, columnspan=2, pady=5)

            # ----------------------------------------------------------

            textnombre = Label(pantallaN, text="IdProveedor: ")
            textnombre.config(font=("Arial", 10, "bold"))
            textnombre.grid(row=1, column=0, ipadx=5, pady=5)
            textadd_nombre = Entry(pantallaN)
            textadd_nombre.grid(row=1, column=1, ipadx=25, pady=5)

            # ----------------------------------------------------------

            textnombre = Label(pantallaN, text="Nombre: ")
            textnombre.config(font=("Arial", 10, "bold"))
            textnombre.grid(row=2, column=0, ipadx=5, pady=5)
            textadd_nombre = Entry(pantallaN)
            textadd_nombre.grid(row=2, column=1, ipadx=25, pady=5)

            # ----------------------------------------------------------

            textcelu = Label(pantallaN, text="Telefono: ")
            textcelu.config(font=("Arial", 10, "bold"))
            textcelu.grid(row=3, column=0, ipadx=5, pady=5)
            textadd_celu = Entry(pantallaN)
            textadd_celu.grid(row=3, column=1, ipadx=25, pady=5)

            # ----------------------------------------------------------

            textemp = Label(pantallaN, text="Empresa: ")
            textemp.config(font=("Arial", 10, "bold"))
            textemp.grid(row=4, column=0, ipadx=5, pady=5)
            textadd_emp = Entry(pantallaN)
            textadd_emp.grid(row=4, column=1, ipadx=25, pady=5)
        def actualizar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("300x400+850+250")
        def eliminar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("300x400+850+250")


        self.agregarBoton = Button()
        self.agregarBoton.config(text="Agregar Provedor", font=("Ariel", 8, "bold"), command=agregar)
        self.agregarBoton.place(x=40, y=30, width=150, height=30)

        self.actuBoton = Button()
        self.actuBoton.config(text="Actualizar Provedor", font=("Ariel", 8, "bold"), command=actualizar)
        self.actuBoton.place(x=40, y=70, width=150, height=30)

        self.elimiBoton = Button()
        self.elimiBoton.config(text="Eliminar Proveedor ", font=("Ariel", 8, "bold"), command=eliminar)
        self.elimiBoton.place(x=40, y=110, width=150, height=30)
        self.ventana.mainloop()
Crud_Provedor()