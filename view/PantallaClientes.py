import tkinter as tk
from tkinter import ttk as ttkk
from tkinter import messagebox
import view.MenuPrincipal as mp
from controller.control_clientes import ControlClientes as cl
from excepciones.exceptions import *
import re

class PantallaClientes(tk.Frame):
    __clientes = cl()
    seleccion_actual = None
    def __init__(self, ventana_principal):
        super().__init__(master=ventana_principal)

        self.tabla = TablaClientes(frame=self)
        self.campos_texto = CamposTexto(frame=self)
        self.botones_salir = BotonRegresarMenu(frame=self)
        self.botones_operaciones = BotonesOperaciones(frame=self)

        self.tabla.pack(side="bottom")
        self.botones_operaciones.pack(side="bottom", expand=True, fill="x")
        self.botones_salir.pack(side="left", expand=True)
        self.campos_texto.pack(side="right", expand=True, fill="both", pady=50)

        self.tabla.obtener_clientes(self.__clientes.obtener_clientes())

    def buscar_cliente(self):
        parametro_busqueda = self.botones_operaciones.campo_buscar_cliente.get().strip()
        campo_busqueda = self.botones_operaciones.combo_columna.get()

        if not parametro_busqueda:
            messagebox.showerror("Error", "El campo no puede estar vacío!")
            return None

        resultado = self.__clientes.obtener_clientes(datos_cliente= {campo_busqueda:parametro_busqueda})

        if not resultado:
            messagebox.showinfo(title="Info", message="No se encontró!")
            return None

        self.tabla.obtener_clientes( resultado  )

        self.seleccion_actual = None
        self.campos_texto.limpiar_campos()

    def eliminar_cliente(self):
        if self.seleccion_actual == None or len( self.seleccion_actual ) == 0:
            messagebox.showerror(title="Error", message="Seleccione primero un cliente!")
            return None

        try:
            self.campos_texto.comprobar_campos_vacios()
            self.__clientes.eliminar_cliente( id_cliente= str( self.seleccion_actual[0] ) )
            self.tabla.limpiar_tabla()
            self.campos_texto.limpiar_campos()
            messagebox.showinfo(title="Éxito", message="el cliente se eliminó exitosamente!")
            self.mostrar_clientes()
        except CamposVacios:
            messagebox.showerror(title="Error", message="Los campos no pueden estar vacios!")
            return None

        self.seleccion_actual = None

    def registrar_cliente(self):

        try:
            self.campos_texto.comprobar_campos_vacios()

            cliente = self.campos_texto.obtener_datos()
            self.__clientes.registrar_cliente(cliente=cliente)

            self.campos_texto.limpiar_campos()

            self.tabla.obtener_clientes(lista_clientes= self.__clientes.obtener_clientes() )

            messagebox.showinfo(title="Éxito", message="el cliente se registró exitosamente!")
        except CamposVacios:
            messagebox.showerror(title="Error", message="Los campos no pueden estar vacios!")

        except DatosIncorrectos:
            messagebox.showerror(title="Error", message="Datos incorrectos!")          

        except RegistroExistente:
            messagebox.showerror(title="Error", message="El cliente ya existe!")

        self.seleccion_actual = None
        
    def actualizar_cliente(self):        
        if self.seleccion_actual == None or len( self.seleccion_actual ) == 0:
            messagebox.showerror(title="Error", message="Seleccione primero un cliente!")
            return None

        try:
            self.campos_texto.comprobar_campos_vacios()
            datos = self.campos_texto.obtener_datos()


            self.__clientes.actualizar_cliente( cliente=datos, id_cliente=str( self.seleccion_actual[0] ) )
            self.campos_texto.limpiar_campos()
            
            self.mostrar_clientes()

            messagebox.showinfo(title="Éxito", message="El cliente se ha actualizado con éxito!")

        except CamposVacios:
            messagebox.showerror(title="Error", message="Los campos no pueden estar vacios!")

        except DatosIncorrectos:
            messagebox.showerror(title="Error", message="Datos incorrectos!")

        self.seleccion_actual = None

    def mostrar_clientes(self):
        registros_clientes = self.__clientes.obtener_clientes()
        
        if len( registros_clientes ) == 0:
            messagebox.showinfo(title="Info", message="No hay clientes!")
            return None

        self.tabla.limpiar_tabla()

        self.tabla.obtener_clientes(lista_clientes=registros_clientes)
        self.seleccion_actual = None
        self.campos_texto.limpiar_campos()

        self.seleccion_actual = None
        
    def seleccionar_cliente(self):
        try:
            datos = self.tabla.tabla_clientes.item( self.tabla.tabla_clientes.selection()[0]).get("values")
            self.seleccion_actual = datos

            self.campos_texto.limpiar_campos()
            self.campos_texto.llenar_campos(datos)

        except IndexError:
            messagebox.showerror(title="Error", message="Seleccione primero una fila!")

            
