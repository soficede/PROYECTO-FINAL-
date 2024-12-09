from Modelo import Usuario

class ControladorUsuario:
    def __init__(self):
        self.usuario_modelo = Usuario("", "", "", "")

    def validar_usuario(self, nombre, contraseña):
        return self.usuario_modelo.validarCredenciales(nombre, contraseña)
