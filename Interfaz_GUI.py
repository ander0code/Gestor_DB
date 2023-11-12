from Login import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from CRUD_PROVEDORES import *
from Connexion_DB import *


class Interfaz_1:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("280x150+850+350")
        self.ventana.title("BackPack")
        self.ventana.resizable(False, False)
        self.ventana.iconbitmap("Logo_.ico")
        self.bs = Base_Datos()
        # -------------------------------------
        self.tex_pantalla = Label(text="ID")
        self.tex_pantalla.config(font=("Ariel", 10, "bold"))
        self.tex_pantalla.pack()
        self.tex_input1 = Entry()
        self.tex_input1.pack()
        # -------------------------------------
        self.tex_pantalla = Label(text="Password")
        self.tex_pantalla.config(font=("Ariel", 10, "bold"))
        self.tex_pantalla.pack()
        self.tex_input2 = Entry(show="*")
        self.tex_input2.pack()
            # -------------------------------------

        def sign_up():
            self.ventana.withdraw()
            global ID_registro, CONTRA_registro,pantalla_new
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
            registBoton.config(text="registrarse", font=("Ariel", 10, "bold"),command=sign_up_add)
            CONTRA_registro = Entry(pantalla_new)
            textowrite.pack()
            texto1.pack()
            ID_registro.pack()
            texto2.pack()
            CONTRA_registro.pack()
            registBoton.pack()
        def sign_up_add():
            if inicio_seccion.agregar_registro(ID_registro, CONTRA_registro):
                mb.showinfo("CONSULTA EXITOSA", "AGREGADO A LA BASE DE DATOS")
                self.registBoton.destroy()
                pantalla_new.withdraw()
                self.ventana.deiconify()
            else:
                mb.showerror("Error", "No se pudo agregar a la base de datos")
        def login():
            if inicio_seccion.login(self.tex_input1, self.tex_input2):
                self.tex_input1.delete(0, "end")
                self.tex_input2.delete(0, "end")
                self.ventana.withdraw()
                mb.showinfo("acceso permitido", "acceso permitido")
                Interfaz_2(self.ventana)

            else:
                mb.showerror("Error", "No pudo ingresar al gestor")
        #-------------------------------------
        self.loginBoton = Button(self.ventana)
        self.loginBoton.config(text="login", font=("Ariel", 10, "bold"), command=login)
        self.loginBoton.place(x=100, y=90, width=80, height=20)
        # -------------------------------------
        self.registBoton = Button(self.ventana)
        self.registBoton.config(text="registrarse", font=("Ariel", 10, "bold"), command=sign_up)
        self.registBoton.place(x=98, y=120, width=85, height=25)

        self.bs.cursor.execute("SELECT Id FROM usuarios;")
        resultados = self.bs.cursor.fetchall()
        if len(resultados) > 0:
            self.registBoton.destroy()
            self.ventana.geometry("280x130+850+350")

        self.ventana.mainloop()
        #-------------------------------------

