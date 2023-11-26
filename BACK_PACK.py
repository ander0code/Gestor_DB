from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from datetime import datetime
from CRUD_PRODUCTOS import Crud_Productos
from CONSULTA_PROVEDORES import Consulta_Proveedor
from CONSULTA_HISTORIAL import Consulta_Historial
from CONSULTA_LOGIN import Login
from CRUD_USUARIOS import Crud_Usuarios
from CONSULTA_EXPORTACION import Consulta_Exportacion
import pandas as pd
import sqlite3
from pathlib import Path
from tkinter import simpledialog
from tkinter import filedialog
# pip install openpyxl <-


class Ventana(tb.Window):
    global app
    app = None

    def __init__(self):
        super().__init__()
        self.ventanaLogin()
        self.rol_usuario_actual = None

    def ventanaLogin(self):
        self.frame_login = Frame(self)
        self.frame_login.pack()

        self.lblframe_login = ttk.LabelFrame(self.frame_login, text='Iniciar Sesión', bootstyle="info")
        self.lblframe_login.pack(padx=10, pady=10)

        ruta = Path(__file__).parent  # Buenas Practicas
        archivo = ruta / "Logo.png"
        logo_image = PhotoImage(file=archivo)

        # Mostrar el logo en lugar del texto
        lbllogo = ttk.Label(self.lblframe_login, image=logo_image)
        lbllogo.image = logo_image  # Mantener una referencia para evitar que el recolector de basura lo elimine
        lbllogo.pack(padx=10, pady=35)

        self.txtUsuario = ttk.Entry(self.lblframe_login, width=40, bootstyle='secondary', justify=CENTER)
        self.txtUsuario.pack(padx=10, pady=10)
        self.set_placeholder(self.txtUsuario, "Usuario")

        self.txtClave = ttk.Entry(self.lblframe_login, width=40, bootstyle='secondary', justify=CENTER)
        self.txtClave.pack(padx=10, pady=10)
        self.txtClave.configure(show='*')
        self.set_placeholder(self.txtClave, "Contraseña")

        btnAcceso = ttk.Button(self.lblframe_login, text='Ingresar', bootstyle="info", command=self.logueo)
        btnAcceso.pack(padx=10, pady=10)

    def set_placeholder(self, entry_widget, placeholder):
        entry_widget.insert(0, placeholder)
        entry_widget.bind("<FocusIn>", lambda event: self.on_entry_click(entry_widget, placeholder))
        entry_widget.bind("<FocusOut>", lambda event: self.on_focus_out(entry_widget, placeholder))

    def on_entry_click(self, entry_widget, placeholder):
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, END)

    def on_focus_out(self, entry_widget, placeholder):
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder)

    def ventanaMenu(self):
        global app
        Centrar_ventana(app,170,400)
        tb.Style('darkly')
        self.frameLeft = Frame(self, width=200)
        self.frameLeft.grid(row=0, column=0, sticky=NSEW)
        self.frameCenter = Frame(self)
        self.frameCenter.grid(row=0, column=1, sticky=NSEW)

        bienvenida_label = ttk.Label(self.frameLeft, text=f'¡Bienvenido, {self.txtUsuario.get()}!',
                                     font=('Arial', 12, 'bold'))
        bienvenida_label.grid(row=0, column=0, padx=10, pady=10, sticky=N)

        btnProductos = ttk.Button(self.frameLeft, text='Productos', width=15,
                                  command=lambda: [self.ventanaListaProductos(),
                                                   Centrar_ventana(app,870,450)])
        btnProductos.grid(row=1, column=0, padx=10, pady=10)

        btnClientes = ttk.Button(self.frameLeft, text='Proveedores', width=15,
                                 command=lambda: [self.ventanaListaUsuarios(mostrar_proveedores=True),
                                                  Centrar_ventana(app,830,450)])
        btnClientes.grid(row=2, column=0, padx=10, pady=10)


        btnUsuarios = ttk.Button(self.frameLeft, text='Usuarios', width=15,
                                 command=lambda: [self.ventanaListaUsuarios(mostrar_proveedores=False),
                                                  Centrar_ventana(app,830,450)])
        if not self.es_administrador_actual():
            btnUsuarios.config(state="disable")
        else:
            btnUsuarios.config(state="normal")
        btnUsuarios.grid(row=3, column=0, padx=10, pady=10)

        btnReportes = ttk.Button(self.frameLeft, text='Reportes', width=15,
                                 command=lambda: [self.mostrarHistorial(),
                                                  Centrar_ventana(app,780,400)])
        btnReportes.grid(row=4, column=0, padx=10, pady=10)

        btnExportarDB = ttk.Button(self.frameLeft, text='Exportar Tabla', width=15,
                                   command=self.ventana_Imprimir_Resgistro)
        btnExportarDB.grid(row=5, column=0, padx=10, pady=10)
        btnRestaurar_DB = ttk.Button(self.frameLeft, text='Restaurar Tabla', width=15,
                                     command=self.subventanborrarTabla)
        if not self.es_administrador_actual():
            btnRestaurar_DB.config(state="disable")
        else:
            btnRestaurar_DB.config(state="normal")
        btnRestaurar_DB.grid(row=6, column=0, padx=10, pady=10)

        btnSalirDelPrograma = ttk.Button(self.frameLeft, text='Salir', width=15, bootstyle='danger',
                                         command=self.BtnSalir)
        btnSalirDelPrograma.grid(row=7, column=0, padx=10, pady=10)

    def BtnSalir(self):
        self.destroy()
    def logueo(self):

        try:
            db = Login()
            nombreUsuario = self.txtUsuario.get()
            claveUsuario = self.txtClave.get()

            datosLogueo = db.verificacion(nombreUsuario, claveUsuario)

            if datosLogueo:
                for row in datosLogueo:
                    codUsuario = row[0]
                    nomUsuario = row[1]
                    claUsuario = row[2]
                    rolUsuario = row[3]

                if nomUsuario == self.txtUsuario.get() and claUsuario == self.txtClave.get():
                    self.rol_usuario_actual = rolUsuario

                    self.frame_login.pack_forget()

                    self.ventanaMenu()
            else:
                self.txtUsuario.delete(0, "end")
                self.txtClave.delete(0, "end")
                self.set_placeholder(self.txtUsuario, "Usuario")
                self.set_placeholder(self.txtClave, "Contraseña")
                messagebox.showerror("INICIO SECION", "DATOS INCORRECTOS")

        except sqlite3.Error as e:
            messagebox.showerror("Acceso", f"Ocurrió un error: {e}")
    # ---------------USUARIOS------------
    def ventanaListaUsuarios(self, mostrar_proveedores=False):
        self.frameListaUsuarios = Frame(self.frameCenter)
        self.frameListaUsuarios.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframeBotonesListUsu = LabelFrame(self.frameListaUsuarios)
        self.lblframeBotonesListUsu.grid(row=0, column=0, sticky=NSEW)

        self.lblframeBusqListUsu = LabelFrame(self.frameListaUsuarios)
        self.lblframeBusqListUsu.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        self.txtBusquedaUsuarios = ttk.Entry(self.lblframeBusqListUsu, width=100)
        self.txtBusquedaUsuarios.grid(row=0, column=0, padx=5, pady=5)
        if mostrar_proveedores:
            self.txtBusquedaUsuarios.bind('<Key>', self.buscarProveedores)

        else:
            self.txtBusquedaUsuarios.bind('<Key>', self.buscarUsuarios)

        # ====================TreeView===============
        self.lblframeTreeListUsu = LabelFrame(self.frameListaUsuarios)
        self.lblframeTreeListUsu.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo", "nombre", "clave", "rol")

        self.TreelistUsuarios = tb.Treeview(self.lblframeTreeListUsu,
                                            columns=columnas, height=17,
                                            show='headings', bootstyle='info')
        self.TreelistUsuarios.grid(row=0, column=0)

        self.TreelistUsuarios.heading("codigo", text="CODIGO", anchor=W)
        self.TreelistUsuarios.heading("nombre", text="NOMBRE", anchor=W)
        self.TreelistUsuarios.heading("clave", text="CLAVE", anchor=W)
        self.TreelistUsuarios.heading("rol", text="ROL", anchor=W)

        self.TreelistUsuarios['displaycolumns'] = ['codigo', 'nombre', 'rol']
        if mostrar_proveedores:
            self.TreelistUsuarios.bind("<<TreeviewSelect>>", self.activar_boton_historial_proveedor)
        else:
            self.TreelistUsuarios.bind("<<TreeviewSelect>>", self.activar_boton_Modificar_Eliminar)

        TreeScrollListUsu = tb.Scrollbar(self.frameListaUsuarios, bootstyle='round-success')
        TreeScrollListUsu.grid(row=2, column=1,)
            # Configu el scroll
        TreeScrollListUsu.config(command=self.TreelistUsuarios.yview)

        if mostrar_proveedores:

            self.btnNuevoUsuario = tb.Button(self.lblframeBotonesListUsu, text='Lista Productos', width=15,
                                             bootstyle="success", state="disabled",
                                             command=self.ventanaListaProductosProvedor)
            self.btnNuevoUsuario.grid(row=0, column=0, padx=5, pady=5)
            self.mostrar_proveedores()

        else:

            btnNuevoUsuario = tb.Button(self.lblframeBotonesListUsu, text='Nuevo', width=15, bootstyle="success",
                                        command=self.ventanaNuevoUsuario)
            btnNuevoUsuario.grid(row=0, column=0, padx=5, pady=5)

            self.btnModificarUsuario = tb.Button(self.lblframeBotonesListUsu, text='Modificar', width=15,
                                                 bootstyle="warning", state="disabled",
                                                 command=self.ventanaModificarUsuario)
            self.btnModificarUsuario.grid(row=0, column=1, padx=5, pady=5)

            self.btnEliminarUsuario = tb.Button(self.lblframeBotonesListUsu, text='Eliminar',
                                                width=15,
                                                bootstyle="danger",
                                                state="disabled", command=self.borrarUsuario)
            self.btnEliminarUsuario.grid(row=0, column=2, padx=5, pady=5)

            self.MostrarUsuarios()

    def activar_boton_Modificar_Eliminar(self, event):
        item_seleccionado = self.TreelistUsuarios.focus()
        if item_seleccionado:
            self.btnModificarUsuario.config(state="normal")
            self.btnEliminarUsuario.config(state="normal")

    def activar_boton_historial_proveedor(self, event):
        item_seleccionado = self.TreelistUsuarios.focus()
        if item_seleccionado:
            self.btnNuevoUsuario.config(state="normal")
        else:
            self.btnNuevoUsuario.config(state="disabled")

    def MostrarUsuarios(self):

        try:

            db = Crud_Usuarios()

            datos = db.Mostrar_Usuarios()

            registros = self.TreelistUsuarios.get_children()

            for elementos in registros:
                self.TreelistUsuarios.delete(elementos)

            for row in datos:
                self.TreelistUsuarios.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3]))

        except sqlite3.Error as e:

            print("Error de SQLite:", e)
            messagebox.showerror("Lista de Usuario",
                                 f"Ocurrió un error al mostrar la lista de usuario: {e}")

    def ventanaNuevoUsuario(self):

        if not self.es_administrador_actual():
            messagebox.showwarning('Modificar Usuario', 'No tienes permisos para modificar usuarios')
            return

        self.frameNewUser = Toplevel(self)
        self.frameNewUser.title('Nuevo Usuario')
        Centrar_ventana(self.frameNewUser,400,300)
        self.frameNewUser.resizable(False, False)
        self.frameNewUser.grab_set()

        lblframeNewUser = LabelFrame(self.frameNewUser)
        lblframeNewUser.grid(row=0, column=0, sticky=NSEW, padx=25, pady=35)

        lblCodeModifyUser = Label(lblframeNewUser, text='Codigo')
        lblCodeModifyUser.grid(row=0, column=0, padx=10, pady=10, sticky=E)
        self.txtCodeNewUser = ttk.Entry(lblframeNewUser, width=40)
        self.txtCodeNewUser.grid(row=0, column=1, padx=10, pady=10)

        lblNameNewUser = Label(lblframeNewUser, text='Nombre')
        lblNameNewUser.grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.txtNameNewUser = ttk.Entry(lblframeNewUser, width=40)
        self.txtNameNewUser.grid(row=1, column=1, padx=10, pady=10)

        lblClaveNewUser = Label(lblframeNewUser, text='Clave')
        lblClaveNewUser.grid(row=2, column=0, padx=10, pady=10, sticky=E)
        self.txtClaveNewUser = ttk.Entry(lblframeNewUser, width=40)
        self.txtClaveNewUser.grid(row=2, column=1, padx=10, pady=10)

        lblRolNewUser = Label(lblframeNewUser, text='Rol')
        lblRolNewUser.grid(row=3, column=0, padx=10, pady=10, sticky=E)
        self.txtRolNewUser = ttk.Combobox(lblframeNewUser, values=('Administrador', 'Proveedor', 'Vendedor'),
                                          width=38, state='readonly')
        self.txtRolNewUser.grid(row=3, column=1, padx=10, pady=10)
        self.txtRolNewUser.current(0)

        btnSaveNewUser = ttk.Button(lblframeNewUser, text='Guardar', width=38, command=self.guardarUsuario)
        btnSaveNewUser.grid(row=4, column=1, padx=10, pady=10)

        self.registrar_en_historial("Usuario ha sido creado por: ", self.txtUsuario.get())

        self.ultimoUsuario()

        self.txtNameNewUser.focus()

    def guardarUsuario(self):

        if self.txtCodeNewUser.get() == "" or self.txtNameNewUser.get() == "" or self.txtClaveNewUser.get() == "":
            messagebox.showwarning('Guardando usuarios', 'Algún campo no es válido, por favor revisar')
            return
        try:

            db = Crud_Usuarios()

            datosGuardarUsuarios = (self.txtCodeNewUser.get(),
                                    self.txtNameNewUser.get(),
                                    self.txtClaveNewUser.get(),
                                    self.txtRolNewUser.get())

            db.Guardar_Usuario(datosGuardarUsuarios)

            messagebox.showinfo('Guardando Usuarios', "Usuario Guardado Correctamente")

            self.frameNewUser.destroy()
            self.ventanaListaUsuarios()
            # Cerrar la conexi

        except:
            messagebox.showerror("Guardando Usuarios", "Ocurrió un error al Guardar Usuario")

    def ultimoUsuario(self):
        try:
            db = Crud_Usuarios()
            datos = db.Ultimo_Usuario()
            for codusu in datos:
                codusu = codusu[0]
                if codusu == None:
                    self.ultusu = (int(1))
                    self.txtCodeNewUser.config(state=NORMAL)
                    self.txtCodeNewUser.insert(0, self.ultusu)
                    self.txtCodeNewUser.config(state='readonly')
                    break

                if codusu == "":
                    self.ultusu = (int(1))
                    self.txtCodeNewUser.config(state=NORMAL)
                    self.txtCodeNewUser.insert(0, self.ultusu)
                    self.txtCodeNewUser.config(state='readonly')
                    break

                else:
                    self.ultusu = (int(codusu) + 1)
                    self.txtCodeNewUser.config(state=NORMAL)
                    self.txtCodeNewUser.insert(0, self.ultusu)
                    self.txtCodeNewUser.config(state='readonly')
        except ValueError as e:
            print("error {}".format(e))

    def buscarUsuarios(self, event):
        try:
            db = Crud_Usuarios()
            registros = self.TreelistUsuarios.get_children()
            for elementos in registros:
                self.TreelistUsuarios.delete(elementos)
            busqueda = self.txtBusquedaUsuarios.get()
            if busqueda:
                # Consultar DB
                datos = db.Buscar_Usuario(busqueda)
            else:

                datos = db.Buscar_Usuario(busqueda)

            for row in datos:
                self.TreelistUsuarios.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))
        except:

            print("Busqueda de usuarios", "Ocurrió un error al buscar en la lista de usuarios")

    def ventanaModificarUsuario(self):

        if not self.es_administrador_actual():
            messagebox.showwarning('Modificar Usuario', 'No tienes permisos para modificar usuarios')
            return

        self.usuarioSeleccionado = self.TreelistUsuarios.focus()
        self.ValModUsu = self.TreelistUsuarios.item(self.usuarioSeleccionado, 'values')

        if self.ValModUsu != '':
            self.frameModifyUser = Toplevel(self)
            self.frameModifyUser.title('Nuevo Usuario')
            Centrar_ventana(self.frameModifyUser,400,300)

            self.frameModifyUser.resizable(False, False)
            self.frameModifyUser.grab_set()

            lblModifyUser = LabelFrame(self.frameModifyUser)
            lblModifyUser.grid(row=0, column=0, sticky=NSEW, padx=25, pady=35)

            lblCodeModifyUser = Label(lblModifyUser, text='Codigo')
            lblCodeModifyUser.grid(row=0, column=0, padx=10, pady=10, sticky=E)
            self.txtCodeModifyUser = ttk.Entry(lblModifyUser, width=40)
            self.txtCodeModifyUser.grid(row=0, column=1, padx=10, pady=10)

            lblModifyNewUser = Label(lblModifyUser, text='Nombre')
            lblModifyNewUser.grid(row=1, column=0, padx=10, pady=10, sticky=E)
            self.txtNameModifyUser = ttk.Entry(lblModifyUser, width=40)
            self.txtNameModifyUser.grid(row=1, column=1, padx=10, pady=10)

            lblClaveModifyUser = Label(lblModifyUser, text='Clave')
            lblClaveModifyUser.grid(row=2, column=0, padx=10, pady=10, sticky=E)
            self.txtClaveModifyUser = ttk.Entry(lblModifyUser, width=40)
            self.txtClaveModifyUser.grid(row=2, column=1, padx=10, pady=10)

            lblRolModifyUser = Label(lblModifyUser, text='Rol')
            lblRolModifyUser.grid(row=3, column=0, padx=10, pady=10, sticky=E)
            self.txtRolModifyUser = ttk.Combobox(lblModifyUser, values=('Administrador', 'Proveedor', 'Vendedor'),
                                                 width=38)
            self.txtRolModifyUser.grid(row=3, column=1, padx=10, pady=10)

            btnSaveModifyUser = ttk.Button(lblModifyUser, text='Modificar', width=38, bootstyle='warning',
                                           command=self.modificarUsuario)
            btnSaveModifyUser.grid(row=4, column=1, padx=10, pady=10)
            self.llenarEntrysPaModificarUser()

            self.txtNameModifyUser.focus()

    def llenarEntrysPaModificarUser(self):

        self.txtCodeModifyUser.delete(0, END)
        self.txtNameModifyUser.delete(0, END)
        self.txtClaveModifyUser.delete(0, END)
        self.txtRolModifyUser.delete(0, END)

        self.txtCodeModifyUser.insert(0, self.ValModUsu[0])
        self.txtCodeModifyUser.config(state='readonly')
        self.txtNameModifyUser.insert(0, self.ValModUsu[1])
        self.txtClaveModifyUser.insert(0, self.ValModUsu[2])
        self.txtRolModifyUser.insert(0, self.ValModUsu[3])
        self.txtRolModifyUser.config(state='readonly')

    def modificarUsuario(self):

        if self.txtCodeModifyUser.get() == "" or self.txtNameModifyUser.get() == "" or self.txtClaveModifyUser.get() == "":
            messagebox.showwarning('Modificando usuarios', 'Algún campo no es válido, por favor revisar')
            return

        try:
            db = Crud_Usuarios()
            datosModificarUsuarios = (self.txtNameModifyUser.get(),
                                      self.txtClaveModifyUser.get(),
                                      self.txtRolModifyUser.get())
            db.Modificar_Usuario(self.txtCodeModifyUser.get(),datosModificarUsuarios)
            messagebox.showinfo('Modificar Usuarios', "Usuario Modificado Correctamente")

            self.ValModUsu = self.TreelistUsuarios.item(
                self.usuarioSeleccionado, text='',
                values=(self.txtCodeModifyUser.get(),
                        self.txtNameModifyUser.get(),
                        self.txtClaveModifyUser.get(),
                        self.txtRolModifyUser.get(),))

            self.registrar_en_historial(f"{self.txtNameModifyUser.get()} ha sido modificado por: ",
                                        self.txtUsuario.get())
            self.frameModifyUser.destroy()
            self.ventanaListaUsuarios()


        except:
            messagebox.showerror("Modificar Usuarios", "Ocurrió un error al Modificar Usuario")

    def borrarUsuario(self):
        # Validar si se ha seleccionado un usuario para borrar
        usuario_seleccionado = self.TreelistUsuarios.focus()
        valores_usuario = self.TreelistUsuarios.item(usuario_seleccionado, 'values')

        if not valores_usuario:
            messagebox.showwarning('Borrando usuarios', 'Por favor, selecciona un usuario para borrar')
            return

        codigo_usuario = valores_usuario[0]
        nombre_usuario = valores_usuario[1]
        rol_usuario = valores_usuario[3]

        # Verificar que el usuario tenga permiso para borrar
        if not self.es_administrador_actual():
            messagebox.showwarning('Borrar Usuario', 'No tienes permisos para eliminar usuarios')
            return

        # Si el usuario que se intenta borrar es administrador, verificar que el rol actual también sea administrador
        if rol_usuario == 'Administrador' and not self.es_administrador_actual():
            messagebox.showwarning('Borrar Usuario', 'No tienes permisos para eliminar a un administrador')
            return

        # Pedir confirmación de contraseña
        contraseña_confirmacion = simpledialog.askstring(
            'Confirmar Eliminación',
            f'Ingrese la contraseña para confirmar la eliminación del usuario {nombre_usuario}:', show='*'
        )

        if not contraseña_confirmacion:
            return  # El usuario cerró la ventana de confirmación o no ingresó contraseña

        try:
            # Establecer conexión
            db = Crud_Usuarios()

            # Consultar DB y verificar la contraseña
            resultado = db.Verifica_Usuario(codigo_usuario, )

            if resultado and resultado[0] == contraseña_confirmacion:
                # Eliminar el usuario
                db.Borrar_Usuario(codigo_usuario, )
                # Aplicar Cambios
                messagebox.showinfo('Borrar Usuario', "Usuario Borrado Correctamente")
                # Cerrar la conexion
                self.registrar_en_historial("Un usuario ha borrado por: ", self.txtUsuario.get())
                # Actualizar la lista de usuarios después de borrar
                self.ventanaListaUsuarios()
            else:
                messagebox.showerror('Error', 'Contraseña incorrecta')

        except sqlite3.Error as e:
            messagebox.showerror("Borrar Usuario", "Ocurrió un error al borrar el usuario: {}".format(e))

    def es_administrador_actual(self):
        # Verificar si el rol almacenado es "Administrador"
        return self.rol_usuario_actual == 'Administrador'

    # ---------------Proveedor------------
    def ventanaListaProductosProvedor(self):

        self.frameListaProductos = Toplevel(self)
        self.frameListaProductos.title('Lista de Productos')
        self.frameListaProductos.resizable(False, False)
        Centrar_ventana(self.frameListaProductos,650,340)

        self.frameListaProductos.grab_set()
        self.lblframeBotonesListProd = LabelFrame(self.frameListaProductos)
        self.lblframeBotonesListProd.grid(row=0, column=0, sticky=NSEW)

        self.lblframeTreeListProd = LabelFrame(self.frameListaProductos)
        self.lblframeTreeListProd.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("ID Producto", "Nombre_proveedor", "Nombre del Producto", "Precio", "Stock", "Descripción")
        self.TreelistProductosPro = tb.Treeview(self.lblframeTreeListProd, columns=columnas, height=17, show='headings',
                                                bootstyle='info')
        self.TreelistProductosPro.grid(row=0, column=0)
        self.TreelistProductosPro.heading("ID Producto", text="ID PRODUCTO", anchor=W)
        self.TreelistProductosPro.column("ID Producto", width=100, anchor=W, stretch=NO)

        self.TreelistProductosPro.heading("Nombre_proveedor", text="PROVEEDOR", anchor=W)
        self.TreelistProductosPro.column("Nombre_proveedor", width=100, anchor=W, stretch=NO)

        self.TreelistProductosPro.heading("Nombre del Producto", text="PRODUCTO", anchor=W)
        self.TreelistProductosPro.column("Nombre del Producto", width=100, anchor=W, stretch=NO)

        self.TreelistProductosPro.heading("Precio", text="PRECIO", anchor=W)
        self.TreelistProductosPro.column("Precio", width=100, anchor=W, stretch=NO)

        self.TreelistProductosPro.heading("Stock", text="STOCK", anchor=W)
        self.TreelistProductosPro.column("Stock", width=100, anchor=W, stretch=NO)

        self.TreelistProductosPro.heading("Descripción", text="DESCRIPCIÓN", anchor=W)
        self.TreelistProductosPro.column("Descripción", width=100, anchor=W, stretch=NO)

        self.TreelistProductosPro['displaycolumns'] = ['ID Producto', 'Nombre_proveedor', 'Nombre del Producto',
                                                       'Precio', 'Stock', 'Descripción']
        # Creando el scrollbar
        TreeScrollListProd = tb.Scrollbar(self.frameListaProductos, bootstyle='round-success')
        TreeScrollListProd.grid(row=2, column=1)
        TreeScrollListProd.config(command=self.TreelistProductosPro.yview)
        self.MostrarProductosProveedor()

    def mostrar_proveedores(self):
        crud = Consulta_Proveedor()
        datos = crud.mostrar_proveedores()
        registros = self.TreelistUsuarios.get_children()
        for elementos in registros:
            self.TreelistUsuarios.delete(elementos)

        for row in datos:
            self.TreelistUsuarios.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3]))

    def MostrarProductosProveedor(self):
        proveedor_seleccionado = self.TreelistUsuarios.focus()
        proveedor_codigo = self.TreelistUsuarios.item(proveedor_seleccionado, 'text')
        crud = Consulta_Proveedor()
        productos = crud.mostrar_productos_proveedor(proveedor_codigo)
        registros = self.TreelistProductosPro.get_children()
        for elementos in registros:
            self.TreelistProductosPro.delete(elementos)
        for producto in productos:
            values = (producto[1], producto[0], producto[3], producto[4], producto[5], producto[6])
            self.TreelistProductosPro.insert('', 'end', values=values)

    def buscarProveedores(self, event):
        registros = self.TreelistUsuarios.get_children()
        for elementos in registros:
            self.TreelistUsuarios.delete(elementos)
        nombre_proveedor = self.txtBusquedaUsuarios.get()
        crud = Consulta_Proveedor()
        proveedores = crud.buscar_proveedores(nombre_proveedor)
        for proveedor in proveedores:
            # Llenar treewbiew
            self.TreelistUsuarios.insert("", 0, text=proveedor[0],
                                         values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3]))


    # ----------Productos-----------
    def ventanaListaProductos(self):

        self.frameListaProducto = Frame(self.frameCenter)
        self.frameListaProducto.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframeBotonesListProduc = LabelFrame(self.frameListaProducto)
        self.lblframeBotonesListProduc.grid(row=0, column=0, sticky=NSEW)

        btnNuevoProduct = tb.Button(self.lblframeBotonesListProduc, text='Nuevo', width=15, bootstyle="success",
                                    command=self.ventanaNuevoProducto)
        btnNuevoProduct.grid(row=0, column=0, padx=5, pady=5)

        self.btnModificarProduc = tb.Button(self.lblframeBotonesListProduc, text='Modificar', width=15,
                                            bootstyle="warning",
                                            state="disabled", command=self.ventanaModificarProductos)
        self.btnModificarProduc.grid(row=0, column=1, padx=5, pady=5)

        self.btnEliminarProduc = tb.Button(self.lblframeBotonesListProduc, text='Eliminar', width=15,
                                           bootstyle="danger",
                                           state="disabled", command=self.borrarProducto)
        self.btnEliminarProduc.grid(row=0, column=2, padx=5, pady=5)

        self.lblframeBusqListProduct = LabelFrame(self.frameListaProducto)
        self.lblframeBusqListProduct.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        self.txtBusquedaProducts = ttk.Entry(self.lblframeBusqListProduct, width=100)
        self.txtBusquedaProducts.grid(row=0, column=0, padx=5, pady=5)
        self.txtBusquedaProducts.bind('<Key>', self.buscarProductos)

        # ====================TreeView===============
        self.lblframeTreeListProduct = LabelFrame(self.frameListaProducto)
        self.lblframeTreeListProduct.grid(row=2, column=0, padx=5, pady=10, sticky=NSEW)

        columnas = ("id_Producto", "ID_Proveedor", "NombreProveedor", "producto", "precio", "stock", "descripcion")

        self.TreelistProductosProductos = tb.Treeview(self.lblframeTreeListProduct, columns=columnas,
                                                      height=17, show='headings', bootstyle='info')
        self.TreelistProductosProductos.grid(row=0, column=0)

        self.TreelistProductosProductos.heading("id_Producto", text="ID PRODUCTO", anchor=W)
        self.TreelistProductosProductos.column("id_Producto", width=100, anchor=W, stretch=NO)

        self.TreelistProductosProductos.heading("ID_Proveedor", text="ID PROVEEDOR", anchor=W)
        self.TreelistProductosProductos.column("ID_Proveedor", width=100, anchor=W, stretch=NO)


        self.TreelistProductosProductos.heading("NombreProveedor", text="PROVEEDOR", anchor=W)
        self.TreelistProductosProductos.column("NombreProveedor", width=100, anchor=W, stretch=NO)

        self.TreelistProductosProductos.heading("producto", text="PRODUCTO", anchor=W)
        self.TreelistProductosProductos.column("producto", width=150, anchor=W, stretch=NO)

        self.TreelistProductosProductos.heading("precio", text="PRECIO", anchor=W)
        self.TreelistProductosProductos.column("precio", width=100, anchor=W, stretch=NO)

        self.TreelistProductosProductos.heading("stock", text="STOCK", anchor=W)
        self.TreelistProductosProductos.column("stock", width=100, anchor=W, stretch=NO)

        self.TreelistProductosProductos.heading("descripcion", text="DESCRIPCIÓN", anchor=W)
        self.TreelistProductosProductos.column("descripcion", width=100, anchor=W, stretch=NO)


        self.TreelistProductosProductos['displaycolumns'] = ['id_Producto', 'NombreProveedor',
                                                             'producto', 'precio', 'stock', 'descripcion']

        self.TreelistProductosProductos.bind("<<TreeviewSelect>>", self.activar_boton_modi_elimi_productos)
        # Creando el rico scrollbar
        TreeScrollListProduct = tb.Scrollbar(self.frameListaProducto, bootstyle='round-success')
        TreeScrollListProduct.grid(row=2, column=1)
        # Configu el scroll
        TreeScrollListProduct.config(command=self.TreelistProductosProductos.yview)

        self.MostrarProductos()

    def activar_boton_modi_elimi_productos(self, event):
        item_seleccionado = self.TreelistProductosProductos.focus()
        if item_seleccionado:
            self.btnModificarProduc.config(state="normal")
            self.btnEliminarProduc.config(state="normal")

    def MostrarProductos(self):

        try:
            Crud = Crud_Productos()
            datos = Crud.mostrar_productos()

            registros = self.TreelistProductosProductos.get_children()

            for elementos in registros:
                self.TreelistProductosProductos.delete(elementos)

            for row in datos:
                self.TreelistProductosProductos.insert("", "end",
                                                       text=row[0],
                                                       values=(row[1], row[2], row[0], row[3], row[4], row[5], row[6]))

        except sqlite3.Error as e:

            print("Error de SQLite:", e)
            messagebox.showerror("Lista de Productos",
                                 f"Ocurrió un error al mostrar la lista de Productos: {e}")

    def ventanaNuevoProducto(self):
        self.frameNewProduct = Toplevel(self)
        self.frameNewProduct.title('Nuevo Producto')
        Centrar_ventana(self.frameNewProduct,440,380)
        self.frameNewProduct.resizable(False, False)
        self.frameNewProduct.grab_set()

        self.db = Consulta_Proveedor()
        self.datos = self.db.Obetener_proveedores()

        lblframeNewProduc = LabelFrame(self.frameNewProduct)
        lblframeNewProduc.grid(row=0, column=0, sticky=NSEW, padx=25, pady=35)

        lblCodeModifyProduct = Label(lblframeNewProduc, text='ID PROVEEDOR')
        lblCodeModifyProduct.grid(row=0, column=0, padx=10, pady=10, sticky=E)
        selecionProveedor = StringVar()
        self.txtCodeNewProduc = ttk.Combobox(lblframeNewProduc, values=self.datos,
                                             textvariable=selecionProveedor, width=40, state='readonly')
        self.txtCodeNewProduc.grid(row=0, column=1, padx=10, pady=10)

        lblNameNewProduct = Label(lblframeNewProduc, text='PRODUCTO')
        lblNameNewProduct.grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.txtNameNewProduct = ttk.Entry(lblframeNewProduc, width=40)
        self.txtNameNewProduct.grid(row=1, column=1, padx=10, pady=10)

        lblPrecioNewProduct = Label(lblframeNewProduc, text='PRECIO')
        lblPrecioNewProduct.grid(row=2, column=0, padx=10, pady=10, sticky=E)
        self.txtPrecioNewProduct = ttk.Entry(lblframeNewProduc, width=40)
        self.txtPrecioNewProduct.grid(row=2, column=1, padx=10, pady=10)

        lblStockNewProduct = Label(lblframeNewProduc, text='STOCK')
        lblStockNewProduct.grid(row=3, column=0, padx=10, pady=10, sticky=E)
        self.txtStockNewProduct = ttk.Entry(lblframeNewProduc, width=40)
        self.txtStockNewProduct.grid(row=3, column=1, padx=10, pady=10)

        lblDescripcionNewProduct = Label(lblframeNewProduc, text='DESCRIPCIÓN')
        lblDescripcionNewProduct.grid(row=4, column=0, padx=10, pady=10, sticky=E)
        self.txtDescripcionNewProduct = ttk.Entry(lblframeNewProduc, width=40)
        self.txtDescripcionNewProduct.grid(row=4, column=1, padx=10, pady=10)

        btnSaveNewProduct = ttk.Button(lblframeNewProduc, text='Guardar', width=38, command=self.guardarProducto)
        btnSaveNewProduct.grid(row=5, column=1, padx=10, pady=10)
        self.txtNameNewProduct.focus()

    def eliminar_letras(self, cadena):
        solo_numeros = ''
        for caracter in cadena:
            if caracter.isdigit():
                solo_numeros += caracter
        return solo_numeros

    def guardarProducto(self):

        if (self.txtCodeNewProduc.get() == ""
                or self.txtNameNewProduct.get() == ""
                or self.txtPrecioNewProduct.get() == ""
                or self.txtStockNewProduct.get() == ""
                or self.txtDescripcionNewProduct.get() == ""):
            messagebox.showwarning('Guardando Producto', 'Algún campo no es válido, por favor revisar')
            return
        # Capturar errores
        try:
            # Establecer conexión
            Crud = Crud_Productos()
            dato_nuevo = self.eliminar_letras(self.txtCodeNewProduc.get())
            Crud.Guardar_Producto(dato_nuevo, self.txtNameNewProduct.get(),
                                  self.txtPrecioNewProduct.get(), self.txtStockNewProduct.get(),
                                  self.txtDescripcionNewProduct.get()
                                  )
            messagebox.showinfo('Guardando Producto', "Usuario Guardado Correctamente")
            self.frameNewProduct.destroy()
            self.registrar_en_historial(f"Un Producto a sido agregago por : ",
                                        self.txtUsuario.get())
            self.ventanaListaProductos()
            # Cerrar la conexion
        except sqlite3.Error as e:
            print("Error de SQLite:", e)
            messagebox.showerror("Guardando Productos", f"Ocurrió un error al Guardar Productos: {e}")

    def buscarProductos(self, event):
        # Capturar errores
        try:
            Crud = Crud_Productos()
            # Limpiar data del treeview
            registros = self.TreelistProductosProductos.get_children()
            # Recorrer registros
            for elementos in registros:
                self.TreelistProductosProductos.delete(elementos)
            busqueda = self.txtBusquedaProducts.get()
            if busqueda:
                # Consultar DB
                datos = Crud.Buscar_Productos(busqueda)
            else:
                # Consulta completa si el campo de búsqueda está vacío
                datos = Crud.Buscar_Productos(busqueda)
                # Traer todos los registros y guardar en "datos"

                # Recorrer cada fila encontrada
            for row in datos:
                # Llenar treewbiew
                self.TreelistProductosProductos.insert("", "end", text=row[0],
                                                       values=(row[1], row[2], row[0], row[3], row[4], row[5], row[6]))

        except sqlite3.Error as e:
            # Mensaje de error porsiaca
            print("Busqueda de productos", f"Ocurrió un error al buscar en la lista de productos: {e}")

    def ventanaModificarProductos(self):

        self.ProductoSeleccionado = self.TreelistProductosProductos.focus()
        self.ValModPro = self.TreelistProductosProductos.item(self.ProductoSeleccionado, 'values')

        if self.ValModPro != '':
            self.frameModifyProduc = Toplevel(self)
            self.frameModifyProduc.title('Nuevo Usuario')
            Centrar_ventana(self.frameModifyProduc,500,430)
            # self.CentrarVentanaModificarUser(400,300)#tamaño
            self.frameModifyProduc.resizable(False, False)
            self.frameModifyProduc.grab_set()
            self.db = Consulta_Proveedor()
            self.datos = self.db.Obetener_proveedores()
            lblModifyProduct = LabelFrame(self.frameModifyProduc)
            lblModifyProduct.grid(row=0, column=0, sticky=NSEW, padx=25, pady=35)

            lblCodeProducModifyProduct = Label(lblModifyProduct, text='Codigo del producto')
            lblCodeProducModifyProduct.grid(row=0, column=0, padx=10, pady=10, sticky=E)
            self.txtCodeProductoModifyProduct = ttk.Entry(lblModifyProduct, width=40)
            self.txtCodeProductoModifyProduct.grid(row=0, column=1, padx=10, pady=10)

            lblCodeModifyProduct = Label(lblModifyProduct, text='Nuevo Codigo de provedor')
            lblCodeModifyProduct.grid(row=1, column=0, padx=10, pady=10, sticky=E)
            selecionProveedor = StringVar()
            self.txtCodeProveModifyProduct = ttk.Combobox(lblModifyProduct, values=self.datos,
                                                          textvariable=selecionProveedor, width=40)
            self.txtCodeProveModifyProduct.grid(row=1, column=1, padx=10, pady=10)

            lblModifyNewProduct = Label(lblModifyProduct, text='Nuevo Nombre')
            lblModifyNewProduct.grid(row=2, column=0, padx=10, pady=10, sticky=E)
            self.txtNewNameModifyProduct = ttk.Entry(lblModifyProduct, width=40)
            self.txtNewNameModifyProduct.grid(row=2, column=1, padx=10, pady=10)

            lblClaveModifyProdut = Label(lblModifyProduct, text='Nuevo Precio')
            lblClaveModifyProdut.grid(row=3, column=0, padx=10, pady=10, sticky=E)
            self.txtPrecioModifyProduct = ttk.Entry(lblModifyProduct, width=40)
            self.txtPrecioModifyProduct.grid(row=3, column=1, padx=10, pady=10)

            lblStockModifyProduct = Label(lblModifyProduct, text='Nuevo Stock')
            lblStockModifyProduct.grid(row=4, column=0, padx=10, pady=10, sticky=E)
            self.txtStockModifyProduct = ttk.Entry(lblModifyProduct, width=40)
            self.txtStockModifyProduct.grid(row=4, column=1, padx=10, pady=10)

            lblDescripcionModifyProduct = Label(lblModifyProduct, text='Nuevo Descripcion')
            lblDescripcionModifyProduct.grid(row=5, column=0, padx=10, pady=10, sticky=E)
            self.txtDescripModifyProduct = ttk.Entry(lblModifyProduct, width=40)
            self.txtDescripModifyProduct.grid(row=5, column=1, padx=10, pady=10)

            btnSaveModifyUser = ttk.Button(lblModifyProduct, text='Modificar', width=38, bootstyle='warning',
                                           command=self.modificarProducto)
            btnSaveModifyUser.grid(row=7, column=1, padx=10, pady=10)
            self.llenarEntrysPaModificarProducts()
            # Foco en el nombre usuario
            self.txtNewNameModifyProduct.focus()

    def llenarEntrysPaModificarProducts(self):

        self.txtCodeProductoModifyProduct.delete(0, END)
        self.txtCodeProveModifyProduct.delete(0, END)
        self.txtNewNameModifyProduct.delete(0, END)
        self.txtPrecioModifyProduct.delete(0, END)
        self.txtStockModifyProduct.delete(0, END)
        self.txtDescripModifyProduct.delete(0, END)

        self.txtCodeProductoModifyProduct.insert(0, self.ValModPro[0])
        self.txtCodeProductoModifyProduct.config(state='readonly')
        self.txtCodeProveModifyProduct.insert(0, self.ValModPro[1])
        self.txtNewNameModifyProduct.insert(0, self.ValModPro[3])
        self.txtPrecioModifyProduct.insert(0, self.ValModPro[4])
        self.txtStockModifyProduct.insert(0, self.ValModPro[5])
        self.txtDescripModifyProduct.insert(0, self.ValModPro[6])

    def modificarProducto(self):

        if (self.txtCodeProductoModifyProduct.get() == ""
                or self.txtCodeProveModifyProduct.get() == ""
                or self.txtNewNameModifyProduct.get() == ""
                or self.txtPrecioModifyProduct.get() == ""
                or self.txtStockModifyProduct.get() == ""
                or self.txtDescripModifyProduct.get() == ""):
            messagebox.showwarning('Modificando Producto', 'Algún campo no es válido, por favor revisar')
            return

        try:

            Crud = Crud_Productos()
            dato_nuevo = self.eliminar_letras(self.txtCodeProveModifyProduct.get())
            datosModificarUsuarios = (
                dato_nuevo,
                self.txtNewNameModifyProduct.get(),
                self.txtPrecioModifyProduct.get(),
                self.txtStockModifyProduct.get(),
                self.txtDescripModifyProduct.get())

            Crud.Modificar_Producto(self.txtCodeProductoModifyProduct.get(), datosModificarUsuarios)
            messagebox.showinfo('Modificar Producto', "Producto Modificado Correctamente")

            self.ValModPro = self.TreelistProductosProductos.item(
                self.ProductoSeleccionado,
                text='',
                values=(
                    self.txtCodeProductoModifyProduct.get(),
                    self.txtCodeProveModifyProduct.get(),
                    self.txtNewNameModifyProduct.get(),
                    self.txtPrecioModifyProduct.get(),
                    self.txtStockModifyProduct.get(),
                    self.txtDescripModifyProduct.get(),))

            self.registrar_en_historial(f"{self.txtNewNameModifyProduct.get()} ha sido modificado por: ",
                                        self.txtUsuario.get())
            self.frameModifyProduc.destroy()
            self.ventanaListaProductos()

        except sqlite3.Error as e:
            print("Error de SQLite:", e)
            messagebox.showerror("Modificar Producto", f"Ocurrió un error al Modificar Producto: {e}")

    def borrarProducto(self):

        producto_seleccionado = self.TreelistProductosProductos.focus()
        valores_producto = self.TreelistProductosProductos.item(producto_seleccionado, 'values')

        if not valores_producto:
            messagebox.showwarning('Borrar Producto', 'Selecciona un producto para borrar.')
            return
        id_producto = valores_producto[0]

        try:
            db = Crud_Productos()
            db.Borrar_Producto(id_producto)

            self.ventanaListaProductos()
            messagebox.showinfo('Borrar Producto', 'Producto borrado correctamente.')
            self.registrar_en_historial("Un Producto ha sido borrado por: ", self.txtUsuario.get())
        except ValueError as e:
            messagebox.showerror('Borrar Producto', f'Ocurrió un error al borrar el producto: {e}')

    # ----------Historial------------
    def mostrarHistorial(self):
        for widget in self.frameCenter.winfo_children():
            widget.destroy()
        self.TreelistHistorial = ttk.Treeview(self.frameCenter, columns=("id", "fecha_hora", "accion", "usuario"),
                                              height=17, show='headings', bootstyle='danger')
        self.TreelistHistorial.grid(row=0, column=0,pady=50)

        self.TreelistHistorial.heading("id", text="ID", anchor=W)
        self.TreelistHistorial.column("id", width=90, anchor=W, stretch=NO)

        self.TreelistHistorial.heading("accion", text="ACCIÓN", anchor=W)
        self.TreelistHistorial.column("accion", width=230, anchor=W, stretch=NO)

        self.TreelistHistorial.heading("fecha_hora", text="FECHA-HORA", anchor=W)
        self.TreelistHistorial.column("fecha_hora", width=150, anchor=W, stretch=NO)

        self.TreelistHistorial.heading("usuario", text="USUARIO", anchor=W)
        self.TreelistHistorial.column("usuario", width=100, anchor=W, stretch=NO)
        TreeScrollListHistorial = tb.Scrollbar(self.frameCenter, bootstyle='round-success')
        TreeScrollListHistorial.grid(row=0, column=1,padx=10)
        TreeScrollListHistorial.config(command=self.TreelistHistorial.yview)
        self.cargarHistorial()

    def cargarHistorial(self):
        try:
            db = Consulta_Historial()
            datosHistorial = db.Cargar_Historial()

            for row in datosHistorial:
                self.TreelistHistorial.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Cargar Historial", f"Error al cargar el historial: {e}")

    def registrar_en_historial(self, accion, usuario):
        try:
            db = Consulta_Historial()

            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.Registro_Historial(fecha_hora_actual, accion, usuario)

        except sqlite3.Error as e:
            messagebox.showerror("Registro en Historial", f"Error al registrar en el historial: {e}")

    # borrar tablas
    def subventanborrarTabla(self):
        self.frameborrarTabla = Toplevel(self)
        self.frameborrarTabla.title('Borrar Tabla')
        Centrar_ventana(self.frameborrarTabla,135,100)
        self.frameborrarTabla.grab_set()
        btnborrarHistorial = ttk.Button(self.frameborrarTabla, text='Borrar Historial', width=15,
                                        command=self.borrar_tabla_historial)
        btnborrarHistorial.grid(row=0, column=0, padx=10, pady=10)

        btnborraProduc = ttk.Button(self.frameborrarTabla, text='Borrar Producto', width=15,
                                    command=self.borrar_tabla_producto)
        btnborraProduc.grid(row=1, column=0, padx=10, pady=10)

    def borrar_tabla_historial(self):
        borra = Consulta_Historial()
        borra.borrar_tabla()
        messagebox.showinfo("Borrar Tabla Historial", "Tabla exitosamente Borrada")
        self.mostrarHistorial()
        self.frameborrarTabla.destroy()

    def borrar_tabla_producto(self):
        borra = Crud_Productos()
        borra.borrar_tabla()
        messagebox.showinfo("Borrar Tabla Producto", "Tabla exitosamente Borrada")
        self.mostrarHistorial()
        self.frameborrarTabla.destroy()

    # ------------------------- Registro_exel ---------------
    def ventana_Imprimir_Resgistro(self):
        self.ventana_Registro_Excel = Toplevel(self)
        self.ventana_Registro_Excel.title('Extracción')
        Centrar_ventana(self.ventana_Registro_Excel,285,150)
        self.ventana_Registro_Excel.grab_set()
        txtTexto = ttk.Label(self.ventana_Registro_Excel, text='Indique que tabla desea Imprimir',
                             font=('Coolvetica', 10, 'bold'), wraplength=250)
        txtTexto.grid(row=0, column=1, padx=10, pady=10)

        selecionTabla = IntVar()
        self.txtTablaImpre = ttk.Combobox(self.ventana_Registro_Excel, values=("Producto", "Historial"),
                                          textvariable=selecionTabla, width=40, state='readonly')
        self.txtTablaImpre.grid(row=1, column=1, padx=10, pady=10)

        btnExpoExcel = ttk.Button(self.ventana_Registro_Excel, text='Imprimir', width=15,
                                  command=self.Imprimir_a_excel)
        btnExpoExcel.grid(row=2, column=1, padx=10, pady=10)

    def obtenerDatosExportar(self):
        db = Consulta_Exportacion()
        ruta = Path(__file__).parent  # Buenas Practicas
        archivo = ruta / "whatislove.db"
        conexion = sqlite3.connect("{0}".format(archivo))

        if self.txtTablaImpre.get() == "Historial":
            dato = self.txtTablaImpre.get()
            consulta = db.Obtener_Datos_Exportar(dato)
            df = pd.read_sql_query(consulta, conexion)
            return df

        elif self.txtTablaImpre.get() == "Producto":
            dato = self.txtTablaImpre.get()
            consulta = db.Obtener_Datos_Exportar(dato)
            df = pd.read_sql_query(consulta, conexion)
            return df

    def Imprimir_a_excel(self):
        df = self.obtenerDatosExportar()

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])

        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Consulta Exitosa",
                                f"Tabla {self.txtTablaImpre.get()} exportada exitosamente")
            self.ventana_Registro_Excel.destroy()
#---------centrar ventanas--------
def Centrar_ventana(ventana, ancho, altura):
    ventana.update_idletasks()
    ventResolucionX = ventana.winfo_screenwidth()
    ventResolucionY = ventana.winfo_screenheight()
    centrar_X = int((ventResolucionX / 2) - (ancho / 2))
    centrar_Y = int((ventResolucionY / 2) - (altura / 2))
    ventana.geometry("{}x{}+{}+{}".format(ancho, altura, centrar_X, centrar_Y))
# --------Arranque------------
def main():
    global app
    app = Ventana()
    app.title('Back Pack')
    Centrar_ventana(app,300,500)
    tb.Style('litera')
    ruta2 = Path(__file__).parent  # Buenas Practicas
    archivo2 = ruta2 / "Logo.ico"
    app.iconbitmap(archivo2)
    app.mainloop()


if __name__ == '__main__':
    main()