class TablaClientes(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.tabla_clientes = ttkk.Treeview(
            master=self, columns=cl.columnas, height=14,show="headings")

        self.scroll_horizontal = ttkk.Scrollbar(
            master=self, orient=tk.HORIZONTAL, command=self.tabla_clientes.xview)
        self.scroll_vertical = ttkk.Scrollbar(
            master=self, orient=tk.VERTICAL, command=self.tabla_clientes.yview)

        self.scroll_horizontal.pack(side="bottom", fill=tk.X)
        self.scroll_vertical.pack(side="right", fill=tk.Y)

        self.tabla_clientes.configure(xscrollcommand=self.scroll_horizontal.set)

        self.tabla_clientes.configure(yscrollcommand=self.scroll_vertical.set)

        self.tabla_clientes.heading("#0", anchor="center")

        for num, campo in enumerate(cl.columnas):
            self.tabla_clientes.heading(
                f"#{num+1}", text=campo, anchor="center")
        
        self.tabla_clientes.pack()

    def obtener_clientes(self, lista_clientes):
        self.limpiar_tabla()

        for cliente in lista_clientes:

            self.tabla_clientes.insert(
                "", tk.END, values=tuple(cliente.values()))

    def limpiar_tabla(self):
        for registro in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(registro)
class CamposTexto(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.panel_izquierdo = tk.Frame(master=self)
        self.panel_central = tk.Frame(master=self)
        self.panel_derecho = tk.Frame(master=self)

        """ filas para los campos: nombre, telefono, ocupacion, correo y fecha de nacimiento """
        self.fila_1_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_2_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_3_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_4_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_5_izquierdo = tk.Frame(master=self.panel_izquierdo)

        """ fila para los campos: calle, colonia, codigo postal, ciudad y estado """
        self.fila_1_central = tk.Frame(master=self.panel_central)
        self.fila_2_central = tk.Frame(master=self.panel_central)
        self.fila_3_central = tk.Frame(master=self.panel_central)
        self.fila_4_central = tk.Frame(master=self.panel_central)
        self.fila_5_central = tk.Frame(master=self.panel_central)

        """fila para el campo: hobbies"""
        self.fila_1_derecha = tk.Frame(master=self.panel_derecho)

        """fila del campo nombre"""
        tk.Label( master=self.fila_1_izquierdo,text="Nombre:" ).pack( side="left" )
        self.campo_nombre = tk.Entry( master=self.fila_1_izquierdo )
        self.campo_nombre.pack( side="left", expand=True, fill="x" )
        self.fila_1_izquierdo.pack( side="top", expand=True, fill="x" )

        """fila del campo telefono"""
        tk.Label( master=self.fila_2_izquierdo,text="Telefono:" ).pack( side="left" )
        self.campo_telefono = tk.Entry( master=self.fila_2_izquierdo )
        self.campo_telefono.pack( side="left", padx=15 )
        self.fila_2_izquierdo.pack( side="top", expand=True, fill="x" )

        """fila del campo ocupacion"""
        tk.Label( master=self.fila_3_izquierdo,text="Ocupacion" ).pack( side="left" )
        self.campo_ocupacion = tk.Entry( master=self.fila_3_izquierdo )
        self.campo_ocupacion.pack( side="left", expand=True, fill="x" )
        self.fila_3_izquierdo.pack( side="top", expand=True, fill="x" )

        """fila del campo correo"""
        tk.Label( master=self.fila_4_izquierdo, text="Correo" ).pack( side="left" )
        self.campo_correo = tk.Entry( master=self.fila_4_izquierdo )
        self.campo_correo.pack( side="left", expand=True, fill="x" )
        self.fila_4_izquierdo.pack( side="top", expand=True, fill="x" )

        """fila del campo fecha, en la fila izquierda se encuentra el campo dia, mes y año"""
        tk.Label(master=self.fila_5_izquierdo, text="Dia").pack(side="left")
        self.campo_dia = tk.Entry(master=self.fila_5_izquierdo, width=6)
        self.campo_dia.pack(side="left", expand=True, fill="x")

        tk.Label(master=self.fila_5_izquierdo, text="Mes").pack(side="left")
        self.campo_mes = tk.Entry(master=self.fila_5_izquierdo, width=6)
        self.campo_mes.pack(side="left", expand=True, fill="x")

        tk.Label(master=self.fila_5_izquierdo, text="Año").pack(side="left")
        self.campo_anio = tk.Entry(master=self.fila_5_izquierdo, width=13)
        self.campo_anio.pack(side="left", expand=True, fill="x")

        self.fila_5_izquierdo.pack(side="top", expand=True)

        """fila del campo calle"""
        tk.Label(master=self.fila_1_central, text="Calle:").pack(side="left")
        self.campo_calle = tk.Entry(master=self.fila_1_central)
        self.campo_calle.pack(side="left", expand=True, fill="x")
        self.fila_1_central.pack(side="top", expand=True, fill="x")

        """fila del campo colonia"""
        tk.Label(master=self.fila_2_central, text="Colonia:").pack(side="left")
        self.campo_colonia = tk.Entry(master=self.fila_2_central)
        self.campo_colonia.pack(side="left", padx=15)
        self.fila_2_central.pack(side="top", expand=True, fill="x")

        """fila del campo codigo postal"""
        tk.Label(master=self.fila_3_central,text="Codigo postal").pack(side="left")
        self.campo_codigo_postal = tk.Entry(master=self.fila_3_central)
        self.campo_codigo_postal.pack(side="left", expand=True, fill="x")
        self.fila_3_central.pack(side="top", expand=True, fill="x")

        """fila del campo ciudad"""
        tk.Label(master=self.fila_4_central, text="Ciudad").pack(side="left")
        self.campo_ciudad = tk.Entry(master=self.fila_4_central)
        self.campo_ciudad.pack(side="left", expand=True, fill="x")
        self.fila_4_central.pack(side="top", expand=True, fill="x")

        """fila del campo estado"""
        tk.Label(master=self.fila_5_central, text="Estado").pack(side="left")
        self.campo_estado = tk.Entry(master=self.fila_5_central)
        self.campo_estado.pack(side="left", expand=True, fill="x")        
        self.fila_5_central.pack(side="top", expand=True, fill="x")


        """fila del campo hobbies"""
        tk.Label(master=self.fila_1_derecha, text="Hobbies:").pack(side="left")
        self.campo_hobbies = tk.Entry(master=self.fila_1_derecha)
        self.campo_hobbies.pack(side="left", expand=True, fill="x")

        self.fila_1_derecha.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.panel_derecho, text="Contacto").pack(side="top")
        self.campo_contacto = tk.Text(master=self.panel_derecho, height=3)
        self.campo_contacto.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.panel_derecho, text="Molestias").pack(side="top")
        self.campo_molestias = tk.Text(master=self.panel_derecho, height=3)
        self.campo_molestias.pack(side="top", expand=True, fill="x")

        self.panel_derecho.pack(side="right", expand=True, fill="both", padx=5)
        self.panel_central.pack(side="right", expand=True, fill="both", padx=5)
        self.panel_izquierdo.pack(
            side="right", expand=True, fill="both", padx=5)

    def obtener_datos(self) -> dict:
        datos_cliente = dict()

        datos_cliente.update({"nombre" : self.campo_nombre.get().strip()})

        calle = self.__limpiar_dato( self.campo_calle.get().strip() )
        colonia = self.__limpiar_dato( self.campo_colonia.get().strip() )
        codigo_postal = self.__limpiar_dato( self.campo_codigo_postal.get().strip() )
        ciudad = self.__limpiar_dato( self.campo_ciudad.get().strip() )
        estado = self.__limpiar_dato( self.campo_estado.get().strip() )

        direccion_completa = f"{calle};{colonia};{codigo_postal};{ciudad};{estado}"

        dia = self.campo_dia.get().strip()
        mes = self.campo_mes.get().strip()
        anio = self.campo_anio.get().strip()

        fecha_completa = f"{dia}-{mes}-{anio}"

        datos_cliente.update( {"direccion" : direccion_completa} )
        datos_cliente.update( {"correo" : self.campo_correo.get().strip()} )
        datos_cliente.update( {"telefono" : self.__limpiar_dato( self.campo_telefono.get().strip() )  } )
        datos_cliente.update( {"fecha_cumpleanos": fecha_completa} )
        datos_cliente.update( {"ocupacion": self.campo_ocupacion.get().strip()} )
        datos_cliente.update( {"hobbies": self.campo_hobbies.get().strip()} )
        datos_cliente.update( {"info_primer_interaccion": self.campo_contacto.get("1.0", "end-1c").strip()} )
        datos_cliente.update( {"molestias" : self.campo_molestias.get("1.0", "end-1c").strip()} )

        return datos_cliente

    def limpiar_campos(self):
        self.campo_nombre.delete(0, "end")
        self.campo_correo.delete(0, "end")
        self.campo_telefono.delete(0, "end")
        self.campo_hobbies.delete(0, "end")
        self.campo_ocupacion.delete(0, "end")
        self.campo_contacto.delete("1.0", "end")
        self.campo_molestias.delete("1.0", "end")
        self.campo_dia.delete(0, "end")
        self.campo_mes.delete(0, "end")
        self.campo_anio.delete(0, "end")
        self.campo_calle.delete(0, "end")
        self.campo_colonia.delete(0, "end")
        self.campo_codigo_postal.delete(0, "end")
        self.campo_ciudad.delete(0, "end")
        self.campo_estado.delete(0, "end")

        self.master.seleccion_actual = None

    def comprobar_campos_vacios(self):
        if not self.campo_nombre.get().strip():
            raise CamposVacios
        if not self.campo_telefono.get().strip():
            raise CamposVacios
        if not self.campo_ocupacion.get().strip():
            raise CamposVacios
        if not self.campo_correo.get().strip():
            raise CamposVacios
        if not self.campo_dia.get().strip():
            raise CamposVacios
        if not self.campo_mes.get().strip():
            raise CamposVacios
        if not self.campo_anio.get().strip():
            raise CamposVacios
        if not self.campo_calle.get().strip():
            raise CamposVacios
        if not self.campo_colonia.get().strip():
            raise CamposVacios
        if not self.campo_codigo_postal.get().strip():
            raise CamposVacios
        if not self.campo_estado.get().strip():
            raise CamposVacios
        if not self.campo_ciudad.get().strip():
            raise CamposVacios
        if not self.campo_hobbies.get().strip():
            raise CamposVacios
        if not self.campo_contacto.get("1.0", "end-1c").strip():
            raise CamposVacios
        if not self.campo_molestias.get("1.0", "end-1c").strip():
            raise CamposVacios

    def llenar_campos(self, lista_datos):
        self.campo_nombre.insert( string=lista_datos[1] , index=0)

        direccion = re.split(r";", lista_datos[2])

        self.campo_calle.insert(string=direccion[0], index=0)
        self.campo_colonia.insert(string=direccion[1], index=0)
        self.campo_codigo_postal.insert(string=direccion[2], index=0)
        self.campo_ciudad.insert(string=direccion[3], index=0)
        self.campo_estado.insert(string=direccion[4], index=0)
        
        self.campo_correo.insert( string=lista_datos[3] , index=0)
        self.campo_telefono.insert( string=lista_datos[4] , index=0)

        dia, mes, anio = lista_datos[5].split("-")

        self.campo_dia.insert(string=dia, index=0)
        self.campo_mes.insert(string=mes, index=0)
        self.campo_anio.insert(string=anio, index=0)

        self.campo_hobbies.insert( string=lista_datos[6] , index=0)
        self.campo_ocupacion.insert( string=lista_datos[7] , index=0)
        self.campo_contacto.insert( tk.END, lista_datos[8] )
        self.campo_molestias.insert( tk.END, lista_datos[9])

    def __limpiar_dato(self, cadena) -> str:
        simbolos = [";", ",", "%", "@", "^", "&", "*", "(", ")", "-", "_", "+", "="]
        nueva_cadena = ""

        for caracter in cadena:
            if caracter not in simbolos:
                nueva_cadena += caracter

        return nueva_cadena
    
