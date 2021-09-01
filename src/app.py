from flask import json, request, jsonify, Blueprint, render_template
from models import Reservation,  db, User, Death
from datetime import timedelta, datetime
from app import app

user = Blueprint('api_user', __name__)

sessiontime = timedelta(hours=3)

@user.route('/register', methods=['POST'])
def register_user():
    if User.query.filter_by(name=request.json.get('name')).first() is not None:
        return jsonify(Error='User already registered'), 409
    user = User()
    user.name = request.json.get('name')
    user.lastname = request.json.get('lastname')

    db.session.add(user)
    db.session.commit()

    return jsonify(Success='User created'), 201

@user.route('/death', methods=['POST'])
@jwt_required()
def add_dance_death(death_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(name=current_user).first()
    death = Death.query.filter_by(id=death_id).first()
    id_reservation = request.json.get("id_reservation")
    reservation = Reservation.query.filter_by(id_death=death.id, id=id_reservation).first()
    if reservation is None:
        return jsonify(Error="Reservation not found"), 404
    reservation.id_user = user.id
    reservation.status = Reservation_Status.reserved
    
    db.session.commit()
    return jsonify(Success="Reservation added with death"), 201

@user.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(name=current_user).first()
    reservations = Reservation.query.filter_by(id_user=user.id, status=Reservation_Status.reserved).all()
    return jsonify([reservation.serialize() for reservation in reservations ]), 200

@user.route('/reservations/<int:id_reservation>/cancel', methods=['DELETE'])
@jwt_required()
def cancel_reservation(id_reservation):
    current_user = get_jwt_identity()
    user = User.query.filter_by(name=current_user).first()
    reservation = Reservation.query.filter_by(id=id_reservation).first()
    if reservation is None:
        return jsonify(Error="Reservation not found"), 404
    if reservation.id_user != user.id:
        return jsonify(Error="Not authorized"), 401
    reservation.status = Reservation_Status.canceled
    db.session.commit()
    return jsonify(Success="Reservation canceled"), 200