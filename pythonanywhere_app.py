"""Entrada exclusiva del alojamiento gratuito; SQLite en un directorio privado."""
import os
from pathlib import Path
from sqlalchemy.engine import URL

directorio = Path(__file__).resolve().parent / "instance"
directorio.mkdir(exist_ok=True)
os.environ["DATABASE_URL"] = URL.create("sqlite", database=str(directorio / "alojamiento.sqlite3")).render_as_string()
os.environ["COOKIE_SECURE"] = "true"

# Configurar la base antes de importar Flask impide abrir la conexión local.
from app import app as application
