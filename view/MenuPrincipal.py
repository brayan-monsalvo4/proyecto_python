import tkinter as tk
from view import PantallaProductos
from view import PantallaClientes


class MenuPrincipal(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        #self.config(background="red")
        tk.Label(self, text="Menu principal :D").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Administrar productos",
                  command=lambda: root.cambiar_pantalla(PantallaProductos.PantallaProductos)).pack()
        
        tk.Button(self, text="Administrar clientes",
                  command=lambda: root.cambiar_pantalla(PantallaClientes.PantallaClientes)).pack()

