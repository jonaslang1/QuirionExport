"""Tests for data module"""
from data import Product
import pytest


@pytest.fixture
def example_product():
    return Product('name', 'ipsId', 'bpId', '2020-01-01T00:00:00.000Z')


def test_init(example_product):
    assert example_product.name == 'name'
    assert example_product.product_id == 'ipsId'
    assert example_product.business_partner_id == 'bpId'
    assert example_product.created_at.year == 2020
    assert example_product.created_at.month == 1
    assert example_product.created_at.day == 1
    assert example_product.history == {}
    assert example_product.deposit == {}


def test_str(example_product):
    assert str(example_product) == 'Product(name=name, ipsID=ipsId, created_at=2020-01-01 00:00:00)'


def test_repr(example_product):
    assert repr(example_product) == 'Product(name=name, ipsID=ipsId, created_at=2020-01-01 00:00:00)'


def test_set_history(example_product):
    example_product.set_history({'2020-01-01': 1})
    assert example_product.history == {'2020-01-01': 1}


def test_set_deposit(example_product):
    example_product.set_deposit({'2020-01-01': 1})
    assert example_product.deposit == {'2020-01-01': 1}

