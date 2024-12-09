from flask import Flask, render_template, request, redirect, url_for, flash
from Controlador import ControladorUsuario

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Ruta para la página de inicio de sesión
@app.route("/", methods=["GET", "POST"])
def ingresar():
    if request.method == "POST":
        nombre = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        controlador = ControladorUsuario()
        
        if controlador.validar_usuario(nombre, contraseña):
            flash("Ingreso exitoso", "success")
            return redirect(url_for("dashboard"))  # Cambia 'dashboard' por tu siguiente vista
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template("ingresar.html")

# Ruta para la siguiente página después del login
@app.route("/dashboard")
def dashboard():
    return "Bienvenido al Sistema de Gestión y Seguimiento de Medicamentos"

if __name__ == "__main__":
    app.run(debug=True)


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

# Ruta para iniciar sesión
@app.route("/", methods=["GET", "POST"])
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

# Ruta para el dashboard (próxima vista después de registro o inicio de sesión)
@app.route("/dashboard")
def dashboard():
    return "Bienvenido al Sistema de Gestión y Seguimiento de Medicamentos"

if __name__ == "__main__":
    app.run(debug=True)