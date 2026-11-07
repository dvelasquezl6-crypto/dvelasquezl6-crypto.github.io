from sqlalchemy import text

from app import app
from database import db


with app.app_context():

    try:

        resultado = db.session.execute(
            text("SELECT DB_NAME()")
        )

        nombre_bd = resultado.scalar()

        print("===================================")
        print("CONEXIÓN EXITOSA")
        print("Base de datos:", nombre_bd)
        print("===================================")

    except Exception as error:

        print("===================================")
        print("ERROR DE CONEXIÓN")
        print(error)
        print("===================================")