class Interfaz_2:
    def __init__(self,ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("300x200+850+350")
        self.ventana.title("BackPack")
        self.ventana.iconbitmap("Logo_.ico")
        self.ventana.resizable(False,False)
        def Provedores():
            self.ventana.withdraw()
            Interfaz_Provedores(self.ventana)
        def Productos():
            self.ventana.withdraw()
            Interfaz_Productos(self.ventana)

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
class Interfaz_Provedores:
    global textadd_id, textadd_nombre,textadd_telefono,textadd_empresa
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

    def mostrar_provedor(self):
        resultados = CRUD_Provedores.mostrar_proveedores()
        self.ventana.withdraw()
        ventana2 = Toplevel(self.ventana)
        ventana2.iconbitmap("Logo_.ico")
        ventana2.title("Opciones")
        ventana2.geometry("1100x450+500+200")
        ventana2.resizable(False, False)
        texto = Label(ventana2, text="PROVEEDORES", font=("Arial", 15, "bold"))
        texto.place(x=500, y=30)

        mi_frame = Frame(ventana2, bd=1, relief=SOLID)
        mi_frame.place(x=100, y=70, width=900, height=300)
        #-------------------------------------------------
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

        #-------------------------------------------------

        boton4 = Button(ventana2, text="Actualizar Producto", font=("Arial", 8, "bold"))
        boton4.place(x=400, y=400, width=150, height=30)

        boton5 = Button(ventana2, text="Eliminar Producto", font=("Arial", 8, "bold"))
        boton5.place(x=600, y=400, width=150, height=30)

        def retornar_ventana():
            ventana2.withdraw()
            self.ventana.deiconify()

        botton_return = Button(ventana2, image=self.imagen, command=retornar_ventana)
        botton_return.place(x=235, y=400)

    def agregar_proveedor(self):
        if CRUD_Provedores.agregar_proveedor(self.textadd_id,self.textadd_nombre,
                                             self.textadd_telefono,self.textadd_empresa):
            mb.showinfo("Éxito", "Proveedor agregado con éxito.")
        else:
            mb.showerror("Error", "Error al agregar el proveedor")



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

        mostrarBoton = Button(self.ventana,text="Mostrar Proveedores", font=("Ariel", 14, "bold"),
                              command=self.mostrar_provedor)
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
class Interfaz_Productos:
    def __init__(self,ventana):
        self.ventana = Toplevel(ventana)
        self.ventana.geometry("300x270+850+350")
        self.ventana.title("BackPack")
        self.ventana.iconbitmap("Logo_.ico")
        self.imagen = PhotoImage(file="logo_return2.1.gif")
        #ventana.minsize(600,700)
        self.texto = Label(self.ventana,text="CRUD PRODUCTOS")
        self.texto.config(font=("Ariel",18,"bold"))
        self.texto.place(x=35,y=10)
        self.ventana.resizable(False,False)

        def Opciones_aparte():
            self.ventana.withdraw()
            ventana2 = Toplevel(self.ventana)
            ventana2.title("Opciones")
            ventana2.geometry("500x450+800+200")
            ventana2.iconbitmap("Logo_.ico")
            ventana2.resizable(False,False)

            def retornar_ventana():
                ventana2.withdraw()
                self.ventana.deiconify()

            botton_return = Button(ventana2, image=self.imagen, command=retornar_ventana)
            botton_return.place(x=235, y=400)

            #----------------------------------
            texto = Label(ventana2, text="Productos", font=("Ariel", 15, "bold"))
            texto.place(x=200, y=30)
            mi_frame = Frame(ventana2, bd=1, relief=SOLID)
            mi_frame.place(x=100, y=70, width=300, height=300)
            # -------------------------------------------------
            bs = Base_Datos()
            bs.cursor.execute("SELECT nombreProducto FROM Productos;")
            resultados = bs.cursor.fetchall()
            print(len(resultados))
            # -------------------------------------------
            panel_control = IntVar()
            panel_control.set(-1)
            # Itera sobre los resultados de la consulta y crea botones de radio para cada fila
            for i, fila in enumerate(resultados):
                x = 200  # La posición horizontal se mantiene constante
                y = 80 + i * 50
                nombre = fila[0]  # Suponiendo que el nombre está en la primera posición de cada fila
                button = Radiobutton(ventana2, variable=panel_control, value=i, text=nombre)
                button.place(x=x, y=y, width=100, height=50)


            #---------------
            botton4 = Button(ventana2)
            botton4.config(text="Actualizar Producto", font=("Ariel", 8, "bold"))
            botton4.place(x=40, y=400, width = 150, height = 30)

            botton5 = Button(ventana2)
            botton5.config(text="Eliminar Producto", font=("Ariel", 8, "bold"))
            botton5.place(x=300, y=400, width = 150, height = 30)
        def agregar():
            pantallaN = Toplevel(self.ventana)
            pantallaN.geometry("400x250+800+380")
            pantallaN.iconbitmap("Logo_.ico")
            pantallaN.resizable(False,False)
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

        self.agregarBoton = Button(self.ventana)
        self.agregarBoton.config(text="Agregar Producto",font=("Ariel", 14,"bold"), command=agregar)
        self.agregarBoton.place(x=50, y=50, width=200, height=50)

        self.mostrarBoton = Button(self.ventana)
        self.mostrarBoton.config(text="Mostrar Productos", font=("Ariel", 14, "bold"), command=Opciones_aparte)
        self.mostrarBoton.place(x=40, y=110, width=220, height=50)

        self.obtenerBoton = Button(self.ventana)
        self.obtenerBoton.config(text="Obtener Producto ", font=("Ariel", 14, "bold"), command=obtener)
        self.obtenerBoton.place(x=40, y=170, width=220, height=50)

        def retornar_ventana():
            self.ventana.withdraw()
            ventana.deiconify()
        botton_return = Button(self.ventana,image=self.imagen,command=retornar_ventana)
        botton_return.place(x=130,y=230)

        self.ventana.mainloop()
Interfaz_1()


