import pytest

from data import Product
from export import export_csv


@pytest.fixture
def example_product():
    product = Product('name', 'ipsId', 'bpId', '2020-01-01T00:00:00.000Z')
    product.set_history({'2020-01-01': 1, '2020-01-02': 2, '2020-01-03': 3})
    product.set_deposit({'2020-01-01': 1, '2020-01-02': 1, '2020-01-03': 1})
    return product


def test_export_csv(example_product):
    export_csv(example_product)
    with open('output/output_name.csv', 'r', encoding='UTF-8') as f:
        lines = f.read().splitlines()
        assert lines[0] == 'Datum;Kurs;Höchst;Tiefst;Umsatz'
        assert lines[1] == '01.01.2020;100.000;;;'
        assert lines[2] == '02.01.2020;200.000;;;'
        assert lines[3] == '03.01.2020;300.000;;;'
        assert len(lines) == 4
