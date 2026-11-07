"""Preparación manual de una base vacía y una cuenta administrativa propia."""
from datetime import datetime
from getpass import getpass
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash
from app import app, create_app
from database import db
from configuracion_demo import NOMBRE_BASE_DEMO, opciones_demo
from models.rol import Rol
from models.usuario import Usuario


def preparar():
    print("Se preparará SistemaPictograficoDemo sin copiar alumnos ni historial.")
    clave = getpass("Contraseña nueva para admin_demo (6 a 15 caracteres): ")
    confirmar = getpass("Confirma la contraseña: ")
    if not 6 <= len(clave) <= 15 or not clave.strip() or clave != confirmar:
        raise SystemExit("Contraseña inválida o confirmación diferente. No se realizaron cambios.")
    # Crear únicamente una base de nombre fijo, sin borrar o restaurar datos.
    with app.app_context(), db.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conexion:
        existe = conexion.execute(text("SELECT DB_ID(:nombre)"), {"nombre": NOMBRE_BASE_DEMO}).scalar()
        if existe is None:
            conexion.execute(text("CREATE DATABASE [SistemaPictograficoDemo]"))
    demo = create_app(opciones_demo())
    with demo.app_context():
        # Nunca reinicializar una demostración que ya contenga información.
        if inspect(db.engine).has_table("Usuarios", schema="dbo"):
            raise SystemExit("La base demo ya fue preparada. No se borró ni cambió su información.")
        db.create_all()
        try:
            admin = Rol(nombre_rol="Administrador")
            db.session.add_all([admin, Rol(nombre_rol="Alumno")])
            db.session.flush()
            db.session.add(Usuario(nombre="Administrador", apellido="Demo", nombre_usuario="admin_demo",
                contrasena=generate_password_hash(clave), id_rol=admin.id_rol,
                estado=True, fecha_registro=datetime.now()))
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
    print("Demostración preparada. Usuario: admin_demo. No se copiaron alumnos ni contraseñas existentes.")


if __name__ == "__main__":
    preparar()
