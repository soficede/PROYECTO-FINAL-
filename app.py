from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from Controlador import ControladorUsuario, ControladorMedicamento, ControladorSeguimiento  # Importar ControladorSeguimiento
from Modelo import Alerta
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret_key"  # Para usar mensajes flash

# Instancia de los controladores
controlador_usuario = ControladorUsuario()
controlador_medicamento = ControladorMedicamento()
controlador_seguimiento = ControladorSeguimiento()  # Instancia del controlador de seguimiento

# Ruta principal
@app.route('/')
def index():
    alerta_obj = Alerta()
    alerta_obj.generarYCrearAlerta()  # Genera las alertas pertinentes al ingresar
    alertas = alerta_obj.listarAlertas()
    return render_template('index.html', alertas=alertas)

# Ruta para el archivo UML
@app.route('/Archivos/UML.html')
def abrir_uml():
    return send_from_directory(os.path.join(app.root_path, 'Archivos'), 'UML.html')

# Ruta para el archivo Informe.pdf
@app.route('/Archivos/Informe.pdf')
def abrir_informe():
    return send_from_directory(os.path.join(app.root_path, 'Archivos'), 'Informe.pdf')

# Ruta para el archivo Manual.pdf
@app.route('/Archivos/Manual.pdf')
def abrir_manual():
    return send_from_directory(os.path.join(app.root_path, 'Archivos'), 'Manual.pdf')

# Rutas para otros manejos
@app.route('/ingresar')
def ingresar():
    return render_template('ingresar.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

@app.route('/validar', methods=['POST'])
def validar():
    nombre = request.form['nombre']
    contraseña = request.form['contraseña']
    if controlador_usuario.validar_credenciales(nombre, contraseña):
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('usuario'))
    else:
        flash('Credenciales inválidas', 'error')
        return redirect(url_for('ingresar'))

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    contraseña = request.form['contraseña']
    correo = request.form['correo']
    rol = request.form['rol']
    if controlador_usuario.registrar_usuario(nombre, contraseña, correo, rol):
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('usuario'))
    else:
        flash('El usuario ya existe', 'error')
        return redirect(url_for('registrarse'))

@app.route('/usuario')
def usuario():
    medicamentos = controlador_medicamento.obtener_medicamentos()
    alerta_obj = Alerta()
    alertas = alerta_obj.listarAlertas()  # Obtener las alertas
    seguimientos = controlador_seguimiento.obtener_seguimientos()
    return render_template('usuario.html', medicamentos=medicamentos, alertas=alertas, seguimientos=seguimientos)

@app.route('/agregar_medicamento', methods=['POST'])
def agregar_medicamento():
    nombre = request.form['nombre']
    dosis = request.form['dosis']
    frecuencia = request.form['frecuencia']
    fecha_vencimiento = request.form['fecha_vencimiento']
    stock = request.form['stock']
    if controlador_medicamento.agregar_medicamento(nombre, dosis, frecuencia, fecha_vencimiento, stock):
        flash('Medicamento agregado correctamente', 'success')
        return redirect(url_for('usuario'))
    else:
        flash('Error al agregar el medicamento', 'error')
        return redirect(url_for('usuario'))

@app.route('/eliminar_medicamento/<int:id>', methods=['GET'])
def eliminar_medicamento(id):
    if controlador_medicamento.eliminar_medicamento(id):
        flash('Medicamento eliminado correctamente', 'success')
    else:
        flash('Error al eliminar el medicamento', 'error')
    return redirect(url_for('usuario'))

@app.route('/editar_medicamento/<int:id>', methods=['GET', 'POST'])
def editar_medicamento(id):
    medicamento = controlador_medicamento.obtener_medicamento_por_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        dosis = request.form['dosis']
        frecuencia = request.form['frecuencia']
        fecha_vencimiento = request.form['fecha_vencimiento']
        stock = request.form['stock']
        if controlador_medicamento.editar_medicamento(id, nombre, dosis, frecuencia, fecha_vencimiento, stock):
            flash('Medicamento editado correctamente', 'success')
            return redirect(url_for('usuario'))
        else:
            flash('Error al editar el medicamento', 'error')
            return redirect(url_for('usuario'))
    return render_template('editar_medicamento.html', medicamento=medicamento)

# Nuevas rutas para gestionar el seguimiento de medicamentos
@app.route('/agregar_seguimiento', methods=['POST'])
def agregar_seguimiento():
    medicamento_id = request.form['medicamento_id']
    fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d')
    frecuencia = int(request.form['frecuencia'])
    stock = int(request.form['stock'])

    if controlador_seguimiento.crear_seguimiento(medicamento_id, fecha_ingreso, frecuencia, stock):
        flash('Seguimiento agregado correctamente', 'success')
        return redirect(url_for('usuario'))
    else:
        flash('Error al agregar el seguimiento', 'error')
        return redirect(url_for('usuario'))

@app.route('/seguimientos')
def seguimientos():
    # Obtenemos todos los seguimientos o de un medicamento específico
    medicamento_id = request.args.get('medicamento_id', None)
    seguimientos = controlador_seguimiento.obtener_seguimientos(medicamento_id)
    
    return render_template('seguimientos.html', seguimientos=seguimientos)

# Rutas para manejar la alerta
@app.route('/marcar_alerta_leida/<int:alerta_id>')
def marcar_alerta_leida(alerta_id):
    alerta_obj = Alerta()
    alerta_obj.marcarComoLeida(alerta_id)  # Marca la alerta como leída
    return redirect(url_for('usuario'))  # Redirige a la vista de usuario

@app.route('/eliminar_alerta/<int:alerta_id>')
def eliminar_alerta(alerta_id):
    alerta_obj = Alerta()
    alerta_obj.eliminarAlerta(alerta_id)  # Elimina la alerta
    return redirect(url_for('usuario'))  # Redirige a la vista de usuario

if __name__ == '__main__':
    app.run(debug=True)
