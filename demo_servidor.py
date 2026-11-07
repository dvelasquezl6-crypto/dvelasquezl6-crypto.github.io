"""Servidor local exclusivo para la demostración HTTPS mediante túnel."""
from waitress import serve
from app import create_app
from configuracion_demo import opciones_demo

if __name__ == "__main__":
    # No se utiliza el servidor de desarrollo ni el depurador. Se confía
    # únicamente en el proxy local que termina la conexión HTTPS del túnel.
    app = create_app(opciones_demo())
    serve(app, host="127.0.0.1", port=8081, trusted_proxy="127.0.0.1",
          trusted_proxy_headers="x-forwarded-proto", clear_untrusted_proxy_headers=True)
