import tkinter as tk
from tkinter import ttk as ttkk
import view.MenuPrincipal as mp
from controller.control_productos import ControlProductos as pr
import app as ap
from tkinter import messagebox
from excepciones.exceptions import *


class PantallaProductos(tk.Frame):
    __productos = pr()
    seleccion_actual = None

    def __init__(self, ventana_principal):
        super().__init__(master=ventana_principal)

        self.tabla = TablaProductos(frame=self)
        self.campos_texto = CamposTexto(frame = self)
        self.botones_salir = BotonRegresarMenu(frame=self)
        self.botones_operaciones = BotonesOperaciones(frame=self)

        self.tabla.pack(side="bottom")
        self.botones_operaciones.pack(side="bottom", expand=True, fill="x")
        self.botones_salir.pack(side="left", expand=True)
        self.campos_texto.pack(side="right", pady=50, expand=True, fill="both")

        #self.tabla.obtener_productos(productos.consultar_producto())

    def buscar_producto(self):
        parametro_busqueda = self.botones_operaciones.campo_buscar_producto.get().strip()
        campo_busqueda = self.botones_operaciones.combo_columna.get()

        if not parametro_busqueda:
            messagebox.showerror("Error", "El campo no puede estar vacío!")
            return None
        
        resultado = self.__productos.obtener_productos(datos_producto={campo_busqueda : parametro_busqueda})

        if not resultado:
            messagebox.showinfo(title="Info", message="No se encontró!")
            return None

        self.tabla.obtener_productos( resultado )
        self.seleccion_actual = None
        self.campos_texto.limpiar_campos()

    def eliminar_producto(self):
        if self.seleccion_actual is None or len( self.seleccion_actual ) == 0:
            messagebox.showerror(title="Error", message="Seleccione primero un producto!")
            return None

        try:
            self.campos_texto.comprobar_campos_vacios()

            res = messagebox.askyesnocancel(title="?", message="Quiere eliminar el producto?")

            if not res or res is None:
                self.seleccion_actual = None
                return None

            self.__productos.eliminar_producto(codigo_producto= str( self.seleccion_actual[0] ))
            self.tabla.limpiar_tabla()
            self.campos_texto.limpiar_campos()
            messagebox.showinfo(title="Éxito", message="El producto se eliminó exitosamente")
            self.mostrar_productos()
        except CamposVacios:
            self.seleccion_actual = None
            messagebox.showerror(title="Error", message="Los campos no pueden estar vacios!")
            return None

        self.seleccion_actual = None

    def registrar_producto(self):
        try:
            self.campos_texto.comprobar_campos_vacios()
            
            producto = self.campos_texto.obtener_datos()

            self.__productos.registrar_producto(producto=producto)

            self.campos_texto.limpiar_campos()

            self.mostrar_productos()

            messagebox.showinfo(title="Éxito", message="el producto se registró exitosamente!")
        except CamposVacios:
            messagebox.showerror(title="Error", message="Los campos no pueden estar vacios!")
        
        except DatosIncorrectos:
            messagebox.showerror(title="Error", message="Datos incorrectos!")          

        except RegistroExistente:
            messagebox.showerror(title="Error", message="El producto ya existe!")
        
        self.seleccion_actual = None

    def actualizar_producto(self):
        if self.seleccion_actual is None or len(self.seleccion_actual) == 0:
            messagebox.showerror("Error", "Seleccione primero un producto!")
            return None
        
        try:
            self.campos_texto.comprobar_campos_vacios()
            datos = self.campos_texto.obtener_datos()

            res = messagebox.askyesnocancel(title="?", message="Quiere actualizar el producto?")

            if not res or res is None:
                self.seleccion_actual = None
                return None

            self.__productos.actualizar_producto(producto=datos, codigo_producto= str(self.seleccion_actual[0]))
            self.mostrar_productos()
            messagebox.showinfo(title="Éxito", message="El producto se ha actualizado con éxito!")
        except CamposVacios:
            messagebox.showerror(title="Error", message="Los campos no pueden estar vacios!")

        except DatosIncorrectos:
            messagebox.showerror(title="Error", message="Datos incorrectos!")

        self.seleccion_actual = None

    def mostrar_productos(self):
        registros_clientes = self.__productos.obtener_productos()

        if len(registros_clientes) == 0:
            messagebox.showinfo(title="Info", message="No hay productos!")
            self.seleccion_actual = None
            return None
        
        self.tabla.limpiar_tabla()
        self.tabla.obtener_productos(lista_productos=registros_clientes)
        self.campos_texto.limpiar_campos()

        self.seleccion_actual = None

    def seleccionar_producto(self):
        try:
            datos = self.tabla.tabla_productos.item( self.tabla.tabla_productos.selection()[0]).get("values")
            self.seleccion_actual = datos

            self.campos_texto.limpiar_campos()
            self.campos_texto.llenar_campos(datos)
        
        except IndexError:
            messagebox.showerror(title="Error", message="Seleccione primero una fila!")
