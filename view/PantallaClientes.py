import tkinter as tk
import view.MenuPrincipal as mp

class PantallaClientes(tk.Frame):
    def __init__(self, ventana_principal):
        super().__init__(master=ventana_principal)

        self.frame_boton_salir = tk.Frame(master=self)
        self.frame_boton_salir.pack(side=tk.LEFT, anchor="n")
        self.frame_boton_salir.config(background="green")
        
        tk.Button(master=self.frame_boton_salir, text="regresar a la pantalla \nprincipal!",
                  command=self.__regresar_menu_principal).pack(side=tk.TOP)
        
        tk.Label(master=self.frame_boton_salir, text="Regresar al menu principal!").pack(side=tk.TOP)

    def __regresar_menu_principal(self):
        self.master.cambiar_pantalla(mp.MenuPrincipal)
        self.frame_boton_salir.destroy()
