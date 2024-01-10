"""Tests for api module"""
# pylint: disable=redefined-outer-name
import pytest

from api import APIClient


@pytest.fixture
def client():
    """API Client fixture"""
    return APIClient()


def test_get_endpoints(client):
    """Test if all endpoints are available"""
    response = client.get_endpoints()
    print(response)
    assert response['version'] == '1.0.0'
    assert response['status'] == 'OK'
    required_endpoints = [
        'login', 'refreshToken', 'getUserV2', 'getBusinessPartnerById', 'getProductById'
    ]
    for endpoint in required_endpoints:
        assert endpoint in response['endpoints']
