import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.mark.parametrize(
    "path,expected_status",
    [
        ("/healthz", 200),
        ("/some-other-path", 404),
    ],
)
def test_health_check_middleware(
    client: Client, path: str, expected_status: int
) -> None:
    response = client.get(path)
    assert response.status_code == expected_status
