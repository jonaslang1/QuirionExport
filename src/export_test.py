"""Tests for export module"""
import base64

# pylint: disable=redefined-outer-name

import pytest

from data import Product
from export import (export_csv_history, save_postbox_document,
                    export_csv_transactions, create_dir_if_not_exists)


def test_create_dir_if_not_exists(tmp_path):
    """Test if directory is created if it does not exist"""
    test_dir = tmp_path / "test_dir"
    assert not test_dir.exists()
    create_dir_if_not_exists(test_dir)
    assert test_dir.exists()
    assert test_dir.is_dir()


@pytest.fixture
def example_product():
    """Product fixture"""
    product = Product('test', 'ipsId', 'bpId', '2020-01-01T00:00:00.000Z')
    product.set_history({'2020-01-01': 1, '2020-01-02': 2, '2020-01-03': 3})
    product.set_deposit({'2020-01-01': 1, '2020-01-02': 1, '2020-01-03': 1})
    return product


def test_export_csv_history(example_product):
    """Test if csv export is correct"""
    export_csv_history(example_product)
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


@pytest.fixture
def example_transactions():
    """Transactions fixture"""
    return [
        {
            "amount": 20000,
            "orderType": "Gutschrift (1040)",
            "currency": "EUR",
            "createdAt": "2023-04-11T07:03:53.892Z",
            "metaType": "Zahlungseingang (30)",
            "Verwendungszweck": "Zahlungseingang",
            "valutaDate": "2023-04-06",
            "bookingDate": "2023-04-06",
            "status": "CLOSED",
            "type": "Überweisungseingang"
        },
        {
            "amount": 135.59,
            "orderType": "Zinszahlung (161)",
            "currency": "EUR",
            "createdAt": "2023-07-03T07:04:12.489Z",
            "metaType": "Zins (16)",
            "Verwendungszweck": "31.03.23-30.06.23",
            "valutaDate": "2023-06-30",
            "bookingDate": "2023-06-30",
            "status": "CLOSED",
            "type": "Transaktion"
        },
    ]


def test_export_csv_transactions(example_transactions):
    """Test if transactions csv export is correct"""
    export_csv_transactions(example_transactions, "bpId")
    with open('output/output_Verrechnungskonto_bpId.csv', 'r', encoding='UTF-8') as f:
        lines = f.read().splitlines()
        assert lines[0] == 'Buchungsdatum;Wertstellungsdatum;Betrag;Verwendungszweck'
        assert lines[1] == ('06.04.2023;06.04.2023;20000,00;'
                            'Überweisungseingang - Gutschrift - Zahlungseingang')
        assert lines[2] == ('30.06.2023;30.06.2023;135,59;'
                            'Transaktion - Zinszahlung - 31.03.23-30.06.23')
        assert len(lines) == 3
