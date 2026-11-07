
# ==========================================
# SISTEMA PICTOGRÁFICO INTERACTIVO
# ARCHIVO: config.py
# CONFIGURACIÓN GENERAL
# ==========================================

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargamos las variables privadas desde .env.
load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:

    # ======================================
    # 1. SEGURIDAD DE FLASK
    # ======================================

    # Clave utilizada para proteger las sesiones
    # y los tokens de los formularios.
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Impedimos que el sistema se inicie
    # sin una clave de seguridad configurada.
    if not SECRET_KEY:
        raise RuntimeError(
            "Falta configurar SECRET_KEY en .env"
        )

    # La cookie de sesión no estará disponible
    # para código JavaScript del navegador.
    SESSION_COOKIE_HTTPONLY = True

    # Evita que otra aplicación Flask local reemplace nuestra cookie "session".
    # El nombre es estable para conservar el acceso entre reinicios del proyecto.
    SESSION_COOKIE_NAME = "sistema_pictografico_session"
    SESSION_COOKIE_PATH = "/"

    # Reduce el envío de cookies en solicitudes
    # originadas desde otros sitios.
    SESSION_COOKIE_SAMESITE = "Lax"

    # En producción con HTTPS debe configurarse
    # COOKIE_SECURE=true en el archivo .env.
    SESSION_COOKIE_SECURE = (
        os.getenv("COOKIE_SECURE", "false").lower()
        == "true"
    )

    # ======================================
    # 2. CONEXIÓN CON SQL SERVER
    # ======================================

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        "mssql+pyodbc://@localhost\\SQLEXPRESS/"
        "SistemaPictografico"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&trusted_connection=yes"
        "&TrustServerCertificate=yes"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ======================================
    # 3. PROTECCIÓN CSRF
    # ======================================

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Límite total de la petición multipart (imagen, audio y campos).
    MAX_CONTENT_LENGTH = 12 * 1024 * 1024
