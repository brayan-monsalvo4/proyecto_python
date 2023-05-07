class InventarioVacio(Exception):
    def __init__(self):
        self.message = "No hay productos en el inventario!"
        super().__init__(self.message)

class CamposIncorrectos(Exception):
    def __init__(self):
        self.message = "Producto con campos incorrectos!"
        super().__init__(self.message)

class DatosIncorrectos(Exception):
    def __init__(self):
        self.message = "Datos del producto incorrectos!"
        super().__init__(self.message)

class CamposVacios(Exception):
    def __init__(self):
        self.message = "Producto con datos vacios!"
        super().__init__(self.message)

class ProductoNoEncontrado(Exception):
    def __init__(self):
        self.message = "Producto no encontrado!"
        super().__init__(self.message)

class CodigoIncorrecto(Exception):
    def __init__(self):
        self.message = "El codigo del producto es incorrecto!"
        super().__init__(self.message)

class ProductoExistente(Exception):
    def __init__(self):
        self.message = "El producto ya existe!"
        super().__init__(self.message)

class ProductoNoExistente(Exception):
    def __init__(self):
        self.message = "El producto no existe!"
        super().__init__(self.message)

        