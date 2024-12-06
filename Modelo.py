class Usuario:
    def __init__(self, nombre, correo, contraseña, rol):
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.rol = rol

    def validarCredenciales(self, nombre, contraseña):
        # Cargar usuarios desde el archivo
        usuarios = self.cargarUsuariosDesdeTxt()
        for usuario in usuarios:
            if usuario["nombre"] == nombre and usuario["contraseña"] == contraseña:
                return True
        return False

    def cargarUsuariosDesdeTxt(self):
        usuarios = []
        try:
            with open("Usuarios.txt", "r") as file:
                for line in file:
                    # Leer cada línea y separar los datos por ":"
                    nombre, contraseña, correo, rol = line.strip().split(":")
                    usuario = {"nombre": nombre, "contraseña": contraseña, "correo": correo, "rol": rol}
                    usuarios.append(usuario)
        except FileNotFoundError:
            print("El archivo Usuarios.txt no existe.")
        return usuarios

    def guardarUsuario(self, nombre, contraseña, correo, rol):
        # Verificar si el usuario ya existe
        usuarios = self.cargarUsuariosDesdeTxt()
        for usuario in usuarios:
            if usuario["nombre"] == nombre:
                print("El usuario ya existe.")
                return False
        
        # Si el usuario no existe, guardarlo en una nueva línea
        with open("Usuarios.txt", "a") as file:
            file.write(f"{nombre}:{contraseña}:{correo}:{rol}\n")  # Asegurarse de agregar un salto de línea
            print(f"Usuario {nombre} guardado exitosamente.")
        return True

import datetime

class Medicamento:
    def __init__(self, id, nombre, dosis, frecuencia, fechaVencimiento, stock):
        self.id = id
        self.nombre = nombre
        self.dosis = dosis
        self.frecuencia = frecuencia
        self.fechaVencimiento = fechaVencimiento
        self.stock = stock

    def actualizarStock(self, cantidad):
        """
        Actualiza el stock del medicamento sumando la cantidad proporcionada.
        """
        self.stock += cantidad
        print(f"Stock actualizado. El nuevo stock de {self.nombre} es {self.stock}.")

    def verificarVencimiento(self):
        """
        Verifica si el medicamento está vencido.
        Retorna True si el medicamento está vencido, False si no.
        """
        hoy = datetime.date.today()
        if self.fechaVencimiento < hoy:
            print(f"El medicamento {self.nombre} está vencido.")
            return True
        else:
            print(f"El medicamento {self.nombre} no está vencido.")
            return False

    def cargarMedicamentosDesdeBD(self):
        """
        Carga los medicamentos desde una base de datos simulada.
        En este caso, simula la carga desde una lista de medicamentos.
        """
        # Simulando base de datos en una lista
        medicamentos = [
            {"id": 1, "nombre": "Paracetamol", "dosis": "500mg", "frecuencia": "Cada 8 horas", "fechaVencimiento": "2024-10-01", "stock": 100},
            {"id": 2, "nombre": "Ibuprofeno", "dosis": "200mg", "frecuencia": "Cada 6 horas", "fechaVencimiento": "2025-05-20", "stock": 50},
        ]
        
        # Convertir las fechas a objetos datetime.date para comparación
        for medicamento in medicamentos:
            medicamento["fechaVencimiento"] = datetime.datetime.strptime(medicamento["fechaVencimiento"], "%Y-%m-%d").date()
        
        return medicamentos

    def guardarMedicamentoEnBD(self, nombre, dosis, frecuencia, fechaVencimiento, stock):
        """
        Guarda un medicamento en la "base de datos".
        En este caso, simplemente imprime el medicamento y lo simula en una lista.
        """
        # Simulando la base de datos como una lista
        medicamento = {
            "id": len(self.cargarMedicamentosDesdeBD()) + 1,  # Asignar un nuevo ID
            "nombre": nombre,
            "dosis": dosis,
            "frecuencia": frecuencia,
            "fechaVencimiento": fechaVencimiento,
            "stock": stock
        }
        
        # Mostrar el medicamento guardado
        print(f"Medicamento guardado: {medicamento}")
        return medicamento
