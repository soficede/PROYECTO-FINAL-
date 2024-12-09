from Modelo import Usuario, Medicamento

class ControladorUsuario:
    def __init__(self):
        self.usuario_modelo = Usuario("", "", "", "")

    def validar_usuario(self, nombre, contraseña):
        return self.usuario_modelo.validarCredenciales(nombre, contraseña)

    def registrar_usuario(self, nombre, contraseña, correo, rol):
        return self.usuario_modelo.guardarUsuario(nombre, contraseña, correo, rol)

class ControladorMedicamento:
    def __init__(self):
        self.medicamento_modelo = Medicamento()

    def listar_medicamentos(self):
        return self.medicamento_modelo.cargarMedicamentosDesdeBD()

    def agregar_medicamento(self, nombre, dosis, frecuencia, fecha_vencimiento, stock):
        nuevo_medicamento = Medicamento(
            nombre=nombre,
            dosis=dosis,
            frecuencia=frecuencia,
            fechaVencimiento=fecha_vencimiento,
            stock=stock
        )
        return nuevo_medicamento.guardarMedicamentoEnBD()

    def eliminar_medicamento(self, medicamento_id):
        medicamento = Medicamento(id=medicamento_id)
        return medicamento.eliminarMedicamento()
