# test_app.py
import pytest
from app.main import app  # Kontrollera att importvägen är korrekt
from unittest.mock import patch

@pytest.fixture
def client():
    # Skapar en testklient för appen
    with app.test_client() as client:
        yield client

# Testar att startsidan laddar korrekt
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Weather App" in response.data  # Kontrollera att rubriken finns på sidan

# Testar att ett POST-anrop med giltiga städer returnerar korrekt väderdata
@patch('app.main.get_weather')
def test_weather_post(mock_get_weather, client):
    # Mocka väderdata för städer
    mock_get_weather.side_effect = [
        {"city": "Stockholm", "temperature": 10, "description": "Clear sky", "icon": "01d"},
        {"city": "Gothenburg", "temperature": 15, "description": "Cloudy", "icon": "03d"}
    ]
    response = client.post('/', data={'city1': 'Stockholm', 'city2': 'Gothenburg'})
    assert response.status_code == 200
    assert b"Stockholm" in response.data
    assert b"Gothenburg" in response.data

# Testar att applikationen hanterar fel vid hämtning av väderdata
@patch('app.main.get_weather', return_value=None)
def test_weather_post_with_invalid_city(mock_get_weather, client):
    response = client.post('/', data={'city1': 'InvalidCity', 'city2': ''})
    assert response.status_code == 200
    assert b"InvalidCity" not in response.data

# Testar väder-API med mockade koordinater och svar
@patch('requests.get')
def test_weather_api(mock_get, client):
    mock_get.return_value.json.return_value = {
        "main": {"temp": 20},
        "weather": [{"description": "Clear sky"}]
    }
    mock_get.return_value.status_code = 200

    response = client.get('/weather?lat=59.3293&lng=18.0686')  # Stockholm koordinater
    assert response.status_code == 200
    assert response.json['temperature'] == 20
    assert response.json['description'] == "Clear sky"

# Testar hantering av saknade koordinater i API-förfrågan
def test_weather_api_missing_coordinates(client):
    response = client.get('/weather')
    assert response.status_code == 400
    assert b"Latitud och longitud saknas." in response.data

