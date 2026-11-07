
# ============================================
# SISTEMA PICTOGRÁFICO INTERACTIVO
# PROTECCIÓN DE CONTRASEÑAS EXISTENTES
# ============================================

# Permite introducir contraseñas sin mostrarlas.
from getpass import getpass

# Herramientas para proteger y verificar contraseñas.
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Importamos nuestra aplicación y conexión.
from app import app
from database import db

# Importamos el modelo de usuarios.
from models.usuario import Usuario


# ============================================
# 1. FUNCIÓN PARA PROTEGER UNA CONTRASEÑA
# ============================================

def proteger_usuario(nombre_usuario):

    # Buscamos al usuario por su nombre.
    consulta = db.select(Usuario).filter_by(
        nombre_usuario=nombre_usuario
    )

    usuario = db.session.execute(
        consulta
    ).scalar_one_or_none()

    # Verificamos si existe.
    if usuario is None:
        print(f"No se encontró: {nombre_usuario}")
        return

    # Evitamos convertir nuevamente una contraseña
    # que ya está protegida mediante hash.
    if usuario.contrasena.startswith(
        ("scrypt:", "pbkdf2:")
    ):
        print(f"{nombre_usuario}: ya está protegido.")
        return

    # Solicitamos la contraseña actual sin mostrarla.
    clave_actual = getpass(
        f"Contraseña actual de {nombre_usuario}: "
    )

    # Verificamos la contraseña existente.
    if clave_actual != usuario.contrasena:
        print("La contraseña actual no coincide.")
        return

    # Generamos un hash seguro de la contraseña.
    nuevo_hash = generate_password_hash(clave_actual)

    # Comprobamos que cabe en VARCHAR(255).
    if len(nuevo_hash) > 255:
        print("El hash supera el tamaño del campo.")
        return

    # Verificamos que el hash generado es válido.
    if not check_password_hash(
        nuevo_hash, clave_actual
    ):
        print("No fue posible verificar el hash.")
        return

    # Sustituimos la contraseña original por su hash.
    usuario.contrasena = nuevo_hash

    # Guardamos el cambio en SQL Server.
    try:
        db.session.commit()
        print(f"{nombre_usuario}: contraseña protegida.")

    except Exception as error:
        db.session.rollback()
        print("Error al guardar los cambios:", error)


# ============================================
# 2. EJECUTAR LA MIGRACIÓN
# ============================================

# Utilizamos el contexto de Flask para acceder
# correctamente a la base de datos.
with app.app_context():

    print("=================================")
    print("PROTECCIÓN DE CONTRASEÑAS")
    print("=================================")

    # Protegemos los usuarios de prueba existentes.
    proteger_usuario("admin")
    proteger_usuario("alumno1")

    print("=================================")
    print("Proceso finalizado.")
