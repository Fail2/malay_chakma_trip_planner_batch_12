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


