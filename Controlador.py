
from flask import Flask, render_template, request, redirect, url_for, flash
from Modelo import Usuario, Medicamento, Alerta

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para registrar un usuario
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

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
