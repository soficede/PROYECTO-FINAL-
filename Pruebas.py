from Modelo import Usuario

# def prueba_usuario():
#     # Instanciar la clase Usuario
#     usuario = Usuario("", "", "", "")
    
#     # Probar guardar un nuevo usuario
#     nombre = input("Introduce el nombre de usuario: ")
#     contraseña = input("Introduce la contraseña: ")
#     correo = input("Introduce el correo: ")
#     rol = input("Introduce el rol: ")
    
#     if usuario.guardarUsuario(nombre, contraseña, correo, rol):
#         print("Usuario guardado exitosamente.")
#     else:
#         print("No se pudo guardar el usuario.")
    
#     # Probar validar credenciales
#     nombre_validar = input("Introduce el nombre de usuario para validar: ")
#     contraseña_validar = input("Introduce la contraseña para validar: ")
    
#     if usuario.validarCredenciales(nombre_validar, contraseña_validar):
#         print("Credenciales válidas.")
#     else:
#         print("Credenciales inválidas.")
    
# # Ejecutar la prueba
# prueba_usuario()

# from Modelo import Medicamento
# from datetime import datetime

# def obtener_fecha():
#     while True:
#         fecha_str = input("Introduce la fecha de vencimiento del medicamento (YYYY-MM-DD): ")
#         try:
#             fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
#             if fecha < datetime.now().date():
#                 print("La fecha de vencimiento no puede ser en el pasado. Inténtalo de nuevo.")
#             else:
#                 return fecha
#         except ValueError:
#             print("Formato de fecha inválido. Debe ser en el formato YYYY-MM-DD. Inténtalo de nuevo.")

# def prueba_medicamento():
#     # Crear un medicamento con valores de prueba
#     nombre = input("Introduce el nombre del medicamento: ")
#     dosis = input("Introduce la dosis del medicamento: ")
#     frecuencia = input("Introduce la frecuencia del medicamento: ")
#     fecha_vencimiento = obtener_fecha()
#     while True:
#         try:
#             stock = int(input("Introduce el stock inicial del medicamento: "))
#             if stock < 0:
#                 print("El stock no puede ser negativo. Inténtalo de nuevo.")
#             else:
#                 break
#         except ValueError:
#             print("Por favor, ingresa un número válido para el stock.")

#     # Crear el objeto medicamento
#     medicamento = Medicamento(nombre=nombre, dosis=dosis, frecuencia=frecuencia, fechaVencimiento=fecha_vencimiento, stock=stock)
    
#     # Guardar medicamento en la base de datos
#     medicamento.guardarMedicamentoEnBD()

#     # Verificar si el medicamento está vencido
#     medicamento.verificarVencimiento()

#     # Buscar medicamento por ID
#     while True:
#         try:
#             medicamento_id = int(input("Introduce el ID del medicamento para buscarlo: "))
#             medicamento_encontrado = medicamento.buscarMedicamentoPorID(medicamento_id)
#             if medicamento_encontrado:
#                 print("Medicamento encontrado:", medicamento_encontrado)
#                 break
#             else:
#                 print("No se encontró el medicamento con ese ID.")
#                 break
#         except ValueError:
#             print("Por favor, ingresa un ID válido.")

#     # Actualizar stock
#     while True:
#         try:
#             cantidad = int(input(f"Introduce la cantidad para actualizar el stock de {nombre} (negativo para reducir): "))
#             if medicamento.actualizarStock(cantidad):
#                 break
#         except ValueError:
#             print("Por favor, ingresa un número válido para la cantidad.")

# # Ejecutar la prueba
# prueba_medicamento()

import mysql.connector
from datetime import datetime, timedelta

class Alerta:
    def __init__(self, id=None, tipo="", mensaje="", estado=False):
        self.id = id
        self.tipo = tipo
        self.mensaje = mensaje
        self.estado = estado

    def generarAlerta(self, medicamento):
        """Genera una alerta para el medicamento dependiendo de su tipo."""
        if medicamento.fechaVencimiento <= datetime.now().date():
            self.tipo = "Vencimiento"
            self.mensaje = f"Alerta: El medicamento {medicamento.nombre} ha vencido."
        elif medicamento.fechaVencimiento == datetime.now().date() + timedelta(days=1):
            self.tipo = "Vencimiento"
            self.mensaje = f"Alerta: El medicamento {medicamento.nombre} vence mañana."
        elif medicamento.stock <= 0:
            self.tipo = "Stock bajo"
            self.mensaje = f"Alerta: El medicamento {medicamento.nombre} está fuera de stock."
        else:
            self.tipo = "Recordatorio"
            self.mensaje = f"Alerta: Es hora de tomar el medicamento {medicamento.nombre}."

        self.estado = False  # La alerta es inicialmente no leída
        return self.guardarAlertaEnBD()

    def listarAlertas(self):
        """Lista todas las alertas almacenadas en la base de datos."""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alertas")
            alertas = cursor.fetchall()
            conexion.close()
            return alertas
        except mysql.connector.Error as err:
            print(f"Error al conectar con la base de datos: {err}")
            return []

    def marcarComoLeida(self):
        """Marca la alerta como leída en la base de datos."""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE alertas SET estado=%s WHERE id=%s",
                (True, self.id)
            )
            conexion.commit()
            conexion.close()
            print(f"Alerta {self.id} marcada como leída.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al marcar la alerta como leída: {err}")
            return False

    def guardarAlertaEnBD(self):
        """Guarda la alerta en la base de datos."""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO alertas (tipo, mensaje, estado) VALUES (%s, %s, %s)",
                (self.tipo, self.mensaje, self.estado)
            )
            conexion.commit()
            conexion.close()
            print(f"Alerta de tipo '{self.tipo}' guardada correctamente en la base de datos.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al guardar la alerta en la base de datos: {err}")
            return False
