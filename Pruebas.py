from Modelo import Usuario

def prueba_usuario():
    # Instanciar la clase Usuario
    usuario = Usuario("", "", "", "")
    
    # Probar guardar un nuevo usuario
    nombre = input("Introduce el nombre de usuario: ")
    contraseña = input("Introduce la contraseña: ")
    correo = input("Introduce el correo: ")
    rol = input("Introduce el rol: ")
    
    if usuario.guardarUsuario(nombre, contraseña, correo, rol):
        print("Usuario guardado exitosamente.")
    else:
        print("No se pudo guardar el usuario.")
    
    # Probar validar credenciales
    nombre_validar = input("Introduce el nombre de usuario para validar: ")
    contraseña_validar = input("Introduce la contraseña para validar: ")
    
    if usuario.validarCredenciales(nombre_validar, contraseña_validar):
        print("Credenciales válidas.")
    else:
        print("Credenciales inválidas.")
    
# Ejecutar la prueba
prueba_usuario()
