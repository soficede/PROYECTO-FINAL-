from Modelo import Medicamento

class ControladorMedicamento:
    def __init__(self):
        self.medicamento_modelo = Medicamento()

    def listar_medicamentos(self):
        return self.medicamento_modelo.cargarMedicamentosDesdeBD()

    def agregar_medicamento(self, nombre, dosis, frecuencia, fecha_vencimiento, stock):
        medicamento = Medicamento(
            nombre=nombre, 
            dosis=dosis, 
            frecuencia=frecuencia, 
            fechaVencimiento=fecha_vencimiento, 
            stock=int(stock)
        )
        return medicamento.guardarMedicamentoEnBD()

    def eliminar_medicamento(self, medicamento_id):
        medicamento = Medicamento(id=medicamento_id)
        return medicamento.eliminarMedicamento()