class TablaProductos(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.tabla_productos = ttkk.Treeview(master=self, columns=pr.columnas, show="headings", height=14)

        self.scroll_horizontal = ttkk.Scrollbar(master=self, orient=tk.HORIZONTAL, command=self.tabla_productos.xview)
        self.scroll_vertical = ttkk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.tabla_productos.yview)

        self.scroll_horizontal.pack(side="bottom", fill=tk.X)
        self.scroll_vertical.pack(side="right", fill=tk.Y)

        self.tabla_productos.configure(xscrollcommand=self.scroll_horizontal.set)
        self.tabla_productos.configure(yscrollcommand=self.scroll_vertical.set)

        for num, campo in enumerate(pr.columnas):
            self.tabla_productos.heading(f"#{num+1}", text=campo, anchor="center")

        self.tabla_productos.pack()

    def obtener_productos(self, lista_productos):
        """ for indice, producto in enumerate(lista_productos):
            self.tabla_productos.insert("", tk.END, text=f"{indice}", values=producto) """
        
        self.limpiar_tabla()

        for producto in lista_productos:
            self.tabla_productos.insert("", tk.END, values=tuple(producto.values()))
        
    def limpiar_tabla(self):
        for registro in self.tabla_productos.get_children():
            self.tabla_productos.delete(registro)

        
