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

from Modelo import Alerta

def prueba_alerta():
    # Crear objeto Alerta
    alerta = Alerta()

    # Generar alertas basadas en la frecuencia y fecha de vencimiento
    alerta.generarAlerta()

    # Listar todas las alertas generadas
    alerta.listarAlertas()

    # Marcar una alerta como leída
    alerta_id = int(input("Introduce el ID de la alerta que quieres marcar como leída: "))
    alerta.marcarComoLeida(alerta_id)

# Ejecutar la prueba
prueba_alerta()

