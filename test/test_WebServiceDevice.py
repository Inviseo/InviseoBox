import pytest
import requests
import requests_mock
from WebServiceDevice import WebServiceDevice
from Logger import Logger

@pytest.fixture
def web_service_device():
    logger = Logger()
    return WebServiceDevice(url="http://example.com", logger=logger)

def test_get_data_success(web_service_device, requests_mock):
    # Mock de la réponse de la requête HTTP avec un code 200 et un JSON
    requests_mock.get("http://example.com", json={"key": "value"}, status_code=200)
    success, data = web_service_device.getData()
    assert success is True
    assert data == {"key": "value"}

def test_get_data_http_error(web_service_device, requests_mock):
    # Mock de la réponse de la requête HTTP avec un code 404
    requests_mock.get("http://example.com", status_code=404)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_timeout(web_service_device, requests_mock):
    # Mock de la requête HTTP pour lever une exception de timeout
    requests_mock.get("http://example.com", exc=requests.exceptions.Timeout)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_connection_error(web_service_device, requests_mock):
    # Mock de la requête HTTP pour lever une exception de connexion
    requests_mock.get("http://example.com", exc=requests.exceptions.ConnectionError)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_too_many_redirects(web_service_device, requests_mock):
    # Mock de la requête HTTP pour lever une exception de trop de redirections
    requests_mock.get("http://example.com", exc=requests.exceptions.TooManyRedirects)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_request_exception(web_service_device, requests_mock):
    # Mock de la requête HTTP pour lever une exception générique de requête
    requests_mock.get("http://example.com", exc=requests.exceptions.RequestException)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_unexpected_exception(web_service_device, requests_mock):
    # Mock de la requête HTTP pour lever une exception inattendue
    requests_mock.get("http://example.com", exc=Exception)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_invalid_json(web_service_device, requests_mock):
    # Mock de la réponse de la requête HTTP avec un contenu non JSON
    requests_mock.get("http://example.com", text="<!doctype html><html><body>Not JSON</body></html>", status_code=200)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_no_url():
    logger = Logger()
    web_service_device = WebServiceDevice(url=None, logger=logger)
    success, data = web_service_device.getData()
    assert success is False
    assert data is None

def test_get_data_no_logger():
    web_service_device = WebServiceDevice(url="http://example.com", logger=None)
    with requests_mock.Mocker() as m:
        m.get("http://example.com", json={"key": "value"}, status_code=200)
        success, data = web_service_device.getData()
        assert success is True
        assert data == {"key": "value"}
