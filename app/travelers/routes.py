from flask import Blueprint, jsonify, render_template, request
from app.models import Trip
from validators.trip_validator import trip_create_validate, trip_update_validate
from app import db


travelers_bp = Blueprint('travelers',__name__)

@travelers_bp.post('/<int:trip_id>/travelers')
def add_traveler_to_trip(trip_id):
    print(trip_id)
    return {"Success": True},200
