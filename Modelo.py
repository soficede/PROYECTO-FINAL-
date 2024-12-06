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
