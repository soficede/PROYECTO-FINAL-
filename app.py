from flask import Flask, render_template, request, redirect, url_for, flash
from Controlador import ControladorUsuario, ControladorMedicamento

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Ruta para la página de inicio
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para la página de inicio de sesión
@app.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if request.method == "POST":
        nombre = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        controlador = ControladorUsuario()
        
        if controlador.validar_usuario(nombre, contraseña):
            flash("Ingreso exitoso", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template("ingresar.html")

# Ruta para la página de registro
@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        correo = request.form.get("correo")
        rol = request.form.get("rol")
        
        controlador = ControladorUsuario()
        if controlador.registrar_usuario(nombre, contraseña, correo, rol):
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("ingresar"))
        else:
            flash("El usuario ya existe. Intenta con otro nombre.", "error")
    return render_template("registrarse.html")

# Ruta para el dashboard
@app.route("/dashboard", methods=["GET"])
def dashboard():
    controlador = ControladorMedicamento()
    medicamentos = controlador.listar_medicamentos()
    return render_template("usuario.html", medicamentos=medicamentos)

# Ruta para eliminar un medicamento
@app.route("/eliminar_medicamento", methods=["POST"])
def eliminar_medicamento():
    id_medicamento = request.form.get("id")
    controlador = ControladorMedicamento()
    if controlador.eliminar_medicamento(id_medicamento):
        flash("Medicamento eliminado exitosamente", "success")
    else:
        flash("Error al eliminar el medicamento", "error")
    return redirect(url_for("dashboard"))

# Ruta para agregar un medicamento
@app.route("/agregar_medicamento", methods=["POST"])
def agregar_medicamento():
    nombre = request.form.get("nombre")
    dosis = request.form.get("dosis")
    frecuencia = request.form.get("frecuencia")
    fecha_vencimiento = request.form.get("fecha_vencimiento")
    stock = int(request.form.get("stock"))

    controlador = ControladorMedicamento()
    if controlador.agregar_medicamento(nombre, dosis, frecuencia, fecha_vencimiento, stock):
        flash("Medicamento agregado exitosamente", "success")
    else:
        flash("Error al agregar el medicamento", "error")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
