import pytest
import requests
import responses
from requests.exceptions import HTTPError, Timeout, TooManyRedirects, ConnectionError, RequestException
from API import API
from unittest.mock import Mock

class MockLogger:
    def error(self, msg):
        print(msg)

@pytest.fixture
def api():
    return API(url="http://example.com", token="testtoken", logger=MockLogger())

@responses.activate
def test_get_devices_success(api):
    responses.add(responses.GET, "http://example.com/workers/devices",
                  json={"devices": ["device1", "device2"]}, status=200)

    devices = api.get_devices()
    assert devices == {"devices": ["device1", "device2"]}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://example.com/workers/devices?token=testtoken"

@responses.activate
def test_get_devices_http_error(api):
    responses.add(responses.GET, "http://example.com/workers/devices", status=500)

    devices = api.get_devices()
    assert devices is None
    assert len(responses.calls) == 3  # Ajusté pour refléter les 3 tentatives

@responses.activate
def test_get_devices_timeout(api):
    responses.add(responses.GET, "http://example.com/workers/devices", body=Timeout("Timeout Error"))

    devices = api.get_devices()
    assert devices is None
    assert len(responses.calls) == 3  # Ajusté pour refléter les 3 tentatives

@responses.activate
def test_send_devices_status_success(api):
    responses.add(responses.POST, "http://example.com/devices/status", status=200)

    result = api.send_devices_status({"status": "active"})
    assert result is True
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://example.com/devices/status"
    assert responses.calls[0].request.body == b'{"token": "testtoken", "status": {"status": "active"}}'  # Correction de l'espace après "token":

@responses.activate
def test_send_devices_status_http_error(api):
    responses.add(responses.POST, "http://example.com/devices/status", status=500)

    result = api.send_devices_status({"status": "active"})
    assert result is None
    assert len(responses.calls) == 1

@responses.activate
def test_send_fields_success(api):
    responses.add(responses.POST, "http://example.com/fields/bulk", status=200)

    result = api.send_fields({"field1": "value1", "field2": "value2"})
    assert result is True
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://example.com/fields/bulk"
    assert responses.calls[0].request.body == b'{"token": "testtoken", "fields": {"field1": "value1", "field2": "value2"}}'  # Correction de l'espace après "token":

@responses.activate
def test_send_fields_http_error(api):
    responses.add(responses.POST, "http://example.com/fields/bulk", status=500)

    result = api.send_fields({"field1": "value1", "field2": "value2"})
    assert result is None
    assert len(responses.calls) == 1