class BotonRegresarMenu(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)
        self.boton_salir_menu = tk.Button(self, text="Regresar al menu principal", command=self.regresar_pantalla_principal)

        self.boton_salir_menu.pack(side="top")

    def regresar_pantalla_principal(self):
        self.master.master.cambiar_pantalla(mp.MenuPrincipal)
        self.destroy()

class BotonesOperaciones(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.boton_seleccionar_cliente = tk.Button(
            master=self, text="Seleccionar", command=self.master.seleccionar_cliente)
        self.campo_buscar_cliente = tk.Entry(master=self)
        self.combo_columna = ttkk.Combobox(
            master=self, values=cl.columnas, state="readonly")
        self.combo_columna.current(0)

        self.boton_buscar_cliente = tk.Button(
            master=self, text="Buscar cliente", command=self.master.buscar_cliente)
        self.boton_eliminar_cliente = tk.Button(
            master=self, text="Eliminar cliente", command=self.master.eliminar_cliente)
        self.actualizar_cliente = tk.Button(
            master=self, text="Actualizar cliente", command=self.master.actualizar_cliente)
        self.registrar_cliente = tk.Button(
            master=self, text="Agregar cliente", command=self.master.registrar_cliente)
        self.boton_consultar_clientes = tk.Button(
            master=self, text="Consultar todos los clientes", command=self.master.mostrar_clientes
        )

        self.boton_limpiar_campos = tk.Button(
            master=self, text="Limpiar campos", command=self.master.campos_texto.limpiar_campos
        )

        self.boton_seleccionar_cliente.pack(side="left", padx=20)
        self.campo_buscar_cliente.pack(side="left", padx=10)
        self.combo_columna.pack(side="left")

        self.boton_buscar_cliente.pack(side="left", padx=10)
        self.boton_eliminar_cliente.pack(side="left", padx=10)
        self.actualizar_cliente.pack(side="left", padx=10)
        self.registrar_cliente.pack(side="left", padx=10)
        self.boton_consultar_clientes.pack(side="left", padx=10)
        self.boton_limpiar_campos.pack(side="left", padx=10)