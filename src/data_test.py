"""Tests for data module"""
# pylint: disable=redefined-outer-name
import pytest

from data import Product


@pytest.fixture
def example_product():
    """Product fixture"""
    return Product('name', 'ipsId', 'bpId', '2020-01-01T00:00:00.000Z')


def test_init(example_product):
    """Test if product is initialized correctly"""
    assert example_product.name == 'name'
    assert example_product.product_id == 'ipsId'
    assert example_product.business_partner_id == 'bpId'
    assert example_product.created_at.year == 2020
    assert example_product.created_at.month == 1
    assert example_product.created_at.day == 1
    assert example_product.history == {}
    assert example_product.deposit == {}


def test_str(example_product):
    """Test if str repr of product is correct"""
    assert (
        str(example_product) == 'Product(name=name, ipsID=ipsId, created_at=2020-01-01 00:00:00)'
    )


def test_repr(example_product):
    """Test if str repr of product is correct"""
    assert (
        repr(example_product) == 'Product(name=name, ipsID=ipsId, created_at=2020-01-01 00:00:00)'
    )


def test_set_history(example_product):
    """Test if history is set correctly"""
    example_product.set_history({'2020-01-01': 1})
    assert example_product.history == {'2020-01-01': 1}


def test_set_deposit(example_product):
    """Test if deposit is set correctly"""
    example_product.set_deposit({'2020-01-01': 1})
    assert example_product.deposit == {'2020-01-01': 1}
