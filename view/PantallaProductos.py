import tkinter as tk
from tkinter import ttk as ttkk
import view.MenuPrincipal as mp
import model.producto as pr
import app as ap

productos = pr.Productos()

class PantallaProductos(tk.Frame):
    def __init__(self, ventana_principal):
        super().__init__(master=ventana_principal)

        self.tabla = TablaProductos(frame=self)

        self.tabla.pack(side="bottom")

        self.tabla.obtener_productos(productos.consultar_producto())

        self.botones_operaciones = BotonesOperaciones(frame=self)
        self.botones_operaciones.pack(side="bottom", expand=True, fill="x")

        self.campos_texto = CamposTexto(frame = self)

        self.campos_texto.pack(side="right", pady=50, padx=50)

        self.botones_salir = BotonRegresarMenu(frame=self)
        self.botones_salir.pack(side="left")

    def buscar_producto(self):
        print("se presiono buscar_producto :D")

    def eliminar_producto(self):
        print("se presiono eliminar_producto :D")
    
    def registrar_producto(self):
        print("se presiono registrar_producto :D")
    
    def actualizar_producto(self):
        print("se presiono actualizar producto :D")

    def mostrar_productos(self):
        print("mostrar productos XD")

    def seleccionar_producto(self):
        print("se selecciono un producto XD")

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
        for indice, producto in enumerate(lista_productos):
            self.tabla_productos.insert("", tk.END, text=f"{indice}", values=producto)
        
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

        tk.Label(master=self.fila_3, text="Cantidad en stock (solo numero entero):").pack(side="left")
        self.campo_cantidad_stock = tk.Entry(master=self.fila_3)
        self.campo_cantidad_stock.pack(side="left", expand=True, fill="x")
        
        self.fila_3.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_4, text="Duracion (dias, solamente numeros enteros):").pack(side="left")
        self.campo_duracion_producto = tk.Entry(master=self.fila_4)
        self.campo_duracion_producto.pack(side="left", expand=True, fill="x")
        
        self.fila_4.pack(side="top", expand=True, fill="x")
        
        
        tk.Label(master=self.panel_derecho, text="Descripcion").pack(side="top")
        self.campo_descripcion = tk.Entry(master=self.panel_derecho)

        self.campo_descripcion.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.panel_derecho, text="Beneficios").pack(side="top")
        self.campo_beneficios = tk.Entry(master=self.panel_derecho)

        self.campo_beneficios.pack(side="top", expand=True, fill="x")


        self.panel_derecho.pack(side="right", expand=True, fill="both")
        self.panel_izquierdo.pack(side="right", expand=True, fill="both")

class BotonRegresarMenu(tk.Frame):
    def __init__(self, frame):
        super().__init__(frame)
        self.boton_salir_menu = tk.Button(self, text="Regresar al menu principal", command=self.regresar_pantalla_principal)
        self.etiqueta_salir_menu = tk.Label(self, text="Regresar al menu principal")

        self.boton_salir_menu.pack(side="top", padx=50, pady=50)
        self.etiqueta_salir_menu.pack(side="top", padx=50, pady=50)

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

        self.boton_seleccionar_producto.pack(side="left", padx=20)
        self.campo_buscar_producto.pack(side="left", padx=10)
        self.combo_columna.pack(side="left")

        self.boton_buscar_producto.pack(side="left", padx=15)
        self.boton_eliminar_producto.pack(side="left", padx=15)
        self.actualizar_producto.pack(side="left", padx=15)
        self.registrar_producto.pack(side="left", padx=15)

