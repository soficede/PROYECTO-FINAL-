from Modelo import Usuario, Medicamento

class ControladorUsuario:
    def __init__(self):
        self.usuario_modelo = Usuario("", "", "", "")

    def validar_usuario(self, nombre, contraseña):
        return self.usuario_modelo.validarCredenciales(nombre, contraseña)

class ControladorUsuario:
    def __init__(self):
        self.usuario_modelo = Usuario("", "", "", "")

    def validar_usuario(self, nombre, contraseña):
        return self.usuario_modelo.validarCredenciales(nombre, contraseña)

    def registrar_usuario(self, nombre, contraseña, correo, rol):
        return self.usuario_modelo.guardarUsuario(nombre, contraseña, correo, rol)


