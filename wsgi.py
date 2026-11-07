"""Punto de entrada para un servidor WSGI de producción, sin depuración."""
from app import create_app

app = create_app()
