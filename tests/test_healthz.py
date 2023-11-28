import pytest
import requests
import requests_mock


def get_health_status():
    response = requests.get("http://virtumall.com/healthz")
    return response.json()


def test_healthz_endpoint():
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://virtumall.com/healthz", json={"message": "ok"}, status_code=200
        )
        response = get_health_status()
        assert response["message"] == "ok"
