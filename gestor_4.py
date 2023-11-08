from tkinter import *
class Crud_Productos:
    def __init__(self,ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("230x150+850+300")
        self.ventana.title("BackPack")
        #ventana.minsize(600,700)
        self.texto = Label(self.ventana,text="CRUD PRODUCTOS")
        self.texto.config(font=("Ariel",10,"bold"))
        self.texto.pack()
        self.ventana.resizable(False,False)
        def Opciones_aparte():
            ventana2 = Toplevel(self.ventana)
            ventana2.title("Opciones")
            ventana2.geometry("500x450")
            ventana2.resizable(False,False)
            texto = Label(ventana2,text="PRODUCTOS",font=("Ariel", 15, "bold"))
            texto.place(x=185,y=30)
            mi_frame = Frame(ventana2, bd=1, relief=SOLID)
            mi_frame.place(x=100, y=70, width=300, height=300)
            botton4 = Button(ventana2)
            botton4.config(text="Actualizar Producto", font=("Ariel", 8, "bold"))
            botton4.place(x=40, y=400, width = 150, height = 30)

            botton5 = Button(ventana2)
            botton5.config(text="Eliminar Producto", font=("Ariel", 8, "bold"))
            botton5.place(x=300, y=400, width = 150, height = 30)
        def agregar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("400x250+850+250")
            pantallaN.grid_columnconfigure(0, weight=1)
            pantallaN.grid_columnconfigure(1, weight=1)

            # ----------------------------------------------------------

            text_datos = Label(pantallaN, text="Ingrese los Datos del Producto")
            text_datos.config(font=("Ariel", 10, "bold"))
            text_datos.grid(row=0, column=0, columnspan=2, pady=5)

            # ----------------------------------------------------------

            textnombre = Label(pantallaN, text="Nombre: ")
            textnombre.config(font=("Arial", 10, "bold"))
            textnombre.grid(row=1, column=0, ipadx=5, pady=5)
            textadd_nombre = Entry(pantallaN)
            textadd_nombre.grid(row=1, column=1, ipadx=25, pady=5)

            # ----------------------------------------------------------

            textprecio = Label(pantallaN, text="Precio: ")
            textprecio.config(font=("Arial", 10, "bold"))
            textprecio.grid(row=2, column=0, ipadx=5, pady=5)
            textadd_precio = Entry(pantallaN)
            textadd_precio.grid(row=2, column=1, ipadx=25, pady=5)

            # ----------------------------------------------------------

            textstock = Label(pantallaN, text="Stock: ")
            textstock.config(font=("Arial", 10, "bold"))
            textstock.grid(row=3, column=0, ipadx=5, pady=5)
            textadd_stock = Entry(pantallaN)
            textadd_stock.grid(row=3, column=1, ipadx=25, pady=5)

            # ----------------------------------------------------------

            textdesc = Label(pantallaN, text="Descripción: ")
            textdesc.config(font=("Arial", 10, "bold"))
            textdesc.grid(row=4, column=0, ipadx=5, pady=5)
            textadd_desc = Text(pantallaN, height=4, width=30)
            textadd_desc.grid(row=4, column=1, pady=5)

        def obtener():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("300x400+850+250")

        def actualizar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("300x400+850+250")

        def eliminar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("300x400+850+250")


        self.agregarBoton = Button(self.ventana)
        self.agregarBoton.config(text="Agregar Producto",font=("Ariel",8,"bold"), command=agregar)
        self.agregarBoton.place(x=40, y=30, width=150, height=30)

        self.mostrarBoton = Button(self.ventana)
        self.mostrarBoton.config(text="Mostrar Productos", font=("Ariel", 8, "bold"), command=Opciones_aparte)
        self.mostrarBoton.place(x=40, y=70, width=150, height =30)

        self.obtenerBoton = Button(self.ventana)
        self.obtenerBoton.config(text="Obtener Producto ", font=("Ariel", 8, "bold"), command=obtener)
        self.obtenerBoton.place(x=40, y=110, width=150, height=30)
        self.ventana.mainloop()