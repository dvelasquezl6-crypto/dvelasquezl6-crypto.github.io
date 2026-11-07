
# ============================================
# PRUEBA DEL MODELO ROL
# Consulta los roles existentes en SQL Server.
# ============================================

# Importamos nuestra aplicación Flask.
from app import app

# Importamos la conexión de SQLAlchemy.
from database import db

# Importamos el modelo Rol.
from models.rol import Rol


# Abrimos el contexto de nuestra aplicación.
with app.app_context():

    try:
        # Consultamos todos los roles registrados.
        consulta = db.select(Rol).order_by(Rol.id_rol)

        roles = db.session.execute(
            consulta
        ).scalars().all()

        # Mostramos el resultado en la terminal.
        print("============================")
        print("ROLES DEL SISTEMA")
        print("============================")

        for rol in roles:
            print(
                f"ID: {rol.id_rol} | "
                f"Nombre: {rol.nombre_rol}"
            )

        print("============================")
        print("Consulta realizada correctamente.")

    except Exception as error:
        # Mostramos el error si falla la consulta.
        print("Error al consultar los roles:")
        print(error)
