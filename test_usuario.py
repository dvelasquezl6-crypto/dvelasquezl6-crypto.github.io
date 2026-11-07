
# ============================================
# PRUEBA DEL MODELO USUARIO
# ============================================

# Importamos la aplicación Flask.
from app import app

# Importamos la conexión a la base de datos.
from database import db

# Importamos el modelo de usuarios.
from models.usuario import Usuario


# ============================================
# 1. INICIAR CONTEXTO DE FLASK
# ============================================

with app.app_context():

    try:

        # ====================================
        # 2. CONSULTAR LOS USUARIOS
        # ====================================

        # Obtenemos los usuarios registrados
        # y los ordenamos por su identificador.
        consulta = db.select(Usuario).order_by(
            Usuario.id_usuario
        )

        usuarios = db.session.execute(
            consulta
        ).scalars().all()


        # ====================================
        # 3. MOSTRAR RESULTADOS
        # ====================================

        print("==============================")
        print("USUARIOS DEL SISTEMA")
        print("==============================")

        for usuario in usuarios:

            print("ID:", usuario.id_usuario)

            print(
                "Nombre:",
                usuario.nombre,
                usuario.apellido
            )

            print(
                "Usuario:",
                usuario.nombre_usuario
            )

            # Consultamos el rol relacionado.
            print(
                "Rol:",
                usuario.rol.nombre_rol
            )

            # Comprobamos el estado.
            if usuario.estado:
                print("Estado: Activo")
            else:
                print("Estado: Inactivo")

            print("------------------------------")


        # ====================================
        # 4. CONFIRMAR LA CONSULTA
        # ====================================

        print("Consulta realizada correctamente.")


    except Exception as error:

        # Mostramos errores de consulta.
        print("ERROR AL CONSULTAR USUARIOS")
        print(error)
