from tkinter import*
from tkinter import ttk,messagebox
import ttkbootstrap as tb
#Impor libreria pa conectar BD
import sqlite3
from tkinter import simpledialog


class Ventana(tb.Window):
    def __init__(self):
        super().__init__()
        self.ventanaLogin()
        self.rol_usuario_actual = None
    def ventanaLogin(self):
        self.frame_login=Frame(self)
        self.frame_login.pack()

        self.lblframe_login=LabelFrame(self.frame_login,text='Acceso')
        self.lblframe_login.pack(padx=10,pady=10)

        lbltitulo=Label(self.lblframe_login,text='Inicio de sesión', font=('Arial',18))
        lbltitulo.pack(padx=10,pady=35)

        self.txtUsuario=ttk.Entry(self.lblframe_login,width=40,justify=CENTER)
        self.txtUsuario.pack(padx=10,pady=10)
        self.txtClave=ttk.Entry(self.lblframe_login, width=40,justify=CENTER)
        self.txtClave.pack(padx=10,pady=10)
        self.txtClave.configure(show='*')

        btnAcceso=ttk.Button(self.lblframe_login, text='Log in',command=self.logueo)
        btnAcceso.pack(padx=10,pady=10)
    def ventanaMenu(self):
        self.frameLeft=Frame(self,width=200)
        self.frameLeft.grid(row=0,column=0,sticky=NSEW)
        self.frameCenter=Frame(self)
        self.frameCenter.grid(row=0,column=1,sticky=NSEW)
        self.frameRight=Frame(self,width=400)
        self.frameRight.grid(row=0,column=2,sticky=NSEW)
        #-------------BOTONES-----
        btnProductos=ttk.Button(self.frameLeft, text='Productos', width=15)
        btnProductos.grid(row=0,column=0,padx=10,pady=10)

        btnVentas=ttk.Button(self.frameLeft, text='Ventas',width=15)
        btnVentas.grid(row=1,column=0,padx=10,pady=10)

        btnClientes=ttk.Button(self.frameLeft, text='Proveedores',width=15)
        btnClientes.grid(row=2,column=0,padx=10,pady=10)

        btnCompras=ttk.Button(self.frameLeft, text='Compras',width=15)
        btnCompras.grid(row=3,column=0,padx=10,pady=10)

        btnUsuarios=ttk.Button(self.frameLeft, text='Usuarios',width=15,command=self.ventanaListaUsuarios)
        btnUsuarios.grid(row=4,column=0,padx=10,pady=10)

        btnReportes=ttk.Button(self.frameLeft, text='Reportes',width=15)
        btnReportes.grid(row=5,column=0,padx=10,pady=10)

        btnBackup=ttk.Button(self.frameLeft, text='Backup',width=15)
        btnBackup.grid(row=6,column=0,padx=10,pady=10)

        btnRestauraDB=ttk.Button(self.frameLeft, text='Restaurar DB',width=15)
        btnRestauraDB.grid(row=7,column=0,padx=10,pady=10)

        btnRestauraDB=ttk.Button(self.frameCenter, text='Restaurar DB')
        btnRestauraDB.grid(row=2,column=0,padx=10,pady=10)

        btnRestauraDB=ttk.Button(self.frameRight, text='Restaurar DB')
        btnRestauraDB.grid(row=3,column=0,padx=10,pady=10)
    def logueo(self):
        # Capturar errores
        try:
            # Establecer conexión
            miConexion = sqlite3.connect('./PuntoVent/whatislove.db')
            # Crear cursor
            miCursor = miConexion.cursor()

            nombreUsuario = self.txtUsuario.get()
            claveUsuario = self.txtClave.get()

            miCursor.execute("SELECT * FROM Usuarios WHERE Nombre=? AND Clave=?", (nombreUsuario, claveUsuario))
            # Traer todos los registros y guardar en "datos"
            datosLogueo = miCursor.fetchall()
            
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

            # Aplicar Cambios
            miConexion.commit()

        except sqlite3.Error as e:
            # Mensaje de error por si acaso
            messagebox.showerror("Acceso", f"Ocurrió un error: {e}")

        finally:
            # Cerrar la conexión
            miConexion.close()
    #---------------USUARIOS------------
    def ventanaListaUsuarios(self):

        self.frameListaUsuarios=Frame(self.frameCenter)
        self.frameListaUsuarios.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframeBotonesListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeBotonesListUsu.grid(row=0,column=0,sticky=NSEW)

        btnNuevoUsuario=tb.Button(self.lblframeBotonesListUsu,text='Nuevo', width=15,bootstyle="success",command=self.ventanaNuevoUsuario)
        btnNuevoUsuario.grid(row=0,column=0,padx=5,pady=5)

        btnModificarUsuario=tb.Button(self.lblframeBotonesListUsu,text='Modificar', width=15,bootstyle="warning", command=self.ventanaModificarUsuario)
        btnModificarUsuario.grid(row=0,column=1,padx=5,pady=5)

        btnEliminarUsuario=tb.Button(self.lblframeBotonesListUsu,text='Eliminar', width=15,bootstyle="danger",command=self.borrarUsuario)
        btnEliminarUsuario.grid(row=0,column=2,padx=5,pady=5)

        self.lblframeBusqListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeBusqListUsu.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        self.txtBusquedaUsuarios=ttk.Entry(self.lblframeBusqListUsu,width=100)
        self.txtBusquedaUsuarios.grid(row=0,column=0,padx=5,pady=5)
        self.txtBusquedaUsuarios.bind('<Key>',self.buscarUsuarios)

        #====================TreeView===============
        self.lblframeTreeListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeTreeListUsu.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        columnas=("codigo", "nombre", "clave", "rol")

        self.TreelistUsuarios=tb.Treeview(self.lblframeTreeListUsu,columns=columnas,height=17,show='headings',bootstyle='dark')
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

        #Llamar a func mostrar usuarios
        self.MostrarUsuarios()
    def MostrarUsuarios(self):
        #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('./PuntoVent/whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()
            #Limpiar data del treeview
            registros=self.TreelistUsuarios.get_children()
            #Recorrer registros
            for elementos in registros:
                self.TreelistUsuarios.delete(elementos)
            #Consultar DB
            miCursor.execute("SELECT * FROM Usuarios")
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
            miConexion=sqlite3.connect('./PuntoVent/whatislove.db')
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
            miConexion=sqlite3.connect('./PuntoVent/whatislove.db')
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
    def buscarUsuarios(self,event):
        #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('./PuntoVent/whatislove.db')
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
            miConexion=sqlite3.connect('./PuntoVent/whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()

            datosModificarUsuarios=self.txtNameModifyUser.get(),self.txtClaveModifyUser.get(),self.txtRolModifyUser.get()            #Consultar DB
            miCursor.execute("UPDATE Usuarios SET Nombre=?,Clave=?,Rol=? WHERE Codigo="+self.txtCodeModifyUser.get(),(datosModificarUsuarios))
            #Traer todos los registros y guardar en "datos"
            messagebox.showinfo('Modificar Usuarios', "Usuario Modificado Correctamente")
            #Aplicar Cambios
            miConexion.commit()
            self.ValModUsu=self.TreelistUsuarios.item(self.usuarioSeleccionado,text='',values=(self.txtCodeModifyUser.get(),self.txtNameModifyUser.get(),self.txtClaveModifyUser.get(),self.txtRolModifyUser.get(),))
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
            miConexion = sqlite3.connect('./PuntoVent/whatislove.db')
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



def main():
    app=Ventana()
    app.title('Sistema de Ventas')
    app.state('zoomed')
    tb.Style('darkly')
    app.mainloop()

if __name__=='__main__':
    main()