from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_exception(e):
    """Manejo de excepciones generales."""
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response
    # Manejadores para otros tipos de excepciones (si es necesario)