from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb
from Connexion_DB import *
from Proveedores_Crud import *

class Gui_Provedores:
    def __init__(self, ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("230x120+850+300")
        self.ventana.title("BackPack")
        self.ventana.resizable(False, False)
        self.bs = Base_Datos()
        self.proveedor = Crud_Proveedor(self.bs)
        self.crear_interfaz()

    def mostrar(self):
        resultados = self.proveedor.mostrar_proveedores()

        ventana2 = Toplevel(self.ventana)
        ventana2.title("Lista de Proveedores")
        ventana2.geometry("1100x450+500+200")

        texto = Label(ventana2, text="PROVEEDORES", font=("Arial", 15, "bold"))
        texto.place(x=500, y=30)

        mi_frame = Frame(ventana2, bd=1, relief=SOLID)
        mi_frame.place(x=100, y=70, width=900, height=300)

        tab = ttk.Treeview(mi_frame, columns=("Id", "Nombre", "Telefono", "Empresa"), show='headings', height=5)

        tab.column("Id", anchor=CENTER)
        tab.heading("Id", text="Id")
        tab.column("Nombre", anchor=CENTER)
        tab.heading("Nombre", text="Nombre")
        tab.column("Telefono", anchor=CENTER)
        tab.heading("Telefono", text="Telefono")
        tab.column("Empresa", anchor=CENTER)
        tab.heading("Empresa", text="Empresa")

        for resultado in resultados:
            tab.insert("", END, values=resultado)

        scroll_y = ttk.Scrollbar(mi_frame, orient=VERTICAL, command=tab.yview)
        tab.configure(yscroll=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        tab.pack(fill=BOTH, expand=YES)

        boton4 = Button(ventana2, text="Actualizar Producto", font=("Arial", 8, "bold"))
        boton4.place(x=400, y=400, width=150, height=30)

        boton5 = Button(ventana2, text="Eliminar Producto", font=("Arial", 8, "bold"))
        boton5.place(x=600, y=400, width=150, height=30)

    def agregar_proveedor(self):
        id = self.textadd_id.get()
        nombre = self.textadd_nombre.get()
        telefono = self.textadd_telefono.get()
        empresa = self.textadd_empresa.get()
        self.proveedor.ingresarProveedor(id, nombre, telefono, empresa)

    def actualizar(self):
        pantallaN = Toplevel(self.ventana)
        pantallaN.geometry("300x400+850+250")

    def eliminar(self):
        pantallaN = Toplevel(self.ventana)
        pantallaN.geometry("300x400+850+250")
    def crear_interfaz(self):
        texto = Label(self.ventana,text="CRUD PROVEEDOR")
        texto.config(font=("Ariel", 10, "bold"))
        texto.pack()

        # ----------------------------------------------------------

        agregarBoton = Button(self.ventana,text="Agregar Proveedor", font=("Ariel", 8, "bold"), command=self.agregar)
        agregarBoton.place(x=40, y=30, width=150, height=30)

        # ----------------------------------------------------------

        mostrarBoton = Button(self.ventana,text="Mostrar Productos", font=("Ariel", 8, "bold"), command=self.mostrar)
        mostrarBoton.place(x=40, y=70, width=150, height=30)

        # ----------------------------------------------------------

    def agregar(self):
        pantallaN = Toplevel(self.ventana)
        pantallaN.geometry("350x215+850+250")
        pantallaN.grid_columnconfigure(0, weight=1)
        pantallaN.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------------

        text_datos = Label(pantallaN, text="Ingrese los Datos del Proveedor")
        text_datos.config(font=("Ariel", 10, "bold"))
        text_datos.grid(row=0, column=0, columnspan=2, pady=5)

        # ----------------------------------------------------------

        text_id = Label(pantallaN, text="IdProveedor: ")
        text_id.config(font=("Arial", 10, "bold"))
        text_id.grid(row=1, column=0, ipadx=5, pady=5)
        self.textadd_id = Entry(pantallaN)
        self.textadd_id.grid(row=1, column=1, ipadx=25, pady=5)

        # ----------------------------------------------------------

        text_nombre = Label(pantallaN, text="Nombre: ")
        text_nombre.config(font=("Arial", 10, "bold"))
        text_nombre.grid(row=2, column=0, ipadx=5, pady=5)
        self.textadd_nombre = Entry(pantallaN)
        self.textadd_nombre.grid(row=2, column=1, ipadx=25, pady=5)

        # ----------------------------------------------------------

        text_telefono = Label(pantallaN, text="Telefono: ")
        text_telefono.config(font=("Arial", 10, "bold"))
        text_telefono.grid(row=3, column=0, ipadx=5, pady=5)
        self.textadd_telefono = Entry(pantallaN)
        self.textadd_telefono.grid(row=3, column=1, ipadx=25, pady=5)

        # ----------------------------------------------------------

        text_empresa = Label(pantallaN, text="Empresa: ")
        text_empresa.config(font=("Arial", 10, "bold"))
        text_empresa.grid(row=4, column=0, ipadx=5, pady=5)
        self.textadd_empresa = Entry(pantallaN)
        self.textadd_empresa.grid(row=4, column=1, ipadx=25, pady=5)

        # ----------------------------------------------------------

        agregar_btn = Button(pantallaN, text="Agregar", font=("Arial", 10, "bold"), command=self.agregar_proveedor)
        agregar_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.ventana.mainloop()
