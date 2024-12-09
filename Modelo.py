from datetime import datetime, timedelta
import mysql.connector

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

class Medicamento:
    def __init__(self, id=None, nombre="", dosis="", frecuencia="", fechaVencimiento=None, stock=0, fechaDeIngreso=None):
        self.id = id
        self.nombre = nombre
        self.dosis = dosis
        self.frecuencia = frecuencia
        self.fechaVencimiento = fechaVencimiento
        self.stock = stock
        self.fechaDeIngreso = fechaDeIngreso if fechaDeIngreso else datetime.now().date()  # Asignar la fecha de ingreso si no se pasa

    def actualizarStock(self, cantidad):
        """ Actualiza el stock del medicamento """
        if cantidad < 0 and abs(cantidad) > self.stock:
            print("No hay suficiente stock para reducir esa cantidad.")
            return False
        self.stock += cantidad
        if self.stock <= 0:
            self.eliminarMedicamento()  # Si el stock es 0 o negativo, eliminar el medicamento
        else:
            return self.guardarMedicamentoEnBD()  # Guardar el medicamento con el stock actualizado
        return True

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
                    "INSERT INTO medicamentos (nombre, dosis, frecuencia, fecha_vencimiento, stock, fecha_ingreso) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (self.nombre, self.dosis, self.frecuencia, self.fechaVencimiento, self.stock, self.fechaDeIngreso)
                )
            else:  # Si ya tiene ID, lo actualizamos
                cursor.execute(
                    "UPDATE medicamentos SET nombre=%s, dosis=%s, frecuencia=%s, fecha_vencimiento=%s, stock=%s, fecha_ingreso=%s "
                    "WHERE id=%s",
                    (self.nombre, self.dosis, self.frecuencia, self.fechaVencimiento, self.stock, self.fechaDeIngreso, self.id)
                )

            conexion.commit()
            conexion.close()
            print(f"Medicamento {self.nombre} guardado correctamente en la base de datos.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al guardar el medicamento: {err}")
            return False

    def eliminarMedicamento(self):
        """ Elimina un medicamento de la base de datos """
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM medicamentos WHERE id = %s", (self.id,))
            conexion.commit()
            conexion.close()
            print(f"Medicamento {self.nombre} eliminado de la base de datos debido a stock cero.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al eliminar el medicamento: {err}")
            return False

    def modificarMedicamento(self, nombre=None, dosis=None, frecuencia=None, fechaVencimiento=None, stock=None, fechaDeIngreso=None):
        """ Modifica un medicamento existente en la base de datos """
        if nombre:
            self.nombre = nombre
        if dosis:
            self.dosis = dosis
        if frecuencia:
            self.frecuencia = frecuencia
        if fechaVencimiento:
            self.fechaVencimiento = fechaVencimiento
        if stock is not None:
            self.stock = stock
        if fechaDeIngreso:
            self.fechaDeIngreso = fechaDeIngreso  # Actualizar la fecha de ingreso si se pasa un valor

        return self.guardarMedicamentoEnBD()  # Guardar los cambios realizados

