from __future__ import annotations
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from .schemas import serviceTicket_schema, serviceTickets_schema
from app.models import ServiceTickets, db
from . import serviceTickets_bp

#   ServiceTickets
#	GET /serviceTickets: Retrieve service ticket by id
@serviceTickets_bp.route('/<int:id>', methods=['GET'])
def get_Service_Ticket(id):
    serviceTicket = db.session.get(ServiceTickets, id)
    return serviceTicket_schema.jsonify(serviceTicket), 200

#	GET /serviceTickets: Retrieve all serviceTickets
@serviceTickets_bp.route('/', methods=['GET'])
def get_serviceTickets():
    query = select(ServiceTickets)
    serviceTickets = db.session.execute(query).scalars().all()
    return serviceTickets_schema.jsonify(serviceTickets), 200

#  POST /serviceTickets: Create a new service ticket
@serviceTickets_bp.route('/', methods=['POST'])
def create_serviceTicket():
    try:
        serviceTicket_data = request.get_json()  # or schema.load()
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    service_date = serviceTicket_data.get("service_date")
    newServiceTicket = ServiceTickets(
        VIN=serviceTicket_data["VIN"],
        service_date=service_date,
        service_desc=serviceTicket_data["service_desc"],
        customer_id=serviceTicket_data["customer_id"],
    )

    db.session.add(newServiceTicket)
    db.session.commit()

    return jsonify({"message": "Service ticket created", "id": newServiceTicket.id}), 201

#	PUT /serviceTickets/<id>: Update a service ticket by ID
@serviceTickets_bp.route('/<int:id>', methods=['PUT'])
def updateServiceTicket(id):
    serviceTicket = db.session.get(ServiceTickets, id)

    if not serviceTicket:
        return jsonify({"message": "Invalid service ticket id"}), 400
    
    try:
        serviceTicket_data = serviceTicket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    serviceTicket.VIN = serviceTicket_data['VIN']
    serviceTicket.service_date = serviceTicket_data['service_date']
    serviceTicket.service_desc = serviceTicket_data['service_desc']

    db.session.commit()
    return serviceTicket_schema.jsonify(serviceTicket), 200

#   DELETE /serviceTickets/<id>: Delete a service ticket by ID
@serviceTickets_bp.route('/<int:id>', methods=['DELETE'])
def delete_serviceTicket(id):
    serviceTicket = db.session.get(ServiceTickets, id)

    if not serviceTicket:
        return jsonify({"message": "Invalid service ticket id"}), 400
    db.session.delete(serviceTicket)
    db.session.commit()
    return jsonify({"message": f"succefully deleted service ticket {id}"}), 200