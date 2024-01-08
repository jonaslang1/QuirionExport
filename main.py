import logging
from api import APIClient
from data import Product
from datetime import datetime


def export_csv(p):
    with open(f'output_{p.name}.csv', 'w') as f:
        f.write('Datum;Kurs;Höchst;Tiefst;Umsatz\n')
        prev = 0
        for date, value in p.history.items():
            if date not in p.deposit:
                continue
            value = value / p.deposit[date] * 100
            if value == prev:
                continue
            date = datetime.strptime(date, "%Y-%m-%d").strftime('%d.%m.%Y')
            f.write(f'{date};{value:.3f};;;\n')
            prev = value


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = APIClient()
    client.fetch_token()
    business_partner_ids = client.get_business_partner_id()
    products = []
    for business_partner_id in business_partner_ids:
        res = client.get_products(business_partner_id)
        for product in res:
            products.append(Product(product["name"], product["ipsId"], business_partner_id, product["createdAt"]))
    for product in products:
        print(product)
        res = client.get_product_history(product.business_partner_id, product.product_id)
        product.set_history({entry['d']: entry['v'] for entry in res["history"]})
        product.set_deposit({entry['d']: entry['v'] for entry in res["rendite"]})
    for product in products:
        export_csv(product)