class Alerta:
    def __init__(self, id=None, tipo="", mensaje="", estado=False):
        self.id = id
        self.tipo = tipo
        self.mensaje = mensaje
        self.estado = estado

    def generarAlerta(self):
        """Genera alertas basadas en la frecuencia y fecha de vencimiento de los medicamentos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)

            # Obtener medicamentos
            cursor.execute("SELECT * FROM medicamentos")
            medicamentos = cursor.fetchall()

            # Obtener la fecha actual
            fecha_actual = datetime.now()

            for medicamento in medicamentos:
                # Verificar vencimiento
                fecha_vencimiento = medicamento['fecha_vencimiento']
                
                if fecha_vencimiento < fecha_actual.date():
                    # Si el medicamento ya está vencido, crear una alerta de vencimiento
                    mensaje = f"El medicamento {medicamento['nombre']} ha vencido. Fecha de vencimiento: {fecha_vencimiento}"
                    self.crearAlerta("Vencimiento", mensaje)
                    # Si ya está vencido, no verificamos la frecuencia de la toma
                    continue

                # Verificar frecuencia para la toma del medicamento
                ultima_toma = medicamento['frecuencia']  # Frecuencia en horas (en la base de datos)
                frecuencia_toma = timedelta(hours=int(ultima_toma))  # Convertir la frecuencia a un objeto timedelta
                
                # Usamos la fecha actual para comprobar si es hora de tomar el medicamento
                ultima_toma_datetime = datetime.combine(fecha_vencimiento, datetime.min.time())  # Combinamos fecha_vencimiento con hora 00:00:00
                proxima_toma = ultima_toma_datetime + frecuencia_toma

                if proxima_toma <= fecha_actual:
                    # Crear alerta para tomar medicamento
                    mensaje = f"Es hora de tomar el medicamento {medicamento['nombre']}. Última toma: {ultima_toma_datetime}, próxima toma: {proxima_toma}"
                    self.crearAlerta("Tomar Medicamento", mensaje)

            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error al generar alerta: {err}")

    def crearAlerta(self, tipo, mensaje):
        """Crea una alerta en la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()

            # Insertar alerta en la tabla alertas
            cursor.execute(
                "INSERT INTO alertas (tipo, mensaje, estado) VALUES (%s, %s, %s)",
                (tipo, mensaje, False)
            )
            conexion.commit()
            conexion.close()
            print(f"Alerta generada: {mensaje}")
        except mysql.connector.Error as err:
            print(f"Error al crear alerta: {err}")

    def listarAlertas(self):
        """Lista todas las alertas en la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)

            # Obtener todas las alertas
            cursor.execute("SELECT * FROM alertas")
            alertas = cursor.fetchall()
            conexion.close()

            for alerta in alertas:
                estado = "Leída" if alerta['estado'] else "No Leída"
                print(f"ID: {alerta['id']}, Tipo: {alerta['tipo']}, Mensaje: {alerta['mensaje']}, Estado: {estado}")
        except mysql.connector.Error as err:
            print(f"Error al listar alertas: {err}")

    def marcarComoLeida(self, alerta_id):
        """Marca una alerta como leída en la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()

            # Actualizar el estado de la alerta a leída
            cursor.execute(
                "UPDATE alertas SET estado = TRUE WHERE id = %s", (alerta_id,)
            )
            conexion.commit()
            conexion.close()
            print(f"Alerta {alerta_id} marcada como leída.")
        except mysql.connector.Error as err:
            print(f"Error al marcar la alerta como leída: {err}")

    def eliminarAlerta(self, alerta_id):
        """Elimina una alerta de la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()

            # Eliminar la alerta de la base de datos
            cursor.execute("DELETE FROM alertas WHERE id = %s", (alerta_id,))
            conexion.commit()
            conexion.close()
            print(f"Alerta {alerta_id} eliminada de la base de datos.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar la alerta: {err}")

from datetime import datetime, timedelta
import mysql.connector

class SeguimientoMedicamento:
    def __init__(self, medicamento_id, fecha_ingreso, frecuencia, stock):
        self.medicamento_id = medicamento_id
        self.fecha_ingreso = fecha_ingreso
        self.frecuencia = frecuencia  # frecuencia en horas
        self.stock = stock
        self.nombre = ""
        self.fecha_final = None
        self.stock_final = None

        self.obtenerDetallesMedicamento()

    def obtenerDetallesMedicamento(self):
        """ Obtiene los detalles del medicamento de la base de datos """
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT nombre FROM medicamentos WHERE id = %s", (self.medicamento_id,))
            medicamento = cursor.fetchone()
            if medicamento:
                self.nombre = medicamento['nombre']
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error al obtener detalles del medicamento: {err}")

    def calcularDuracionStock(self):
        """ Calcula cuántos días puede durar el medicamento basado en la frecuencia y stock """
        try:
            # La frecuencia está en horas, por lo que necesitamos saber cuántas tomas se hacen al día.
            tomas_por_dia = 24 / self.frecuencia  # Por ejemplo, si la frecuencia es 8, serán 3 tomas al día

            # Duración en días
            duracion_dias = self.stock / tomas_por_dia

            # Calculamos la fecha final
            self.fecha_final = self.fecha_ingreso + timedelta(days=duracion_dias)

            # El stock final será 0, ya que hemos calculado que se consume todo el stock
            self.stock_final = 0

            return self.fecha_final, self.stock_final
        except Exception as e:
            print(f"Error al calcular la duración del stock: {e}")
            return None, None

    def guardarSeguimientoEnBD(self):
        """ Guarda el seguimiento del medicamento en la base de datos """
        try:
            # Calculamos la duración del stock
            fecha_final, stock_final = self.calcularDuracionStock()

            if fecha_final is None:
                print("No se pudo calcular la fecha final del seguimiento.")
                return False

            # Conectamos a la base de datos
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor()

            # Insertamos el seguimiento en la tabla seguimiento_medicamentos
            cursor.execute(
                "INSERT INTO seguimiento_medicamentos (medicamento_id, fecha_inicio, fecha_final, stock_final, frecuencia) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.medicamento_id, self.fecha_ingreso, fecha_final, stock_final, self.frecuencia)
            )

            conexion.commit()
            conexion.close()

            print(f"Seguimiento para {self.nombre} guardado correctamente.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al guardar el seguimiento en la base de datos: {err}")
            return False

    def verSeguimientos(self, medicamento_id=None):
        """
        Busca y lista los seguimientos de medicamentos en la base de datos.
        Si se pasa un medicamento_id, devuelve solo los seguimientos de ese medicamento.
        Si no, devuelve todos los seguimientos.
        """
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="admin_farmacia",
                password="contraseña_segura_123",
                database="gestion_medicamentos"
            )
            cursor = conexion.cursor(dictionary=True)

            if medicamento_id:
                # Buscar seguimientos de un medicamento específico
                cursor.execute(
                    "SELECT sm.*, m.nombre FROM seguimiento_medicamentos sm "
                    "JOIN medicamentos m ON sm.medicamento_id = m.id "
                    "WHERE sm.medicamento_id = %s", (medicamento_id,)
                )
            else:
                # Buscar todos los seguimientos
                cursor.execute(
                    "SELECT sm.*, m.nombre FROM seguimiento_medicamentos sm "
                    "JOIN medicamentos m ON sm.medicamento_id = m.id"
                )

            seguimientos = cursor.fetchall()
            conexion.close()

            # Mostrar seguimientos
            if not seguimientos:
                print("No se encontraron seguimientos.")
                return

            for seguimiento in seguimientos:
                print(f"ID Seguimiento: {seguimiento['id']}")
                print(f"Medicamento: {seguimiento['nombre']} (ID: {seguimiento['medicamento_id']})")
                print(f"Fecha de Inicio: {seguimiento['fecha_inicio']}")
                print(f"Fecha Final: {seguimiento['fecha_final']}")
                print(f"Stock Final: {seguimiento['stock_final']}")
                print(f"Frecuencia: Cada {seguimiento['frecuencia']} horas")
                print("-" * 40)
        except mysql.connector.Error as err:
            print(f"Error al buscar seguimientos: {err}")



