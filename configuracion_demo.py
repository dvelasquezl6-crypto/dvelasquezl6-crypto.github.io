"""La demostración utiliza otra base SQL Server, nunca la base de trabajo."""
from sqlalchemy.engine import make_url
from config import Config

NOMBRE_BASE_DEMO = "SistemaPictograficoDemo"


def opciones_demo():
    url = make_url(Config.SQLALCHEMY_DATABASE_URI)
    if url.get_backend_name() != "mssql":
        raise RuntimeError("Esta preparación requiere SQL Server.")
    return {"SQLALCHEMY_DATABASE_URI": url.set(database=NOMBRE_BASE_DEMO),
            "DEBUG": False, "SESSION_COOKIE_SECURE": True,
            "SESSION_COOKIE_NAME": "sistema_pictografico_demo"}
