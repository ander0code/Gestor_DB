from tkinter import*
from tkinter import ttk,messagebox
import ttkbootstrap as tb
#Impor libreria pa conectar BD
import sqlite3

class Ventana(tb.Window):
    def __init__(self):
        super().__init__()
        self.ventanaLogin()
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


        #Capturar errores
        try:
            #Establecer conexión
            miConexion=sqlite3.connect('./PuntoVent/whatislove.db')
            #Crear cursor
            miCursor=miConexion.cursor()

            nombreUsuario=self.txtUsuario.get()
            claveUsuario=self.txtClave.get()

            miCursor.execute("SELECT * FROM Usuarios WHERE Nombre=? AND Clave=?", (nombreUsuario,claveUsuario))
            #Traer todos los registros y guardar en "datos"
            datosLogueo=miCursor.fetchall()
            if datosLogueo!="":
                for row in datosLogueo:
                    codUsuario=row[0]
                    nomUsuario=row[1]
                    claUsuario=row[2]
                    rolUsuario=row[3]
                if(nomUsuario==self.txtUsuario.get() and claUsuario==self.txtClave.get()):
                    self.frame_login.pack_forget()#ocultar ventana de login
                    self.ventanaMenu()#abrimos ventanamenu

            #Aplicar Cambios
            miConexion.commit()
            #Cerrar la conexion
            miConexion.close()

        except:
            #Mensaje de error porsiaca
            messagebox.showerror("Acceso", "El usuario o clave son incorrectos")
    #---------------USUARIOS------------
    def ventanaListaUsuarios(self):

        self.frameListaUsuarios=Frame(self.frameCenter)
        self.frameListaUsuarios.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframeBotonesListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeBotonesListUsu.grid(row=0,column=0,sticky=NSEW)

        btnNuevoUsuario=tb.Button(self.lblframeBotonesListUsu,text='Nuevo', width=15,bootstyle="success",command=self.ventanaNuevoUsuario)
        btnNuevoUsuario.grid(row=0,column=0,padx=5,pady=5)

        btnModificarUsuario=tb.Button(self.lblframeBotonesListUsu,text='Modificar', width=15,bootstyle="warning")
        btnModificarUsuario.grid(row=0,column=1,padx=5,pady=5)

        btnEliminarUsuario=tb.Button(self.lblframeBotonesListUsu,text='Eliminar', width=15,bootstyle="danger")
        btnEliminarUsuario.grid(row=0,column=2,padx=5,pady=5)

        self.lblframeBusqListUsu=LabelFrame(self.frameListaUsuarios)
        self.lblframeBusqListUsu.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        txtBusquedaUsuarios=ttk.Entry(self.lblframeBusqListUsu,width=100)
        txtBusquedaUsuarios.grid(row=0,column=0,padx=5,pady=5)

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

        lblCodeNewUser=Label(lblframeNewUser,text='Codigo')
        lblCodeNewUser.grid(row=0,column=0,padx=10,pady=10,sticky=E)
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


def main():
    app=Ventana()
    app.title('Sistema de Ventas')
    app.state('zoomed')
    tb.Style('darkly')
    app.mainloop()

if __name__=='__main__':
    main()