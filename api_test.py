import pytest

from api import APIClient


@pytest.fixture
def client():
    return APIClient()


def test_get_endpoints(client):
    response = client.get_endpoints()
    print(response)
    assert response['version'] == '1.0.0'
    assert response['status'] == 'OK'
    for endpoint in ['login', 'refreshToken', 'getUserV2', 'getBusinessPartnerById', 'getProductById']:
        assert endpoint in response['endpoints']
