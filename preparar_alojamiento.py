"""Crear tablas, catálogo visual y una cuenta nueva en la copia de alojamiento."""
from datetime import datetime
from getpass import getpass
from pathlib import Path
from werkzeug.security import generate_password_hash

from pythonanywhere_app import application
from database import db
from models.rol import Rol
from models.usuario import Usuario
from models.categoria import Categoria
from models.pictograma import Pictograma
from migraciones.preparar_actividades_catalogo import preparar


CATALOGO = {
    "Necesidades básicas": [("Tengo sed", "tengo_sed"), ("Tengo hambre", "tengo_hambre"),
                            ("Quiero ir al baño", "ir_bano"), ("Quiero descansar", "descansar")],
    "Emociones": [("Estoy feliz", "feliz"), ("Estoy triste", "triste"),
                  ("Estoy enojado", "enojado"), ("Tengo miedo", "miedo")],
    "Rutinas": [("Lavarse las manos", "lavar-manos"), ("Cepillarse los dientes", "cepillar-dientes"),
                ("Vestirse", "vestirse"), ("Ir a la escuela", "ir-escuela")],
    "Objetos": [("Pelota", "pelota"), ("Libro", "libro"), ("Lápiz", "lapiz"), ("Mochila", "mochila")],
}


def inicializar(clave=None):
    with application.test_request_context():
        db.create_all()
        roles = {r.nombre_rol: r for r in db.session.scalars(db.select(Rol))}
        for nombre in ("Administrador", "Alumno"):
            if nombre not in roles:
                roles[nombre] = Rol(nombre_rol=nombre)
                db.session.add(roles[nombre])
        db.session.flush()
        admin = db.session.scalar(db.select(Usuario.id_usuario).where(
            Usuario.id_rol == roles["Administrador"].id_rol).limit(1))
        if admin is None:
            if clave is None:
                clave = getpass("Nueva contraseña de admin_demo (6 a 15 caracteres): ")
                if clave != getpass("Confirma la contraseña: "):
                    raise SystemExit("Las contraseñas no coinciden.")
            if not 6 <= len(clave) <= 15 or not clave.strip():
                raise SystemExit("La contraseña debe tener entre 6 y 15 caracteres.")
            db.session.add(Usuario(nombre="Administrador", apellido="Demo", nombre_usuario="admin_demo",
                contrasena=generate_password_hash(clave), id_rol=roles["Administrador"].id_rol,
                estado=True, fecha_registro=datetime.now()))
        for nombre, items in CATALOGO.items():
            categoria = db.session.scalar(db.select(Categoria).where(Categoria.nombre_categoria == nombre))
            if categoria is None:
                categoria = Categoria(nombre_categoria=nombre, estado=True)
                db.session.add(categoria)
                db.session.flush()
            for titulo, archivo in items:
                ruta = f"img/pictogramas/{archivo}-v1.png"
                if not (Path(application.static_folder) / ruta).is_file():
                    raise RuntimeError(f"No se encuentra la imagen {ruta}")
                if db.session.scalar(db.select(Pictograma.id_pictograma).where(
                        Pictograma.id_categoria == categoria.id_categoria, Pictograma.nombre == titulo)) is None:
                    db.session.add(Pictograma(id_categoria=categoria.id_categoria, nombre=titulo,
                                              imagen=ruta, estado=True))
        # La preparación de ejercicios confirma el catálogo y el administrador
        # en la misma transacción. No se importan usuarios de SQL Server.
        preparar()


if __name__ == "__main__":
    inicializar()
    print("Copia preparada. En la primera instalación el usuario es admin_demo.")
