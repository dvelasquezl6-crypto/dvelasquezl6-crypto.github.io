
# ==========================================
# SISTEMA PICTOGRÁFICO INTERACTIVO
# ARCHIVO: app.py
# ARCHIVO PRINCIPAL DE FLASK
# ==========================================

# ==========================================
# 1. IMPORTACIONES
# ==========================================

from flask import (
    Flask,
    flash,
    g,
    render_template,
    session,
    redirect,
    url_for
)

# Protección de formularios.
from flask_wtf.csrf import CSRFProtect, CSRFError
from pathlib import Path

# Configuración y base de datos.
from config import Config
from database import db

# Rutas del sistema.
from routes.login import login_bp
from routes.admin import admin_bp
from routes.alumno import alumno_bp
from routes.alumnos import alumnos_bp
from routes.categorias import categorias_bp
from routes.pictogramas import pictogramas_bp
from routes.actividades import actividades_bp
from routes.progreso import progreso_bp
from routes.ejercicios import ejercicios_bp
from routes.rutinas import rutinas_bp
from routes.cuenta import cuenta_bp


# ==========================================
# 2. PROTECCIÓN CSRF
# ==========================================

csrf = CSRFProtect()


# ==========================================
# 3. CREAR LA APLICACIÓN
# ==========================================

def create_app(configuracion=None):

    app = Flask(__name__)

    # Cargamos la configuración.
    app.config.from_object(Config)

    # Permite probar los módulos con una base aislada, sin tocar SQL Server.
    if configuracion:
        app.config.update(configuracion)

    # Los archivos se crean aquí únicamente cuando se guarda una subida válida.
    app.config.setdefault("PICTOGRAMAS_UPLOAD_DIR", str(Path(app.static_folder) / "uploads" / "pictogramas"))

    # La copia de alojamiento usa SQLite y traduce el esquema dbo. La
    # instalación local conserva su conexión y esquema originales de SQL Server.
    from sqlalchemy.engine import make_url
    if make_url(app.config["SQLALCHEMY_DATABASE_URI"]).get_backend_name() == "sqlite":
        app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {}).setdefault(
            "execution_options", {"schema_translate_map": {"dbo": None}})

    # Inicializamos SQLAlchemy.
    db.init_app(app)

    # Activamos la protección de formularios.
    csrf.init_app(app)

    # Un formulario antiguo puede sobrevivir al cierre de sesión, a un cambio
    # de cuenta en otra pestaña o al reinicio con una clave distinta. Se rechaza
    # el POST y se muestra el login con un token nuevo; nunca se reenvían datos.
    @app.errorhandler(CSRFError)
    def recuperar_formulario(error):
        g.pop("csrf_token", None)
        # Registrar solo el motivo permite diagnosticar cookies o formularios
        # antiguos sin escribir contraseñas ni tokens en el registro del servidor.
        app.logger.info("Formulario rechazado por CSRF: %s", error.description)
        flash("El formulario venció o la sesión cambió. Ingresa tus datos nuevamente. Si vuelve a ocurrir, permite las cookies y utiliza siempre la misma dirección del sistema.")
        return render_template("login.html"), 400

    # Evita reutilizar desde la caché formularios con tokens de otra sesión.
    @app.after_request
    def proteger_cache_formularios(respuesta):
        if respuesta.mimetype == "text/html":
            respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    @app.errorhandler(413)
    def archivo_demasiado_grande(error):
        # La petición se rechaza antes de guardar archivos o registros.
        flash("Los archivos superan el límite total de 12 MB. Utiliza archivos de hasta 5 MB cada uno.")
        return render_template("login.html"), 413

    # ======================================
    # 4. REGISTRAR BLUEPRINTS
    # ======================================

    app.register_blueprint(login_bp)
    app.register_blueprint(rutinas_bp)
    app.register_blueprint(cuenta_bp)

    @app.context_processor
    def identidad_cuenta():
        # Nombre y avatar se leen de la cuenta real, no de campos del navegador.
        from models.usuario import Usuario
        usuario = db.session.get(Usuario, session["usuario_id"]) if session.get("usuario_id") else None
        if usuario and usuario.estado:
            return dict(identidad_nombre=f"{usuario.nombre} {usuario.apellido}".strip(),
                        identidad_iniciales=((usuario.nombre[:1] or "") + (usuario.apellido[:1] or "")).upper())
        return dict(identidad_nombre="Administrador", identidad_iniciales="AD")

    app.register_blueprint(admin_bp)

    app.register_blueprint(alumno_bp)

    # Registramos la gestión de alumnos.
    app.register_blueprint(alumnos_bp)

    # Gestión de categorías, protegida para administradores.
    app.register_blueprint(categorias_bp)

    # Gestión de pictogramas y recursos multimedia.
    app.register_blueprint(pictogramas_bp)

    # Administración de módulos y actividades que consulta el panel del alumno.
    app.register_blueprint(actividades_bp)

    # Escrituras del alumno y consultas administrativas del seguimiento.
    app.register_blueprint(progreso_bp)

    # Configuración administrativa y respuestas de ejercicios interactivos.
    app.register_blueprint(ejercicios_bp)

    # ======================================
    # 5. RUTA PRINCIPAL
    # ======================================

    @app.route("/")
    def inicio():

        return redirect(
            url_for("login.iniciar_sesion")
        )

    return app


# ==========================================
# 6. EJECUTAR FLASK
# ==========================================

app = create_app()


if __name__ == "__main__":

    # Solo para desarrollo local.
    app.run(debug=True)
