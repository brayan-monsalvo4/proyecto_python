import tkinter as tk
import view.MenuPrincipal as MP
from tkinter import messagebox
import sys

lista_operaciones = ["Seleccionar", "Agregar", "Eliminar", "Actualizar"]

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title = "Negocio Aromaterapia"
        self.geometry("900x500")
        self.protocol("WM_DELETE_WINDOW", self.__cerrar)
        self.resizable = True 

        self.cambiar_pantalla( MP.MenuPrincipal )
        

    def cambiar_pantalla(self, frame_class):
        """Recibe una clase Frame para mostrarla en la pantalla principal"""

        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack(expand=True, fill="both")

    def __cerrar(self):
        respuesta = messagebox.askyesno("Terminar?", "Quiere cerrar el programa?")
        if respuesta:
            self.destroy()
            sys.exit(0)


if __name__ == "__main__":
    app = Root()
    app.mainloop()
