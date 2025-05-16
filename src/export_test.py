"""Tests for export module"""
import base64

# pylint: disable=redefined-outer-name

import pytest

from data import Product
from export import export_csv, save_postbox_document


@pytest.fixture
def example_product():
    """Product fixture"""
    product = Product('test', 'ipsId', 'bpId', '2020-01-01T00:00:00.000Z')
    product.set_history({'2020-01-01': 1, '2020-01-02': 2, '2020-01-03': 3})
    product.set_deposit({'2020-01-01': 1, '2020-01-02': 1, '2020-01-03': 1})
    return product


def test_export_csv(example_product):
    """Test if csv export is correct"""
    export_csv(example_product)
    with open('output/output_test.csv', 'r', encoding='UTF-8') as f:
        lines = f.read().splitlines()
        assert lines[0] == 'Datum;Kurs;Höchst;Tiefst;Umsatz'
        assert lines[1] == '01.01.2020;100,000;;;'
        assert lines[2] == '02.01.2020;200,000;;;'
        assert lines[3] == '03.01.2020;300,000;;;'
        assert len(lines) == 4


def test_save_postbox_document():
    """Test if postbox document is saved correctly"""
    # This test requires a valid document item and content
    # You can mock the document item and content for testing purposes
    document_item = {
        'fileName': 'test.pdf',
        'displayName': 'Test Document'
    }
    content = b'Test content'
    content_bytes = base64.b64encode(content)
    save_postbox_document(document_item, content_bytes)
    with open('output/documents/test.pdf', 'rb') as f:
        assert f.read() == content