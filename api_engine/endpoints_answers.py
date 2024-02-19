from api_url_creator.url_creator import UrlCreator
from pathlib import Path
from requests.exceptions import HTTPError
from requests_mock import Mocker
import pytest
import requests
import json

'https://restful-booker.herokuapp.com/apidoc/index.html - api-Booking-CreateBooking'


url_instance = UrlCreator()
WD = Path(__file__).resolve().parent.parent

@pytest.fixture(scope='module')
def create_booking():
    with open(f'{WD}/json_data/booking.json', 'r') as json_package:
        booking_data = json.load(json_package)
    response = requests.post(url_instance.booking(), json=booking_data)
    assert response.status_code == 200
    booking_id = response.json().get('bookingid')
    yield booking_id

def test_create_booking(create_booking):
    assert isinstance(create_booking, int)

def test_wrong_json_data():
    wrong_data = f'{WD}/json_data/wrong_json_data.json'
    response = requests.post(url_instance.booking(), data=wrong_data, headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    assert 'Bad Request' in response.text

@pytest.fixture(scope='module')
def mock_create_booking():
    with Mocker() as m:
        m.post(url_instance.booking(), status_code=401)
        yield m

def test_unauthorized_access(mock_create_booking):
    with pytest.raises(HTTPError) as error:
        response = requests.post(url_instance.booking())
        response.raise_for_status()
    assert error.value.response.status_code == 401

@pytest.fixture(scope='module')
def mock_rate_limiting():
    with Mocker() as m:
        m.post(url_instance.booking(), status_code=429)
        yield m

def test_rate_limiting(mock_rate_limiting):
    with pytest.raises(HTTPError) as error:
        response = requests.post(url_instance.booking())
        response.raise_for_status()
    assert error.value.response.status_code == 429

