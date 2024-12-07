from flask import Flask, render_template, request, redirect, url_for, flash
from Modelo import Usuario, Medicamento, Alerta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conexión a la base de datos (configuración inicial)
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="admin_farmacia",
        password="contraseña_segura_123",
        database="gestion_medicamentos"
    )

# Ruta para la página principal (Dashboard)
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para registrar un nuevo usuario
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        rol = request.form['rol']
        usuario = Usuario("", "", "", "")
        if usuario.guardarUsuario(nombre, contraseña, correo, rol):
            flash("Usuario registrado con éxito.", "success")
        else:
            flash("Error: el usuario ya existe.", "danger")
        return redirect(url_for('home'))
    return render_template('registrar.html')

# Ruta para gestionar medicamentos
@app.route('/medicamentos')
def medicamentos():
    medicamento = Medicamento()
    lista_medicamentos = medicamento.cargarMedicamentosDesdeBD()
    return render_template('medicamentos.html', medicamentos=lista_medicamentos)

# Ruta para generar y listar alertas
@app.route('/alertas')
def alertas():
    alerta = Alerta()
    alerta.generarAlerta()  # Genera las alertas basadas en vencimientos y frecuencia
    alertas_lista = alerta.listarAlertas()  # Devuelve una lista de alertas
    return render_template('alertas.html', alertas=alertas_lista)

# Ruta para gestionar el seguimiento de medicamentos
@app.route('/seguimiento')
def seguimiento():
    # Aquí puedes integrar la lógica de seguimiento que desees, por ejemplo, obteniendo datos de seguimiento.
    # A continuación, simulo una lista de seguimiento para que puedas visualizarla.
    seguimiento_lista = [
        {"medicamento": "Paracetamol", "horaUltimaDosis": "2024-12-05 08:00", "proximaDosis": "2024-12-05 12:00"},
        {"medicamento": "Ibuprofeno", "horaUltimaDosis": "2024-12-04 14:00", "proximaDosis": "2024-12-04 18:00"}
    ]
    return render_template('seguimiento.html', seguimientos=seguimiento_lista)

if __name__ == '__main__':
    app.run(debug=True)
