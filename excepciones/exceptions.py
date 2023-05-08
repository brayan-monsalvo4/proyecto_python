class TablaVacia(Exception):
    def __init__(self):
        self.message = "No hay registros en la tabla!"
        super().__init__(self.message)

class CamposIncorrectos(Exception):
    def __init__(self):
        self.message = "registro con campos incorrectos!"
        super().__init__(self.message)

class DatosIncorrectos(Exception):
    def __init__(self):
        self.message = "Datos del registro incorrectos!"
        super().__init__(self.message)

class CamposVacios(Exception):
    def __init__(self):
        self.message = "Registro con datos vacios!"
        super().__init__(self.message)

class RegistroNoEncontrado(Exception):
    def __init__(self):
        self.message = "Registro no encontrado!"
        super().__init__(self.message)

class CodigoIncorrecto(Exception):
    def __init__(self):
        self.message = "El identificador del registro es incorrecto!"
        super().__init__(self.message)

class RegistroExistente(Exception):
    def __init__(self):
        self.message = "El registro ya existe!"
        super().__init__(self.message)

class RegistroNoExistente(Exception):
    def __init__(self):
        self.message = "El registro no existe!"
        super().__init__(self.message)

        