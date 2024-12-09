from flask import Flask, render_template, request, redirect, url_for, flash
import os
from Modelo import Usuario, Medicamento, Alerta  # Asegúrate de que Modelo.py esté en el mismo directorio

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave para manejar sesiones y flash messages

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el registro de usuarios
@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        rol = request.form['rol']
        usuario = Usuario(nombre, correo, contraseña, rol)
        if usuario.guardarUsuario(nombre, contraseña, correo, rol):
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('ingresar'))
        else:
            flash('El usuario ya existe o hubo un error.', 'danger')
    return render_template('registrarse.html')

# Ruta para manejar el login de usuarios
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        usuario = Usuario("", "", "", "")
        if usuario.validarCredenciales(nombre, contraseña):
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    return render_template('ingresar.html')

# Ruta del dashboard del usuario
@app.route('/dashboard')
def dashboard():
    medicamentos = Medicamento().cargarMedicamentosDesdeBD()
    return render_template('usuario.html', medicamentos=medicamentos)

# Ruta para gestionar medicamentos
@app.route('/agregar_medicamento', methods=['POST'])
def agregar_medicamento():
    nombre = request.form['nombre']
    dosis = request.form['dosis']
    frecuencia = request.form['frecuencia']
    fecha_vencimiento = request.form['fecha_vencimiento']
    stock = int(request.form['stock'])

    medicamento = Medicamento(nombre=nombre, dosis=dosis, frecuencia=frecuencia, 
                              fechaVencimiento=fecha_vencimiento, stock=stock)
    if medicamento.guardarMedicamentoEnBD():
        flash('Medicamento agregado exitosamente.', 'success')
    else:
        flash('Error al agregar medicamento.', 'danger')
    return redirect(url_for('dashboard'))

# Inicia la aplicación
if __name__ == '__main__':
    app.run(debug=True)

