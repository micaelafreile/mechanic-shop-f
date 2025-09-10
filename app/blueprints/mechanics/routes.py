
from __future__ import annotations
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from .schemas import mechanic_schema, mechanics_schema
from app.models import Mechanics, db
from . import mechanics_bp

#   Mechanics
#	GET /mechanics: Retrieve mechanics by id
@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = db.session.get(Mechanics, id)
    return mechanic_schema.jsonify(mechanic), 200

#	GET /mechanics: Retrieve all mechanics
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200

#  POST /mechanics: Create a new mechanic
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanics(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201

#	PUT /mechanics/<id>: Update a mechanic by ID
@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanics, id)

    if not mechanic:
        return jsonify({"message": "Invalid mechanic id"}), 400
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic.name = mechanic_data['name']
    mechanic.email = mechanic_data['email']
    mechanic.phone = mechanic_data['phone']
    mechanic.salary = mechanic_data['salary']

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#   DELETE /mechanics/<id>: Delete a mechanic by ID
@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanics, id)

    if not mechanic:
        return jsonify({"message": "Invalid mechanic id"}), 400
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"succefully deleted mechanic {id}"}), 200
