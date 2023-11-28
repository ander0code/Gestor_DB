import bcrypt

def encriptar_contrasena(contrasena):
    contrasena_encoded = contrasena.encode('utf-8')
    hashed = bcrypt.hashpw(contrasena_encoded, bcrypt.gensalt())
    return hashed

def verificar_contrasena(contrasena, hashed):
    contrasena_encoded = contrasena.encode('utf-8')
    return bcrypt.checkpw(contrasena_encoded, hashed)

# Ejemplo de uso
contrasena_original = "123"

# Encriptar la contraseña
contrasena_encriptada = encriptar_contrasena(contrasena_original)
print("Contraseña encriptada:", contrasena_encriptada)

# Verificar la contraseña
contrasena_ingresada = "123"
es_correcta = verificar_contrasena(contrasena_ingresada, contrasena_encriptada)
print("¿La contraseña es correcta?", es_correcta)

