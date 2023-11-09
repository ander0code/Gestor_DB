from tkinter import *
from tkinter import messagebox as mb
from Connexion_DB import *
class Crud_Provedores:
    def __init__(self,ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("300x200+850+350")
        self.ventana.title("BackPack")
        self.ventana.iconbitmap("Logo_.ico")
        self.ventana.resizable(False, False)
        self.bs = Base_Datos()
        self.crear_interfaz()
        self.imagen = PhotoImage(file="logo_return2.1.gif")

        def retornar_ventana():
            self.ventana.withdraw()
            ventana.deiconify()

        self.botton_return2 = Button(self.ventana, image=self.imagen, command=retornar_ventana)
        self.botton_return2.place(x=130, y=170)

    def mostrar(self):
        self.ventana.withdraw()
        ventana2 = Toplevel(self.ventana)
        ventana2.iconbitmap("Logo_.ico")
        ventana2.title("Opciones")
        ventana2.geometry("500x450+800+300")
        ventana2.resizable(False, False)
        texto = Label(ventana2, text="PROVEEDORES", font=("Ariel", 15, "bold"))
        texto.place(x=180, y=30)
        mi_frame = Frame(ventana2, bd=1, relief=SOLID)
        mi_frame.place(x=100, y=70, width=300, height=300)
        #-------------------------------------------------
        bs = Base_Datos()
        bs.cursor.execute("SELECT nombre FROM Proveedores;")
        resultados = bs.cursor.fetchall()
        print(len(resultados))
        #-------------------------------------------

        panel_control = IntVar()
        panel_control.set(-1)
            # Itera sobre los resultados de la consulta y crea botones de radio para cada fila
        for i, fila in enumerate(resultados):
            x = 200  # La posición horizontal se mantiene constante
            y = 80 + i * 50
            nombre = fila[0]  # Suponiendo que el nombre está en la primera posición de cada fila
            button = Radiobutton(ventana2, variable=panel_control, value=i, text=nombre)
            button.place(x=x, y=y, width=100, height=50)

        #-------------------------------------------------
        botton4 = Button(ventana2)
        botton4.config(text="Actualizar Producto", font=("Ariel", 8, "bold"))
        botton4.place(x=40, y=400, width=150, height=30)

        botton5 = Button(ventana2)
        botton5.config(text="Eliminar Producto", font=("Ariel", 8, "bold"))
        botton5.place(x=300, y=400, width=150, height=30)
        def retornar_ventana():
            ventana2.withdraw()
            self.ventana.deiconify()

        botton_return = Button(ventana2, image=self.imagen, command=retornar_ventana)
        botton_return.place(x=235, y=400)

    def agregar_proveedor(self):
        id = self.textadd_id.get()
        nombre = self.textadd_nombre.get()
        telefono = self.textadd_telefono.get()
        empresa = self.textadd_empresa.get()

        try:
            self.bs.cursor.execute(
                "INSERT INTO Proveedores (idProveedor, nombre, numero_telefono, empresa) VALUES (?, ?, ?, ?)",
                (id, nombre, telefono, empresa))
            self.bs.conexion.commit()
            mb.showinfo("Éxito", "Proveedor agregado con éxito.")
        except sqlite3.Error as e:
            mb.showerror("Error", "Error al agregar el proveedor: " + str(e))

    def actualizar(self):
        pantallaN = Toplevel(self.ventana)
        pantallaN.geometry("300x400+850+250")

    def eliminar(self):
        pantallaN = Toplevel(self.ventana)
        pantallaN.geometry("300x400+850+250")
    def crear_interfaz(self):
        texto = Label(self.ventana,text="CRUD PROVEEDOR")
        texto.config(font=("Ariel", 18, "bold"))
        texto.place(x=35,y=10)
        # ----------------------------------------------------------

        agregarBoton = Button(self.ventana,text="Agregar Proveedor", font=("Ariel", 14, "bold"), command=self.agregar)
        agregarBoton.place(x=50, y=50, width=200, height=50)

        # ----------------------------------------------------------

        mostrarBoton = Button(self.ventana,text="Mostrar Proveedores", font=("Ariel", 14, "bold"), command=self.mostrar)
        mostrarBoton.place(x=40, y=110, width=220, height=50)

        # ----------------------------------------------------------

    def agregar(self):
        self.ventana.withdraw()
        pantallaN = Toplevel(self.ventana)
        pantallaN.iconbitmap("Logo_.ico")
        pantallaN.geometry("350x215+800+350")
        pantallaN.grid_columnconfigure(0, weight=1)
        pantallaN.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------------
        def retornar_ventana():
            pantallaN.withdraw()
            self.ventana.deiconify()
        botton_return = Button(pantallaN,image=self.imagen,command=retornar_ventana)
        botton_return.place(x=30,y=172)

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

        # ----------------------------------------------------------

        self.ventana.mainloop()
