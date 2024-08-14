from flask import Blueprint, request, jsonify, abort
from . import db
from .models import Item

main_bp = Blueprint('main', __name__)

ERROR_NO_DATA = "No data provided"
ERROR_MISSING_NAME = "Missing required parameter: 'name'"
ERROR_MISSING_DESCRIPTION = "Missing required parameter: 'description'"


# Prueba de la ruta

def validate_item_data(data):
    if not data:
        abort(400, description=ERROR_NO_DATA)
    if 'name' not in data:
        abort(400, description=ERROR_MISSING_NAME)
    if 'description' not in data:
        abort(400, description=ERROR_MISSING_DESCRIPTION)


@main_bp.route('/items', methods=['POST'])
def create_item():
    try:
        # Asegurarse de que las tablas se crean si no existen
        with db.session.begin_nested():
            print("Verifying and creating tables if not present...")
            db.create_all()
            print("Tables verified/created.")

        data = request.get_json()
        if not data:
            print("No data provided in request")
            return jsonify({'error': 'No data provided'}), 400

        validate_item_data(data)
        print(f"Data validated: {data}")

        new_item = Item(name=data['name'], description=data['description'])
        db.session.add(new_item)
        db.session.commit()
        print("Item created successfully.")
        return jsonify({'message': 'Item created successfully', 'id': new_item.id}), 201

    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@main_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    results = [{"id": item.id, "name": item.name, "description": item.description} for item in items]
    return jsonify(results), 200


@main_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    result = {"id": item.id, "name": item.name, "description": item.description}
    return jsonify(result), 200


@main_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    validate_item_data(data)

    item = Item.query.get_or_404(item_id)
    item.name = data['name']
    item.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'}), 200


@main_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200
