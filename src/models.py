import os
import sys
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

db = SQLAlchemy()
Base = declarative_base()
Reservation_Status = Enum('Reservation_Status', 'available reserved canceled confirmed missed finished' )

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname= db.Column(db.String(50), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    reservations = db.relationship('Reservation', cascade='all, delete', backref='user')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname
        }

    def serialize_reservations(self):
        return list(map(lambda reservation: reservation.serialize(), self.reservations))

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        if self.id_user is None:
            name = self.user.name
        else:
            name = self.user.name

        if self.status == Reservation_Status.available:
            status = 'available'
        elif self.status == Reservation_Status.reserved:
            status = 'reserved'
        elif self.status == Reservation_Status.canceled:
            status = 'canceled'
        elif self.status == Reservation_Status.missed:
            status = 'missed'
        elif self.status == Reservation_Status.confirmed:
            status = 'confirmed'
        elif self.status == Reservation_Status.finished:
            status = 'finished'
        return {
            'id': self.id,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'id_user': self.id_user,
            'user_name': self.user.name + ' ' + self.user.lastname,
            'status' : status,
        }

class Death(db.Model):
    __tablename__ = 'death'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reservations = db.relationship('Reservation', cascade='all, delete', backref='clinic')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')