import pytest
from datetime import date

from app import db, create_app
from app.models import Trip
from app.services import list_trips,get_trip,create_trip,update_trip,update_trip_status,delete_trip,get_trip_summary


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def trip(app):
    data = {
        "destination": "Cox's Bazar",
        "start_date": "2099-10-10",
        "end_date": "2099-10-15",
        "budget": 50000,
        "max_travelers": 5,
    }

    response, status_code = create_trip(data)

    assert status_code == 201
    assert response["success"] is True

    return db.session.get(Trip, response["data"]["id"])


def test_list_trips_empty(app):
    with app.app_context():
        response, status_code = list_trips()

        assert status_code == 200
        assert response["success"] is True
        assert response["data"] == []


def test_create_trip_success(app):
    with app.app_context():
        data = {
            "destination": "Rangamati",
            "start_date": "2099-10-10",
            "end_date": "2099-10-15",
            "budget": 35000,
            "max_travelers": 4,
        }

        response, status_code = create_trip(data)

        assert status_code == 201
        assert response["success"] is True
        assert response["message"] == "Trip created successfully"
        assert response["data"]["destination"] == "Rangamati"
        assert response["data"]["budget"] == 35000
        assert response["data"]["max_travelers"] == 4


def test_create_trip_validation_error(app):
    with app.app_context():
        data = {
            "destination": "",
            "start_date": "2099-10-10",
            "end_date": "2099-10-15",
            "budget": 50000,
            "max_travelers": 5,
        }

        response, status_code = create_trip(data)

        assert status_code == 400
        assert response["success"] is False
        assert response["error"] == "Validation error"


def test_get_trip_success(app, trip):
    with app.app_context():
        response, status_code = get_trip(trip.id)

        assert status_code == 200
        assert response["success"] is True
        assert response["data"]["id"] == trip.id
        assert response["data"]["destination"] == "Cox's Bazar"
        assert response["data"]["budget"] == 50000


def test_get_trip_not_found(app):
    with app.app_context():
        response, status_code = get_trip(999)

        assert status_code == 404
        assert response["success"] is False
        assert response["error"] == "Resource not found"


def test_list_trips_success(app, trip):
    with app.app_context():
        response, status_code = list_trips()

        assert status_code == 200
        assert response["success"] is True
        assert len(response["data"]) == 1
        assert response["data"][0]["id"] == trip.id


def test_update_trip_success(app, trip):
    with app.app_context():
        data = {
            "destination": "Rangamati",
            "start_date": "2099-11-10",
            "end_date": "2099-11-15",
            "budget": 60000,
            "max_travelers": 6,
        }

        response, status_code = update_trip(trip.id, data)

        assert status_code == 200
        assert response["success"] is True
        assert response["message"] == "Trip updated successfully"
        assert response["data"]["destination"] == "Rangamati"
        assert response["data"]["budget"] == 60000
        assert response["data"]["max_travelers"] == 6


def test_update_trip_not_found(app):
    with app.app_context():
        data = {
            "destination": "Rangamati",
            "start_date": "2099-11-10",
            "end_date": "2099-11-15",
            "budget": 60000,
            "max_travelers": 6,
        }

        response, status_code = update_trip(999, data)

        assert status_code == 404
        assert response["success"] is False
        assert response["error"] == "Resource not found"


def test_update_trip_budget_less_than_expenses(app, trip):
    with app.app_context():
        data = {
            "destination": "Cox's Bazar",
            "start_date": "2099-10-10",
            "end_date": "2099-10-15",
            "budget": 40000,
            "max_travelers": 5,
        }

        response, status_code = update_trip(trip.id, data)

        assert status_code == 200
        assert response["success"] is True



def test_update_trip_validation_error(app, trip):
    with app.app_context():
        data = {
            "destination": "",
            "start_date": "2099-10-10",
            "end_date": "2099-10-15",
            "budget": 50000,
            "max_travelers": 5,
        }

        response, status_code = update_trip(trip.id, data)

        assert status_code == 400
        assert response["success"] is False
        assert response["error"] == "Validation error"


def test_update_trip_status_success(app, trip):
    with app.app_context():
        data = {
            "status": "ongoing"
        }

        response, status_code = update_trip_status(trip.id, data)

        assert status_code == 200
        assert response["success"] is True
        assert response["message"] == "Trip status updated successfully"
        assert response["data"]["status"] == "ONGOING"


def test_update_trip_status_invalid_transition(app, trip):
    with app.app_context():
        data = {
            "status": "completed"
        }

        response, status_code = update_trip_status(trip.id, data)

        assert status_code == 400
        assert response["success"] is False
        assert response["error"] == "Validation error"


def test_update_trip_status_not_found(app):
    with app.app_context():
        data = {
            "status": "ongoing"
        }

        response, status_code = update_trip_status(999, data)

        assert status_code == 404
        assert response["success"] is False
        assert response["error"] == "Resource not found"




