from flask import Flask, render_template, request, redirect, url_for, flash
from Controlador import ControladorUsuario, ControladorMedicamento

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Instancias de los controladores
controlador_usuario = ControladorUsuario()
controlador_medicamento = ControladorMedicamento()

# Ruta para la página principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para el dashboard del usuario
@app.route("/usuario")
def usuario():
    medicamentos = controlador_medicamento.listar_medicamentos()
    return render_template("usuario.html", medicamentos=medicamentos)

# Ruta para agregar un medicamento
@app.route("/agregar_medicamento", methods=["GET", "POST"])
def agregar_medicamento():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        dosis = request.form.get("dosis")
        frecuencia = request.form.get("frecuencia")
        fecha_vencimiento = request.form.get("fecha_vencimiento")
        stock = request.form.get("stock")
        controlador_medicamento.agregar_medicamento(nombre, dosis, frecuencia, fecha_vencimiento, stock)
        flash("Medicamento agregado exitosamente.", "success")
        return redirect(url_for("usuario"))
    return render_template("agregar_medicamento.html")

# Ruta para eliminar un medicamento
@app.route("/eliminar_medicamento", methods=["POST"])
def eliminar_medicamento():
    medicamento_id = request.form.get("id")
    controlador_medicamento.eliminar_medicamento(medicamento_id)
    flash("Medicamento eliminado exitosamente.", "success")
    return redirect(url_for("usuario"))

# Ruta para modificar un medicamento
@app.route("/modificar_medicamento", methods=["GET", "POST"])
def modificar_medicamento():
    # Implementación similar a agregar con cambios específicos
    return "Vista para modificar medicamento"

# Ruta para actualizar stock
@app.route("/actualizar_stock", methods=["GET", "POST"])
def actualizar_stock():
    # Implementación para actualizar stock
    return "Vista para actualizar stock"

if __name__ == "__main__":
    app.run(debug=True)
