import tkinter as tk
from tkinter import ttk as ttkk
import view.MenuPrincipal as mp
import model.cliente as cl

clientes = cl.Clientes()


class PantallaClientes(tk.Frame):
    def __init__(self, ventana_principal):
        super().__init__(master=ventana_principal)

        self.tabla = TablaClientes(frame=self)

        self.tabla.pack(side="bottom")

        self.tabla.obtener_clientes(clientes.consultar_cliente())

        self.botones_operaciones = BotonesOperaciones(frame=self)
        self.botones_operaciones.pack(side="bottom", expand=True, fill="x")

        self.botones_salir = BotonRegresarMenu(frame=self)
        self.botones_salir.pack(side="left", expand=True)

        self.campos_texto = CamposTexto(frame=self)

        self.campos_texto.pack(side="right", expand=True, fill="both", pady=50)

    def buscar_cliente(self):
        print("se presiono buscar_cliente :D")

    def eliminar_cliente(self):
        print("se presiono eliminar_cliente :D")

    def registrar_cliente(self):
        print("se presiono registrar_cliente :D")

    def actualizar_cliente(self):
        print("se presiono actualizar cliente :D")

    def mostrar_clientes(self):
        print("mostrar clientes XD")

    def seleccionar_cliente(self):
        print("se selecciono un cliente XD")


class TablaClientes(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.tabla_clientes = ttkk.Treeview(
            master=self, columns=cl.columnas, show="headings", height=14)

        self.scroll_horizontal = ttkk.Scrollbar(
            master=self, orient=tk.HORIZONTAL, command=self.tabla_clientes.xview)
        self.scroll_vertical = ttkk.Scrollbar(
            master=self, orient=tk.VERTICAL, command=self.tabla_clientes.yview)

        self.scroll_horizontal.pack(side="bottom", fill=tk.X)
        self.scroll_vertical.pack(side="right", fill=tk.Y)

        self.tabla_clientes.configure(
            xscrollcommand=self.scroll_horizontal.set)
        self.tabla_clientes.configure(yscrollcommand=self.scroll_vertical.set)

        for num, campo in enumerate(cl.columnas):
            self.tabla_clientes.heading(
                f"#{num+1}", text=campo, anchor="center")

        self.tabla_clientes.pack()

    def obtener_clientes(self, lista_clientes):
        for indice, cliente in enumerate(lista_clientes):
            self.tabla_clientes.insert(
                "", tk.END, text=f"{indice}", values=cliente)


class CamposTexto(tk.Frame):
    def __init__(self, frame):
        super().__init__(master=frame)

        self.panel_izquierdo = tk.Frame(master=self)
        self.panel_central = tk.Frame(master=self)
        self.panel_derecho = tk.Frame(master=self)

        self.fila_1_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_2_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_3_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_4_izquierdo = tk.Frame(master=self.panel_izquierdo)
        self.fila_5_izquierdo = tk.Frame(master=self.panel_izquierdo)

        self.fila_1_central = tk.Frame(master=self.panel_central)
        self.fila_2_central = tk.Frame(master=self.panel_central)
        self.fila_3_central = tk.Frame(master=self.panel_central)
        self.fila_4_central = tk.Frame(master=self.panel_central)
        self.fila_5_central = tk.Frame(master=self.panel_central)

        self.fila_1_derecha = tk.Frame(master=self.panel_derecho)

        tk.Label(master=self.fila_1_izquierdo,
                 text="Nombre:").pack(side="left")
        self.campo_nombre = tk.Entry(master=self.fila_1_izquierdo)
        self.campo_nombre.pack(side="left", expand=True, fill="x")

        self.fila_1_izquierdo.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_2_izquierdo,
                 text="Telefono:").pack(side="left")
        self.campo_telefono = tk.Entry(master=self.fila_2_izquierdo)
        self.campo_telefono.pack(side="left", padx=15)

        self.fila_2_izquierdo.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_3_izquierdo,
                 text="Ocupacion").pack(side="left")
        self.campo_ocupacion = tk.Entry(master=self.fila_3_izquierdo)
        self.campo_ocupacion.pack(side="left", expand=True, fill="x")

        self.fila_3_izquierdo.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_4_izquierdo, text="Correo").pack(side="left")
        self.campo_correo = tk.Entry(master=self.fila_4_izquierdo)
        self.campo_correo.pack(side="left", expand=True, fill="x")

        self.fila_4_izquierdo.pack(side="top", expand=True, fill="x")

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

        tk.Label(master=self.fila_1_central, text="Calle:").pack(side="left")
        self.campo_calle = tk.Entry(master=self.fila_1_central)
        self.campo_calle.pack(side="left", expand=True, fill="x")

        self.fila_1_central.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_2_central, text="Colonia:").pack(side="left")
        self.campo_colonia = tk.Entry(master=self.fila_2_central)
        self.campo_colonia.pack(side="left", padx=15)

        self.fila_2_central.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_3_central,
                 text="Codigo postal").pack(side="left")
        self.campo_codigo_postal = tk.Entry(master=self.fila_3_central)
        self.campo_codigo_postal.pack(side="left", expand=True, fill="x")

        self.fila_3_central.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_4_central, text="Estado").pack(side="left")
        self.campo_estado = tk.Entry(master=self.fila_4_central)
        self.campo_estado.pack(side="left", expand=True, fill="x")

        self.fila_4_central.pack(side="top", expand=True, fill="x")

        tk.Label(master=self.fila_5_central, text="Ciudad").pack(side="left")
        self.campo_ciudad = tk.Entry(master=self.fila_5_central)
        self.campo_ciudad.pack(side="left", expand=True, fill="x")

        self.fila_5_central.pack(side="top", expand=True, fill="x")

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


class BotonRegresarMenu(tk.Frame):
    def __init__(self, frame):
        super().__init__(frame)
        self.boton_salir_menu = tk.Button(
            self, text="Regresar al menu principal", command=self.regresar_pantalla_principal)
        self.etiqueta_salir_menu = tk.Label(
            self, text="Regresar al menu principal")

        self.boton_salir_menu.pack(side="top")
        self.etiqueta_salir_menu.pack(side="top")

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

        self.boton_seleccionar_cliente.pack(side="left", padx=20)
        self.campo_buscar_cliente.pack(side="left", padx=10)
        self.combo_columna.pack(side="left")

        self.boton_buscar_cliente.pack(side="left", padx=15)
        self.boton_eliminar_cliente.pack(side="left", padx=15)
        self.actualizar_cliente.pack(side="left", padx=15)
        self.registrar_cliente.pack(side="left", padx=15)
