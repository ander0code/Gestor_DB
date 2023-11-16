from tkinter import*
from tkinter import ttk,messagebox
import ttkbootstrap as tb
from datetime import datetime
from CRUD_PROVEDORES import Crud_Proveedor
from CRUD_PRODUCTOS import Crud_Productos
from CRUD_HISTORIAL import Crud_Historial
from LOGIN import Login
from CRUD_USUARIOS import Crud_Usuarios
#Impor libreria pa conectar BD
import sqlite3
from tkinter import simpledialog

class Ventana(tb.Window):
    def __init__(self):
        super().__init__()
        self.ventanaLogin()
        self.rol_usuario_actual = None
    def ventanaLogin(self):
        self.frame_login = Frame(self)
        self.frame_login.pack()

        self.lblframe_login = ttk.LabelFrame(self.frame_login, text='Acceso')
        self.lblframe_login.pack(padx=10, pady=10)

        lbltitulo = Label(self.lblframe_login, text='Inicio de sesión', font=('Arial', 18))
        lbltitulo.pack(padx=10, pady=35)

        self.txtUsuario = ttk.Entry(self.lblframe_login, width=40,bootstyle='secondary', justify=CENTER)
        self.txtUsuario.pack(padx=10, pady=10)
        self.set_placeholder(self.txtUsuario, "Usuario")

        self.txtClave = ttk.Entry(self.lblframe_login, width=40,bootstyle='secondary', justify=CENTER)
        self.txtClave.pack(padx=10, pady=10)
        self.txtClave.configure(show='*')
        self.set_placeholder(self.txtClave, "Contraseña")

        btnAcceso = ttk.Button(self.lblframe_login, text='Log in', command=self.logueo)
        btnAcceso.pack(padx=10, pady=10)
    # es para imitar el placeholder
    def set_placeholder(self, entry_widget, placeholder):
        entry_widget.insert(0, placeholder)
        entry_widget.bind("<FocusIn>", lambda event: self.on_entry_click(entry_widget, placeholder))
        entry_widget.bind("<FocusOut>", lambda event: self.on_focus_out(entry_widget, placeholder))
    def on_entry_click(self, entry_widget, placeholder):
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, END)
              # Cambiar el color del texto al escribir
    def on_focus_out(self, entry_widget, placeholder):
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder)
              # Restaurar el color del texto al placeholder
    def ventanaMenu(self):
        self.frameLeft=Frame(self,width=200)
        self.frameLeft.grid(row=0,column=0,sticky=NSEW)
        self.frameCenter=Frame(self)
        self.frameCenter.grid(row=0,column=1,sticky=NSEW)
        self.frameRight=Frame(self,width=400)
        self.frameRight.grid(row=0,column=2,sticky=NSEW)
        #-------------BOTONES-----
        btnProductos=ttk.Button(self.frameLeft, text='Productos', width=15,command=self.ventanaListaProductos)
        btnProductos.grid(row=0,column=0,padx=10,pady=10)


        btnClientes=ttk.Button(self.frameLeft, text='Proveedores',width=15,
                               command=lambda: self.ventanaListaUsuarios(mostrar_proveedores=True))
        btnClientes.grid(row=1,column=0,padx=10,pady=10)


        btnUsuarios=ttk.Button(self.frameLeft, text='Usuarios',width=15,
                               command=lambda: self.ventanaListaUsuarios(mostrar_proveedores=False))
        btnUsuarios.grid(row=2,column=0,padx=10,pady=10)

        btnReportes=ttk.Button(self.frameLeft, text='Reportes',width=15,command=self.mostrarHistorial)
        btnReportes.grid(row=3,column=0,padx=10,pady=10)
        
        btnRestaurar_DB=ttk.Button(self.frameLeft, text='Restaurar DB',width=15,command=self.subventanborrarTabla)
        btnRestaurar_DB.grid(row=4,column=0,padx=10,pady=10)
    def logueo(self):
        # Capturar errores
        try:
            # Establecer conexión
            db = Login()

            nombreUsuario = self.txtUsuario.get()
            claveUsuario = self.txtClave.get()
            # Traer todos los registros y guardar en "datos"
            datosLogueo = db.verificacion(nombreUsuario, claveUsuario)

            if datosLogueo:
                for row in datosLogueo:
                    codUsuario = row[0]
                    nomUsuario = row[1]
                    claUsuario = row[2]
                    rolUsuario = row[3]

                if nomUsuario == self.txtUsuario.get() and claUsuario == self.txtClave.get():
                    # Almacenar el rol del usuario actual en una variable de instancia
                    self.rol_usuario_actual = rolUsuario

                    # Ocultar ventana de login
                    self.frame_login.pack_forget()
                    # Abrir ventana de menú
                    self.ventanaMenu()
            else:
                messagebox.showerror("INICIO SECION","DATOS INCORRECTOS")

            # Aplicar Cambios

        except sqlite3.Error as e:
            # Mensaje de error por si acaso
            messagebox.showerror("Acceso", f"Ocurrió un error: {e}")

    #---------------USUARIOS------------
    def ventanaListaUsuarios(self, mostrar_proveedores= False):

        self.frameListaUsuarios=Frame(self.frameCenter)
        self.frameListaUsuarios.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframeBotonesListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeBotonesListUsu.grid(row=0,column=0,sticky=NSEW)

        self.lblframeBusqListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeBusqListUsu.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        self.txtBusquedaUsuarios=ttk.Entry(self.lblframeBusqListUsu,width=100)
        self.txtBusquedaUsuarios.grid(row=0,column=0,padx=5,pady=5)
        # Condicional para buscar Prove - Usua
        if mostrar_proveedores:
            self.txtBusquedaUsuarios.bind('<Key>', self.buscarProveedores)

        else:
            self.txtBusquedaUsuarios.bind('<Key>', self.buscarProductos)

        #====================TreeView===============
        self.lblframeTreeListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeTreeListUsu.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        columnas=("codigo", "nombre", "clave", "rol")

        self.TreelistUsuarios=tb.Treeview(self.lblframeTreeListUsu,columns=columnas,height=17,show='headings',bootstyle='secondary')
        self.TreelistUsuarios.grid(row=0,column=0)

        self.TreelistUsuarios.heading("codigo",text="Codigo",anchor=W)
        self.TreelistUsuarios.heading("nombre",text="Nombre",anchor=W)
        self.TreelistUsuarios.heading("clave",text="Clave",anchor=W)
        self.TreelistUsuarios.heading("rol",text="Rol",anchor=W)


        self.TreelistUsuarios['displaycolumns']=['codigo','nombre','rol']#Solo apareceran 3 pq la clave es secreta SAPAZO

        #Creando el rico scrollbar
        TreeScrollListUsu=tb.Scrollbar(self.frameListaUsuarios,bootstyle='round-success')
        TreeScrollListUsu.grid(row=2,column=1)
        #Configu el scroll
        TreeScrollListUsu.config(command=self.TreelistUsuarios.yview)

        #Condicionales para la seleccion de Botnoes Proveedor y Usuarios
        if mostrar_proveedores:
            btnNuevoUsuario = tb.Button(self.lblframeBotonesListUsu, text='Lista Productos', width=15,
                                        bootstyle="success", command=self.ventanaListaProductosProvedor)
            btnNuevoUsuario.grid(row=0, column=0, padx=5, pady=5)


            self.mostrar_proveedores()

        else:

            btnNuevoUsuario = tb.Button(self.lblframeBotonesListUsu, text='Nuevo', width=15, bootstyle="success",
                                        command=self.ventanaNuevoUsuario)
            btnNuevoUsuario.grid(row=0, column=0, padx=5, pady=5)

            btnModificarUsuario = tb.Button(self.lblframeBotonesListUsu, text='Modificar', width=15,
                                            bootstyle="warning", command=self.ventanaModificarUsuario)
            btnModificarUsuario.grid(row=0, column=1, padx=5, pady=5)

            btnEliminarUsuario = tb.Button(self.lblframeBotonesListUsu, text='Eliminar', width=15, bootstyle="danger",
                                           command=self.borrarUsuario)
            btnEliminarUsuario.grid(row=0, column=2, padx=5, pady=5)

            self.MostrarUsuarios()
    def MostrarUsuarios(self):
        #Capturar errores
        try:
            #Establecer conexión
            db = Crud_Usuarios()
            #Crear cursor
            # Consultar DB
            datos=db.Mostrar_Usuarios()
            #Limpiar data del treeview
            registros=self.TreelistUsuarios.get_children()
            #Recorrer registros
            for elementos in registros:
                self.TreelistUsuarios.delete(elementos)
            #Recorrer cada fila encontrada
            for row in datos:
                #Llenar treewbiew
                self.TreelistUsuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #Aplicar Cambios

        except sqlite3.Error as e:
            #Mensaje de error porsiaca
            print("Error de SQLite:", e)
            messagebox.showerror("Lista de Usuario", f"Ocurrió un error al mostrar la lista de usuario: {e}")
    def ventanaNuevoUsuario(self):
        self.frameNewUser=Toplevel(self)#Ventana por encima de la lista de usuarios
        self.frameNewUser.title('Nuevo Usuario')
        self.CentrarVentanaNuevoUser(400,300)#tamaño
        self.frameNewUser.resizable(0,0)#Para que no se maximice ni minimice
        self.frameNewUser.grab_set()#Para que no permita otra acción hasta que se cierre pues

        lblframeNewUser=LabelFrame(self.frameNewUser)
        lblframeNewUser.grid(row=0,column=0,sticky=NSEW,padx=25,pady=35)

        lblCodeModifyUser=Label(lblframeNewUser,text='Codigo')
        lblCodeModifyUser.grid(row=0,column=0,padx=10,pady=10,sticky=E)
        self.txtCodeNewUser=ttk.Entry(lblframeNewUser,width=40)
        self.txtCodeNewUser.grid(row=0,column=1,padx=10,pady=10)

        lblNameNewUser=Label(lblframeNewUser,text='Nombre')
        lblNameNewUser.grid(row=1,column=0,padx=10,pady=10,sticky=E)
        self.txtNameNewUser=ttk.Entry(lblframeNewUser,width=40)
        self.txtNameNewUser.grid(row=1,column=1,padx=10,pady=10)

        lblClaveNewUser=Label(lblframeNewUser,text='Clave')
        lblClaveNewUser.grid(row=2,column=0,padx=10,pady=10,sticky=E)
        self.txtClaveNewUser=ttk.Entry(lblframeNewUser,width=40)
        self.txtClaveNewUser.grid(row=2,column=1,padx=10,pady=10)

        lblRolNewUser=Label(lblframeNewUser,text='Rol')
        lblRolNewUser.grid(row=3,column=0,padx=10,pady=10,sticky=E)
        self.txtRolNewUser=ttk.Combobox(lblframeNewUser,values=('Administrador','Proveedor','Vendedor'),width=38,state='readonly')
        self.txtRolNewUser.grid(row=3,column=1,padx=10,pady=10)
        self.txtRolNewUser.current(0)

        btnSaveNewUser=ttk.Button(lblframeNewUser,text='Guardar',width=38,command=self.guardarUsuario)
        btnSaveNewUser.grid(row=4,column=1,padx=10,pady=10)
        
        self.registrar_en_historial("Usuario ha sido creado por: ", self.txtUsuario.get())

        #Llamamos a la funcion ultimo usuario
        self.ultimoUsuario()
        #Foco en el nombre usuario
        self.txtNameNewUser.focus()
    def guardarUsuario(self):
        #Validacion pa que no queden vacios los campos
        if self.txtCodeNewUser.get()=="" or self.txtNameNewUser.get()=="" or self.txtClaveNewUser.get()=="":
            messagebox.showwarning('Guardando usuarios', 'Algún campo no es válido, por favor revisar')
            return
        #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()

            datosGuardarUsuarios=self.txtCodeNewUser.get(),self.txtNameNewUser.get(),self.txtClaveNewUser.get(),self.txtRolNewUser.get()            #Consultar DB
            miCursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)",(datosGuardarUsuarios))
            #Traer todos los registros y guardar en "datos"
            messagebox.showinfo('Guardando Usuarios', "Usuario Guardado Correctamente")
            #Aplicar Cambios
            miConexion.commit()
            self.frameNewUser.destroy()#Cerrala ventana
            self.ventanaListaUsuarios()#Carga nuevamente la ventana pa ver los cambios
            #Cerrar la conexion
            miConexion.close()

        except:
            messagebox.showerror("Guardando Usuarios","Ocurrió un error al Guardar Usuario")
    def ultimoUsuario(self):
         #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()
            #Limpiar data del treeview

            miCursor.execute("SELECT MAX(Codigo) FROM Usuarios")
            #Traer todos los registros y guardar en "datos"
            datos=miCursor.fetchone()#Solo necesita un dato
            for codusu in datos:
                if codusu==None:
                    self.ultusu=(int(1))
                    self.txtCodeNewUser.config(state=NORMAL)
                    self.txtCodeNewUser.insert(0,self.ultusu)
                    self.txtCodeNewUser.config(state='readonly')
                    break

                if codusu=="":
                    self.ultusu=(int(1))
                    self.txtCodeNewUser.config(state=NORMAL)
                    self.txtCodeNewUser.insert(0,self.ultusu)
                    self.txtCodeNewUser.config(state='readonly')
                    break

                else:
                    self.ultusu=(int(codusu)+1)
                    self.txtCodeNewUser.config(state=NORMAL)
                    self.txtCodeNewUser.insert(0,self.ultusu)
                    self.txtCodeNewUser.config(state='readonly')


            #Aplicar Cambios
            miConexion.commit()
            #Cerrar la conexion
            miConexion.close()

        except:
            #Mensaje de error porsiaca
            print("Ocurrió un error")
    def CentrarVentanaNuevoUser(self,ancho,alto):
        ventanaAncho=ancho
        ventanaAlto=alto
        pantallaAncho=self.frameRight.winfo_screenwidth()
        pantallaAlto=self.frameRight.winfo_screenheight()
        coordenadasX=int((pantallaAncho/2)-(ventanaAlto/2))
        coordenadasY=int((pantallaAlto/2)-(ventanaAlto/2))
        self.frameNewUser.geometry("{}x{}+{}+{}".format(ventanaAncho,ventanaAlto,coordenadasX,coordenadasY))
    def buscarProducztos(self,event):
        #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()
            #Limpiar data del treeview
            registros=self.TreelistUsuarios.get_children()
            #Recorrer registros
            for elementos in registros:
                self.TreelistUsuarios.delete(elementos)
            #Consultar DB
            miCursor.execute("SELECT * FROM Usuarios WHERE Nombre LIKE ?", (self.txtBusquedaUsuarios.get()+'%',))
            #Traer todos los registros y guardar en "datos"
            datos=miCursor.fetchall()
            #Recorrer cada fila encontrada
            for row in datos:
                #Llenar treewbiew
                self.TreelistUsuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #Aplicar Cambios
            miConexion.commit()
            #Cerrar la conexion
            miConexion.close()

        except:
            #Mensaje de error porsiaca
            print("Busqueda de usuarios","Ocurrió un error al buscar en la lista de usuarios")
    def ventanaModificarUsuario(self):
        #Aca se valida que se abra la ventana solamente si hay algun valor seleccionado
        self.usuarioSeleccionado=self.TreelistUsuarios.focus()
        self.ValModUsu=self.TreelistUsuarios.item(self.usuarioSeleccionado,'values')

        if self.ValModUsu!='':
            self.frameModifyUser=Toplevel(self)#Ventana por encima de la lista de usuarios
            self.frameModifyUser.title('Nuevo Usuario')
            self.frameModifyUser.geometry('400x300')
            #self.CentrarVentanaModificarUser(400,300)#tamaño
            self.frameModifyUser.resizable(0,0)#Para que no se maximice ni minimice
            self.frameModifyUser.grab_set()#Para que no permita otra acción hasta que se cierre pues

            lblModifyUser=LabelFrame(self.frameModifyUser)
            lblModifyUser.grid(row=0,column=0,sticky=NSEW,padx=25,pady=35)

            lblCodeModifyUser=Label(lblModifyUser,text='Codigo')
            lblCodeModifyUser.grid(row=0,column=0,padx=10,pady=10,sticky=E)
            self.txtCodeModifyUser=ttk.Entry(lblModifyUser,width=40)
            self.txtCodeModifyUser.grid(row=0,column=1,padx=10,pady=10)

            lblModifyNewUser=Label(lblModifyUser,text='Nombre')
            lblModifyNewUser.grid(row=1,column=0,padx=10,pady=10,sticky=E)
            self.txtNameModifyUser=ttk.Entry(lblModifyUser,width=40)
            self.txtNameModifyUser.grid(row=1,column=1,padx=10,pady=10)

            lblClaveModifyUser=Label(lblModifyUser,text='Clave')
            lblClaveModifyUser.grid(row=2,column=0,padx=10,pady=10,sticky=E)
            self.txtClaveModifyUser=ttk.Entry(lblModifyUser,width=40)
            self.txtClaveModifyUser.grid(row=2,column=1,padx=10,pady=10)

            lblRolModifyUser=Label(lblModifyUser,text='Rol')
            lblRolModifyUser.grid(row=3,column=0,padx=10,pady=10,sticky=E)
            self.txtRolModifyUser=ttk.Combobox(lblModifyUser,values=('Administrador','Proveedor','Vendedor'),width=38)
            self.txtRolModifyUser.grid(row=3,column=1,padx=10,pady=10)


            btnSaveModifyUser=ttk.Button(lblModifyUser,text='Modificar',width=38,bootstyle='warning', command=self.modificarUsuario)
            btnSaveModifyUser.grid(row=4,column=1,padx=10,pady=10)
            self.llenarEntrysPaModificarUser()
            #Foco en el nombre usuario
            self.txtNameModifyUser.focus()
    def llenarEntrysPaModificarUser(self):
        #Limpiar los entrys
        self.txtCodeModifyUser.delete(0,END)
        self.txtNameModifyUser.delete(0,END)
        self.txtClaveModifyUser.delete(0,END)
        self.txtRolModifyUser.delete(0,END)
        #Llenar los entrys
        self.txtCodeModifyUser.insert(0,self.ValModUsu[0])
        self.txtCodeModifyUser.config(state='readonly')
        self.txtNameModifyUser.insert(0,self.ValModUsu[1])
        self.txtClaveModifyUser.insert(0,self.ValModUsu[2])
        self.txtRolModifyUser.insert(0,self.ValModUsu[3])
        self.txtRolModifyUser.config(state='readonly')
    def modificarUsuario(self):
        #Validacion pa que no queden vacios los campos
        if self.txtCodeModifyUser.get()=="" or self.txtNameModifyUser.get()=="" or self.txtClaveModifyUser.get()=="":
            messagebox.showwarning('Modificando usuarios', 'Algún campo no es válido, por favor revisar')
            return
        #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()

            datosModificarUsuarios=self.txtNameModifyUser.get(),self.txtClaveModifyUser.get(),self.txtRolModifyUser.get()            #Consultar DB
            miCursor.execute("UPDATE Usuarios SET Nombre=?,Clave=?,Rol=? WHERE Codigo="+self.txtCodeModifyUser.get(),(datosModificarUsuarios))
            #Traer todos los registros y guardar en "datos"
            messagebox.showinfo('Modificar Usuarios', "Usuario Modificado Correctamente")
            #Aplicar Cambios
            miConexion.commit()
            self.ValModUsu=self.TreelistUsuarios.item(self.usuarioSeleccionado,text='',values=(self.txtCodeModifyUser.get(),self.txtNameModifyUser.get(),self.txtClaveModifyUser.get(),self.txtRolModifyUser.get(),))
            self.registrar_en_historial(f"{self.txtNameModifyUser.get()} ha sido modificado por: ", self.txtUsuario.get())
            self.frameModifyUser.destroy()#Cerrala ventana
            self.ventanaListaUsuarios()#Carga nuevamente la ventana pa ver los cambios
            #Cerrar la conexion
            miConexion.close()

        except:
            messagebox.showerror("Modificar Usuarios","Ocurrió un error al Modificar Usuario")
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
        contraseña_confirmacion = simpledialog.askstring('Confirmar Eliminación', f'Ingrese la contraseña para confirmar la eliminación del usuario {nombre_usuario}:', show='*')

        if not contraseña_confirmacion:
            return  # El usuario cerró la ventana de confirmación o no ingresó contraseña

        try:
            # Establecer conexión
            miConexion = sqlite3.connect('whatislove.db')
            # Crear cursor
            miCursor = miConexion.cursor()

            # Consultar DB y verificar la contraseña
            miCursor.execute("SELECT Clave FROM Usuarios WHERE Codigo=?", (codigo_usuario,))
            resultado = miCursor.fetchone()

            if resultado and resultado[0] == contraseña_confirmacion:
                # Eliminar el usuario
                miCursor.execute("DELETE FROM Usuarios WHERE Codigo=?", (codigo_usuario,))
                # Aplicar Cambios
                miConexion.commit()
                messagebox.showinfo('Borrar Usuario', "Usuario Borrado Correctamente")
                # Cerrar la conexion
                miConexion.close()
                self.registrar_en_historial("Un usuario ha borrado por: ", self.txtUsuario.get())
                # Actualizar la lista de usuarios después de borrar
                self.ventanaListaUsuarios()
            else:
                messagebox.showerror('Error', 'Contraseña incorrecta')

        except sqlite3.Error as e:
            messagebox.showerror("Borrar Usuario", "Ocurrió un error al borrar el usuario: {}".format(e))

        finally:
            miConexion.close()
    def es_administrador_actual(self):
        # Verificar si el rol almacenado es "Administrador"
        return self.rol_usuario_actual == 'Administrador'


    # ---------------Proveedor------------
    def ventanaListaProductosProvedor(self):
        self.frameListaProductos = Toplevel(self)
        self.frameListaProductos.title('Lista de Productos')
        self.frameListaProductos.resizable(0, 0)


        self.frameListaProductos.geometry("1250x340+325+325")

        self.frameListaProductos.grab_set()
        self.lblframeBotonesListProd = LabelFrame(self.frameListaProductos)
        self.lblframeBotonesListProd.grid(row=0, column=0, sticky=NSEW)

        self.lblframeTreeListProd = LabelFrame(self.frameListaProductos)
        self.lblframeTreeListProd.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("ID Producto", "Nombre_proveedor", "Nombre del Producto", "Precio", "Stock", "Descripción")
        self.TreelistProductosPro = tb.Treeview(self.lblframeTreeListProd, columns=columnas, height=17, show='headings',
                                            bootstyle='secondary')
        self.TreelistProductosPro.grid(row=0, column=0)
        self.TreelistProductosPro.heading("ID Producto", text="ID Producto", anchor=W)
        self.TreelistProductosPro.heading("Nombre_proveedor", text="Nombre_proveedor", anchor=W)
        self.TreelistProductosPro.heading("Nombre del Producto", text="Nombre del Producto", anchor=W)
        self.TreelistProductosPro.heading("Precio", text="Precio", anchor=W)
        self.TreelistProductosPro.heading("Stock", text="Stock", anchor=W)
        self.TreelistProductosPro.heading("Descripción", text="Descripción", anchor=W)

        self.TreelistProductosPro['displaycolumns'] = ['ID Producto', 'Nombre_proveedor', 'Nombre del Producto',
                                                    'Precio', 'Stock', 'Descripción']
        # Creando el scrollbar
        TreeScrollListProd = tb.Scrollbar(self.frameListaProductos, bootstyle='round-success')
        TreeScrollListProd.grid(row=2, column=1)
        TreeScrollListProd.config(command=self.TreelistProductosPro.yview)
        self.MostrarProductosProveedor()
    def mostrar_proveedores(self):

        crud = Crud_Proveedor()
        datos = crud.mostrar_proveedores()
        registros = self.TreelistUsuarios.get_children()
        for elementos in registros:
            self.TreelistUsuarios.delete(elementos)

        for row in datos:
            self.TreelistUsuarios.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))
    def MostrarProductosProveedor(self):
        proveedor_seleccionado = self.TreelistUsuarios.focus()
        proveedor_codigo = self.TreelistUsuarios.item(proveedor_seleccionado, 'text')
        crud = Crud_Proveedor()
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
        crud = Crud_Proveedor()
        proveedores = crud.buscar_proveedores(nombre_proveedor)
        for proveedor in proveedores:
            # Llenar treewbiew
            self.TreelistUsuarios.insert("", 0, text=proveedor[0],
                                         values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3]))


    #----------Productos-----------
    def ventanaListaProductos(self):

        self.frameListaProducto=Frame(self.frameCenter)
        self.frameListaProducto.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframeBotonesListProduc=LabelFrame(self.frameListaProducto)
        self.lblframeBotonesListProduc.grid(row=0,column=0,sticky=NSEW)

        btnNuevoProduct=tb.Button(self.lblframeBotonesListProduc,text='Nuevo', width=15,bootstyle="success",command=self.ventanaNuevoProducto)
        btnNuevoProduct.grid(row=0,column=0,padx=5,pady=5)

        btnModificarProduc=tb.Button(self.lblframeBotonesListProduc,text='Modificar', width=15,bootstyle="warning", command=self.ventanaModificarProductos)
        btnModificarProduc.grid(row=0,column=1,padx=5,pady=5)

        btnEliminarProduc=tb.Button(self.lblframeBotonesListProduc,text='Eliminar', width=15,bootstyle="danger",command=self.borrarProducto)
        btnEliminarProduc.grid(row=0,column=2,padx=5,pady=5)

        self.lblframeBusqListProduct=LabelFrame(self.frameListaProducto)
        self.lblframeBusqListProduct.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        self.txtBusquedaProducts=ttk.Entry(self.lblframeBusqListProduct,width=100)
        self.txtBusquedaProducts.grid(row=0,column=0,padx=5,pady=5)
        self.txtBusquedaProducts.bind('<Key>',self.buscarProductos)

        #====================TreeView===============
        self.lblframeTreeListProduct=LabelFrame(self.frameListaProducto)
        self.lblframeTreeListProduct.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        columnas=("id_Producto","provedor", "producto", "precio", "stock","descripcion")

        self.TreelistProductosProductos=tb.Treeview(self.lblframeTreeListProduct,columns=columnas,height=17,show='headings',bootstyle='info')
        self.TreelistProductosProductos.grid(row=0,column=0)

        self.TreelistProductosProductos.heading("id_Producto",text="id_Producto",anchor=W)
        self.TreelistProductosProductos.heading("provedor",text="provedor",anchor=W)
        self.TreelistProductosProductos.heading("producto",text="producto",anchor=W)
        self.TreelistProductosProductos.heading("precio",text="precio",anchor=W)
        self.TreelistProductosProductos.heading("stock", text="stock", anchor=W)
        self.TreelistProductosProductos.heading("descripcion", text="descripcion", anchor=W)

        self.TreelistProductosProductos['displaycolumns']=['id_Producto','provedor','producto','precio','stock','descripcion']#Solo apareceran 3 pq la clave es secreta SAPAZO

        #Creando el rico scrollbar
        TreeScrollListProduct=tb.Scrollbar(self.frameListaProducto,bootstyle='round-success')
        TreeScrollListProduct.grid(row=2,column=1)
        #Configu el scroll
        TreeScrollListProduct.config(command=self.TreelistProductosProductos.yview)

        #Llamar a func mostrar usuarios
        self.MostrarProductos()
    def MostrarProductos(self):
        #Capturar errores
        try:
            Crud = Crud_Productos()
            datos = Crud.mostrar_productos()

            #Limpiar data del treeview
            registros=self.TreelistProductosProductos.get_children()
            #Recorrer registros
            for elementos in registros:
                self.TreelistProductosProductos.delete(elementos)
            #Traer todos los registros y guardar en "datos"
            #Recorrer cada fila encontrada
            for row in datos:
                self.TreelistProductosProductos.insert("","end",text=row[0],values=(row[0],row[1],row[2],row[3],row[4],row[5]))

        except sqlite3.Error as e:
            #Mensaje de error porsiaca
            print("Error de SQLite:", e)
            messagebox.showerror("Lista de Usuario", f"Ocurrió un error al mostrar la lista de usuario: {e}")
    def ventanaNuevoProducto(self):
        self.frameNewProduct=Toplevel(self)#Ventana por encima de la lista de usuarios
        self.frameNewProduct.title('Nuevo Producto')
        self.frameNewProduct.geometry("410x380+700+320")#tamaño
        self.frameNewProduct.resizable(False,False)#Para que no se maximice ni minimice
        self.frameNewProduct.grab_set()#Para que no permita otra acción hasta que se cierre pues

        lblframeNewProduc=LabelFrame(self.frameNewProduct)
        lblframeNewProduc.grid(row=0,column=0,sticky=NSEW,padx=25,pady=35)

        lblCodeModifyProduct=Label(lblframeNewProduc,text='Id_provedor')
        lblCodeModifyProduct.grid(row=0,column=0,padx=10,pady=10,sticky=E)
        selecionProveedor = StringVar()
        self.txtCodeNewProduc=ttk.Entry(lblframeNewProduc,width=40)
        self.txtCodeNewProduc.grid(row=0,column=1,padx=10,pady=10)

        lblNameNewProduct=Label(lblframeNewProduc,text='Producto')
        lblNameNewProduct.grid(row=1,column=0,padx=10,pady=10,sticky=E)
        self.txtNameNewProduct=ttk.Entry(lblframeNewProduc,width=40)
        self.txtNameNewProduct.grid(row=1,column=1,padx=10,pady=10)

        lblPrecioNewProduct=Label(lblframeNewProduc,text='precio')
        lblPrecioNewProduct.grid(row=2,column=0,padx=10,pady=10,sticky=E)
        self.txtPrecioNewProduct=ttk.Entry(lblframeNewProduc,width=40)
        self.txtPrecioNewProduct.grid(row=2,column=1,padx=10,pady=10)

        lblStockNewProduct=Label(lblframeNewProduc,text='stock')
        lblStockNewProduct.grid(row=3,column=0,padx=10,pady=10,sticky=E)
        self.txtStockNewProduct = ttk.Entry(lblframeNewProduc, width=40)
        self.txtStockNewProduct.grid(row=3, column=1, padx=10, pady=10)

        lblDescripcionNewProduct = Label(lblframeNewProduc, text='Descripcion')
        lblDescripcionNewProduct.grid(row=4, column=0, padx=10, pady=10, sticky=E)
        self.txtDescripcionNewProduct = ttk.Entry(lblframeNewProduc, width=40)
        self.txtDescripcionNewProduct.grid(row=4, column=1, padx=10, pady=10)



        btnSaveNewProduct=ttk.Button(lblframeNewProduc,text='Guardar',width=38,command=self.guardarProducto)
        btnSaveNewProduct.grid(row=5,column=1,padx=10,pady=10)
        
        #Foco en el nombre usuario
        self.txtNameNewProduct.focus()


    def guardarProducto(self):
        #Validacion pa que no queden vacios los campos
        if (self.txtCodeNewProduc.get()==""
                or self.txtNameNewProduct.get()==""
                or self.txtPrecioNewProduct.get()==""
                or self.txtStockNewProduct.get()==""
                or self.txtDescripcionNewProduct.get()==""):
            messagebox.showwarning('Guardando Producto', 'Algún campo no es válido, por favor revisar')
            return
        #Capturar errores
        try:
            #Establecer conexión
            Crud = Crud_Productos()
            Crud.Guardar_Producto(self.txtCodeNewProduc.get(),self.txtNameNewProduct.get(),
                                   self.txtPrecioNewProduct.get(),self.txtStockNewProduct.get(),
                                   self.txtDescripcionNewProduct.get()
                                   )
            #Traer todos los registros y guardar en "datos"
            messagebox.showinfo('Guardando Producto', "Usuario Guardado Correctamente")
            self.frameNewProduct.destroy()#Cerrala ventana
            self.registrar_en_historial(f"Un Producto a sido agregago por : ",
                                        self.txtUsuario.get())
            self.ventanaListaProductos()#Carga nuevamente la ventana pa ver los cambios
            #Cerrar la conexion
        except sqlite3.Error as e:
            print("Error de SQLite:", e)
            messagebox.showerror("Guardando Productos", f"Ocurrió un error al Guardar Productos: {e}")
    def buscarProductos(self,event):
        #Capturar errores
        try:
            Crud = Crud_Productos()
            #Limpiar data del treeview
            registros=self.TreelistProductosProductos.get_children()
            #Recorrer registros
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
                self.TreelistProductosProductos.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        except sqlite3.Error as e:
            # Mensaje de error porsiaca
            print("Busqueda de productos", f"Ocurrió un error al buscar en la lista de productos: {e}")
    def ventanaModificarProductos(self):
        #Aca se valida que se abra la ventana solamente si hay algun valor seleccionado
        self.ProductoSeleccionado=self.TreelistProductosProductos.focus()
        self.ValModPro=self.TreelistProductosProductos.item(self.ProductoSeleccionado,'values')

        if self.ValModPro!='':
            self.frameModifyProduc=Toplevel(self)#Ventana por encima de la lista de usuarios
            self.frameModifyProduc.title('Nuevo Usuario')
            self.frameModifyProduc.geometry('500x430+700+320')
            #self.CentrarVentanaModificarUser(400,300)#tamaño
            self.frameModifyProduc.resizable(0,0)#Para que no se maximice ni minimice
            self.frameModifyProduc.grab_set()#Para que no permita otra acción hasta que se cierre pues

            lblModifyProduct=LabelFrame(self.frameModifyProduc)
            lblModifyProduct.grid(row=0,column=0,sticky=NSEW,padx=25,pady=35)
            
            lblCodeProducModifyProduct=Label(lblModifyProduct,text='Codigo del producto')
            lblCodeProducModifyProduct.grid(row=0,column=0,padx=10,pady=10,sticky=E)
            self.txtCodeProductoModifyProduct=ttk.Entry(lblModifyProduct,width=40)
            self.txtCodeProductoModifyProduct.grid(row=0,column=1,padx=10,pady=10)

            lblCodeModifyProduct=Label(lblModifyProduct,text='Nuevo Codigo de provedor')
            lblCodeModifyProduct.grid(row=1,column=0,padx=10,pady=10,sticky=E)
            self.txtCodeProveModifyProduct=ttk.Entry(lblModifyProduct,width=40)
            self.txtCodeProveModifyProduct.grid(row=1,column=1,padx=10,pady=10)

            lblModifyNewProduct=Label(lblModifyProduct,text='Nuevo Nombre')
            lblModifyNewProduct.grid(row=2,column=0,padx=10,pady=10,sticky=E)
            self.txtNewNameModifyProduct=ttk.Entry(lblModifyProduct,width=40)
            self.txtNewNameModifyProduct.grid(row=2,column=1,padx=10,pady=10)

            lblClaveModifyProdut=Label(lblModifyProduct,text='Nuevo Precio')
            lblClaveModifyProdut.grid(row=3,column=0,padx=10,pady=10,sticky=E)
            self.txtPrecioModifyProduct=ttk.Entry(lblModifyProduct,width=40)
            self.txtPrecioModifyProduct.grid(row=3,column=1,padx=10,pady=10)

            lblStockModifyProduct=Label(lblModifyProduct,text='Nuevo Stock')
            lblStockModifyProduct.grid(row=4,column=0,padx=10,pady=10,sticky=E)
            self.txtStockModifyProduct=ttk.Entry(lblModifyProduct,width=40)
            self.txtStockModifyProduct.grid(row=4,column=1,padx=10,pady=10)
            
            lblDescripcionModifyProduct=Label(lblModifyProduct,text='Nuevo Descripcion')
            lblDescripcionModifyProduct.grid(row=5,column=0,padx=10,pady=10,sticky=E)
            self.txtDescripModifyProduct=ttk.Entry(lblModifyProduct,width=40)
            self.txtDescripModifyProduct.grid(row=5,column=1,padx=10,pady=10)
            


            btnSaveModifyUser=ttk.Button(lblModifyProduct,text='Modificar',width=38,bootstyle='warning', command=self.modificarProducto)
            btnSaveModifyUser.grid(row=7,column=1,padx=10,pady=10)
            self.llenarEntrysPaModificarProducts()
            #Foco en el nombre usuario
            self.txtNewNameModifyProduct.focus()
    def llenarEntrysPaModificarProducts(self):
        #Limpiar los entrys
        self.txtCodeProductoModifyProduct.delete(0,END)
        self.txtCodeProveModifyProduct.delete(0,END)
        self.txtNewNameModifyProduct.delete(0,END)
        self.txtPrecioModifyProduct.delete(0,END)
        self.txtStockModifyProduct.delete(0,END)
        self.txtDescripModifyProduct.delete(0,END)
        #Llenar los entrys
        self.txtCodeProductoModifyProduct.insert(0,self.ValModPro[0])
        self.txtCodeProductoModifyProduct.config(state='readonly')
        self.txtCodeProveModifyProduct.insert(0,self.ValModPro[1])
        self.txtNewNameModifyProduct.insert(0,self.ValModPro[2])
        self.txtPrecioModifyProduct.insert(0,self.ValModPro[3])
        self.txtStockModifyProduct.insert(0,self.ValModPro[4])
        self.txtDescripModifyProduct.insert(0,self.ValModPro[5])
    def modificarProducto(self):
        #Validacion pa que no queden vacios los campos
        if (self.txtCodeProductoModifyProduct.get()=="" 
            or self.txtCodeProveModifyProduct.get()=="" 
            or self.txtNewNameModifyProduct.get()=="" 
            or self.txtPrecioModifyProduct.get()=="" 
            or self.txtStockModifyProduct.get()=="" 
            or self.txtDescripModifyProduct.get() == ""):
            messagebox.showwarning('Modificando usuarios', 'Algún campo no es válido, por favor revisar')
            return 
        #Capturar errores
        try:
            #Establecer conexión
            Crud = Crud_Productos()

            datosModificarUsuarios=(
            self.txtCodeProveModifyProduct.get(),
            self.txtNewNameModifyProduct.get(),
            self.txtPrecioModifyProduct.get(),
            self.txtStockModifyProduct.get(),
            self.txtDescripModifyProduct.get()) 
            #Consultar DB
            Crud.Modificar_Producto(self.txtCodeProductoModifyProduct.get(),datosModificarUsuarios)
            messagebox.showinfo('Modificar Usuarios', "Usuario Modificado Correctamente")
            #Aplicar Cambios
            self.ValModPro=self.TreelistProductosProductos.item(
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
            self.frameModifyProduc.destroy()#Cerrala ventana
            self.ventanaListaProductos()#Carga nuevamente la ventana pa ver los cambios
            #Cerrar la conexion


        except sqlite3.Error as e:
            print("Error de SQLite:", e)
            messagebox.showerror("Modificar Usuarios", f"Ocurrió un error al Modificar Usuario: {e}")
    def borrarProducto(self):
        # Obtén el producto seleccionado
        producto_seleccionado = self.TreelistProductosProductos.focus()
        valores_producto = self.TreelistProductosProductos.item(producto_seleccionado, 'values')

        if not valores_producto:
            messagebox.showwarning('Borrar Producto', 'Selecciona un producto para borrar.')
            return

        # Obtén el ID del producto seleccionado
        id_producto = valores_producto[0]

        # Capturar errores
        try:
            # Establecer conexión
            db = Crud_Productos()
            #borramos el producto
            db.Borrar_Producto(id_producto)
            # Actualizar la vista de productos
            self.ventanaListaProductos()
            messagebox.showinfo('Borrar Producto', 'Producto borrado correctamente.')
            self.registrar_en_historial("Un Producto ha sido borrado por: ", self.txtUsuario.get())
        except ValueError as e:
            messagebox.showerror('Borrar Producto', f'Ocurrió un error al borrar el producto: {e}')
        
        
        
    #----------Historial------------
    def mostrarHistorial(self):
    # Limpiar contenido del frame actual
        for widget in self.frameCenter.winfo_children():
            widget.destroy()

        # Crear el Treeview en el mismo frame
        self.TreelistHistorial = ttk.Treeview(self.frameCenter, columns=("id","fecha_hora", "accion", "usuario"), height=17, show='headings',bootstyle='danger')
        self.TreelistHistorial.grid(row=0, column=0)

        self.TreelistHistorial.heading("id", text="ID", anchor=W)
        self.TreelistHistorial.heading("accion", text="Acción", anchor=W)
        self.TreelistHistorial.heading("fecha_hora", text="Fecha y Hora", anchor=W)
        self.TreelistHistorial.heading("usuario", text="Usuario", anchor=W)

        # Obtener datos del historial desde la base de datos y cargar en el Treeview
        self.cargarHistorial()
    def cargarHistorial(self):
        try:
            db = Crud_Historial()

            datosHistorial = db.Cargar_Historial()

            for row in datosHistorial:
                self.TreelistHistorial.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Cargar Historial", f"Error al cargar el historial: {e}")

    def registrar_en_historial(self, accion, usuario):
        try:
            db = Crud_Historial()
            # Obtener la fecha y hora actual
            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insertar en la tabla de historial
            db.Registro_Historial(fecha_hora_actual, accion,usuario)


        except sqlite3.Error as e:
            messagebox.showerror("Registro en Historial", f"Error al registrar en el historial: {e}")

    #borrar tablas
    def subventanborrarTabla(self):
        self.frameborrarTabla = Toplevel(self)
        self.frameborrarTabla.title('Borrar Tabla')
        self.frameborrarTabla.geometry("135x100+900+400")
        self.frameborrarTabla.grab_set()
        btnborrarHistorial = ttk.Button(self.frameborrarTabla, text='Borrar Historial', width=15,
                                        command=self.borrar_tabla_historial)
        btnborrarHistorial.grid(row=0, column=0, padx=10, pady=10)

        btnborraProduc = ttk.Button(self.frameborrarTabla, text='Borrar Producto', width=15,
                                    command=self.borrar_tabla_producto)
        btnborraProduc.grid(row=1, column=0, padx=10, pady=10)

    def borrar_tabla_historial(self):
        borra = Crud_Historial()
        borra.borrar_tabla()
        messagebox.showinfo("Borrar Tabla Historial", "Tabla exitosamente Borrada")

    def borrar_tabla_producto(self):
        borra = Crud_Productos()
        borra.borrar_tabla()
        messagebox.showinfo("Borrar Tabla Producto", "Tabla exitosamente Borrada")

def main():
    app=Ventana()
    app.title('Sistema de Ventas')
    app.state('zoomed')
    tb.Style('darkly')
    app.mainloop()

if __name__=='__main__':
    main()