class CamposTexto(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)
        
        self.panel_izquierdo = tk.Frame(master=self)
        self.panel_derecho = tk.Frame(master=self)

        self.fila_1 = tk.Frame(master=self.panel_izquierdo)
        self.fila_2 = tk.Frame(master=self.panel_izquierdo)
        self.fila_3 = tk.Frame(master=self.panel_izquierdo)
        self.fila_4 = tk.Frame(master=self.panel_izquierdo)

        tk.Label(master=self.fila_1, text="Nombre:").pack(side="left")
        self.campo_nombre = tk.Entry(master=self.fila_1)
        self.campo_nombre.pack(side="left", expand=True, fill="x")
        self.fila_1.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_2, text="Precio:").pack(side="left")
        self.campo_precio = tk.Entry(master=self.fila_2)
        self.campo_precio.pack(side="left", padx=15)
        self.fila_2.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_3, text="Cantidad en stock:").pack(side="left")
        self.campo_cantidad_stock = tk.Entry(master=self.fila_3)
        self.campo_cantidad_stock.pack(side="left", expand=True, fill="x")
        self.fila_3.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_4, text="Duracion:").pack(side="left")
        self.campo_duracion_producto = tk.Entry(master=self.fila_4)
        self.campo_duracion_producto.pack(side="left", expand=True, fill="x")
        self.fila_4.pack(side="top", expand=True, fill="x")
        
        
        tk.Label(master=self.panel_derecho, text="Descripcion").pack(side="top")
        self.campo_descripcion = tk.Text(master=self.panel_derecho, height=3)
        self.campo_descripcion.pack(side="top")

        tk.Label(master=self.panel_derecho, text="Beneficios").pack(side="top")
        self.campo_beneficios = tk.Text(master=self.panel_derecho, height=3)
        self.campo_beneficios.pack(side="top")

        self.panel_derecho.pack(side="right", expand=True, fill="both")
        self.panel_izquierdo.pack(side="right", expand=True, fill="both")

    def obtener_datos(self) -> dict:
        datos_producto = dict()

        datos_producto.update( {"nombre" : self.campo_nombre.get().strip() } )
        datos_producto.update( {"descripcion" : self.campo_descripcion.get("1.0", "end-1c").strip() } )
        datos_producto.update( {"precio" : self.campo_precio.get().strip() })
        datos_producto.update( {"cantidad_stock" : self.campo_cantidad_stock.get().strip()} )
        datos_producto.update( {"duracion_producto" : self.campo_duracion_producto.get().strip() } )
        datos_producto.update( {"beneficios" : self.campo_beneficios.get("1.0", "end-1c").strip()} )

        return datos_producto
    
    def limpiar_campos(self):
        self.campo_nombre.delete(0, "end")
        self.campo_descripcion.delete("1.0", "end")
        self.campo_precio.delete(0, "end")
        self.campo_cantidad_stock.delete(0, "end")
        self.campo_duracion_producto.delete(0, "end")
        self.campo_beneficios.delete("1.0", "end")

    def comprobar_campos_vacios(self):
        if not self.campo_nombre.get().strip():
            raise CamposVacios
        if not self.campo_descripcion.get("1.0", "end-1c").strip():
            raise CamposVacios
        if not self.campo_precio.get().strip():
            raise CamposVacios
        if not self.campo_cantidad_stock.get().strip():
            raise CamposVacios
        if not self.campo_duracion_producto.get().strip():
            raise CamposVacios
        if not self.campo_beneficios.get("1.0", "end-1c").strip():
            raise CamposVacios
        
    def llenar_campos(self, lista_datos):
        self.campo_nombre.insert( string=lista_datos[1], index=0)
        self.campo_descripcion.insert(tk.END, lista_datos[2])
        self.campo_precio.insert(string=lista_datos[3], index=0)
        self.campo_cantidad_stock.insert(string=lista_datos[4], index=0)
        self.campo_duracion_producto.insert(string=lista_datos[5], index=0)
        self.campo_beneficios.insert(tk.END, lista_datos[6])

class BotonRegresarMenu(tk.Frame):
    def __init__(self, frame):
        super().__init__(frame)
        self.boton_salir_menu = tk.Button(self, text="Regresar al menu principal", command=self.regresar_pantalla_principal)

        self.boton_salir_menu.pack(side="top")

    def regresar_pantalla_principal(self):
        self.master.master.cambiar_pantalla(mp.MenuPrincipal)
        self.destroy()
        
class BotonesOperaciones(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.boton_seleccionar_producto = tk.Button(master=self, text="Seleccionar", command=self.master.seleccionar_producto)
        self.campo_buscar_producto = tk.Entry(master=self)
        self.combo_columna = ttkk.Combobox(master=self, values=pr.columnas, state="readonly")
        self.combo_columna.current(0)

        self.boton_buscar_producto = tk.Button(master=self, text="Buscar producto", command=self.master.buscar_producto)
        self.boton_eliminar_producto = tk.Button(master=self, text="Eliminar producto", command=self.master.eliminar_producto)
        self.actualizar_producto = tk.Button(master=self, text="Actualizar producto", command=self.master.actualizar_producto)
        self.registrar_producto = tk.Button(master=self, text="Agregar producto", command=self.master.registrar_producto)
        self.obtener_productos = tk.Button(master=self, text="Obtener todos los productos", command=self.master.mostrar_productos)
        self.boton_limpiar_campos = tk.Button(master=self, text="Limpiar campos", command=self.master.campos_texto.limpiar_campos)

        self.boton_seleccionar_producto.pack(side="left", padx=20)
        self.campo_buscar_producto.pack(side="left", padx=10)
        self.combo_columna.pack(side="left")



        self.boton_buscar_producto.pack(side="left", padx=10)
        self.boton_eliminar_producto.pack(side="left", padx=10)
        self.actualizar_producto.pack(side="left", padx=10)
        self.registrar_producto.pack(side="left", padx=10)
        self.obtener_productos.pack(side="left", padx=10)
        self.boton_limpiar_campos.pack(side="left", padx=10)

