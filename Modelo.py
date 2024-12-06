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

import mysql.connector
from datetime import datetime

class Medicamento:
    def __init__(self, id=None, nombre="", dosis="", frecuencia="", fechaVencimiento=None, stock=0):
        self.id = id
        self.nombre = nombre
        self.dosis = dosis
        self.frecuencia = frecuencia
        self.fechaVencimiento = fechaVencimiento
        self.stock = stock

    def actualizarStock(self, cantidad):
        """ Actualiza el stock del medicamento """
        if cantidad < 0 and abs(cantidad) > self.stock:
            print("No hay suficiente stock para reducir esa cantidad.")
            return False
        self.stock += cantidad
        return self.guardarMedicamentoEnBD()  # Guardar el medicamento con el stock actualizado

    def verificarVencimiento(self):
        """ Verifica si el medicamento está vencido """
        if self.fechaVencimiento < datetime.now().date():
            print(f"El medicamento {self.nombre} está vencido.")
            return True
        dias_restantes = (self.fechaVencimiento - datetime.now().date()).days
        print(f"El medicamento {self.nombre} vence en {dias_restantes} días.")
        return False

    def cargarMedicamentosDesdeBD(self):
        """ Carga todos los medicamentos desde la base de datos """
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM medicamentos")
            medicamentos = cursor.fetchall()
            conexion.close()
            return medicamentos
        except mysql.connector.Error as err:
            print(f"Error al conectar con la base de datos: {err}")
            return []

    def buscarMedicamentoPorID(self, medicamento_id):
        """ Busca un medicamento por su ID """
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM medicamentos WHERE id = %s", (medicamento_id,))
            medicamento = cursor.fetchone()
            conexion.close()
            return medicamento
        except mysql.connector.Error as err:
            print(f"Error al buscar medicamento: {err}")
            return None

    def guardarMedicamentoEnBD(self):
        """ Guarda o actualiza un medicamento en la base de datos """
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()
            
            if self.id is None:  # Si el medicamento no tiene ID, es un nuevo medicamento
                cursor.execute(
                    "INSERT INTO medicamentos (nombre, dosis, frecuencia, fecha_vencimiento, stock) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (self.nombre, self.dosis, self.frecuencia, self.fechaVencimiento, self.stock)
                )
            else:  # Si ya tiene ID, lo actualizamos
                cursor.execute(
                    "UPDATE medicamentos SET nombre=%s, dosis=%s, frecuencia=%s, fecha_vencimiento=%s, stock=%s "
                    "WHERE id=%s",
                    (self.nombre, self.dosis, self.frecuencia, self.fechaVencimiento, self.stock, self.id)
                )
            
            conexion.commit()
            conexion.close()
            print(f"Medicamento {self.nombre} guardado correctamente en la base de datos.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al guardar el medicamento: {err}")
            return False

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

