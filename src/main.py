"""Main module"""
import logging
from getpass import getpass

from api import APIClient
from data import Product
from export import export_csv


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = APIClient()
    username = input('username:')
    pw = getpass('password:')
    client.fetch_token(username, pw)
    business_partner_ids = client.get_business_partner_id()
    products = []
    for bp_id in business_partner_ids:
        res = client.get_products(bp_id)
        for product in res:
            products.append(
                Product(product["name"], product["ipsId"], bp_id, product["createdAt"])
            )
    for product in products:
        logging.debug(f'Fetching and exporting data from {product}')
        res = client.get_product_history(product.business_partner_id, product.product_id)
        product.set_history({entry['d']: entry['v'] for entry in res["history"]})
        product.set_deposit({entry['d']: entry['v'] for entry in res["rendite"]})
        export_csv(product)
        logging.info(f'Successfully exported data from {product}')

