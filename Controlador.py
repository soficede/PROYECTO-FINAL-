from Modelo import Usuario
from Modelo import Medicamento
from Modelo import SeguimientoMedicamento
from datetime import datetime

class ControladorUsuario:
    def __init__(self):
        self.usuario_model = Usuario("", "", "", "")

    def validar_credenciales(self, nombre, contraseña):
        return self.usuario_model.validarCredenciales(nombre, contraseña)

    def registrar_usuario(self, nombre, contraseña, correo, rol):
        return self.usuario_model.guardarUsuario(nombre, contraseña, correo, rol)

class ControladorMedicamento:
    def __init__(self):
        self.medicamento_model = Medicamento()

    def agregar_medicamento(self, nombre, dosis, frecuencia, fecha_vencimiento, stock):
        medicamento = Medicamento(
            nombre=nombre,
            dosis=dosis,
            frecuencia=frecuencia,
            fechaVencimiento=fecha_vencimiento,
            stock=stock
        )
        return medicamento.guardarMedicamentoEnBD()

    def obtener_medicamentos(self):
        return self.medicamento_model.cargarMedicamentosDesdeBD()

    def obtener_medicamento_por_id(self, id):
        return self.medicamento_model.buscarMedicamentoPorID(id)

    def eliminar_medicamento(self, id):
        medicamento = Medicamento(id=id)
        return medicamento.eliminarMedicamento()

    def editar_medicamento(self, id, nombre=None, dosis=None, frecuencia=None, fecha_vencimiento=None, stock=None):
        medicamento = Medicamento(id=id)
        return medicamento.modificarMedicamento(nombre, dosis, frecuencia, fecha_vencimiento, stock)

class ControladorSeguimiento:
    def __init__(self):
        pass

    def crear_seguimiento(self, medicamento_id, fecha_ingreso, frecuencia, stock):
        # Crear un objeto SeguimientoMedicamento
        seguimiento = SeguimientoMedicamento(medicamento_id, fecha_ingreso, frecuencia, stock)
        return seguimiento.guardarSeguimientoEnBD()

    def obtener_seguimientos(self, medicamento_id=None):
        # Crear un objeto SeguimientoMedicamento y obtener los seguimientos
        seguimiento = SeguimientoMedicamento(medicamento_id, None, None, None)
        return seguimiento.verSeguimientos(medicamento_id)