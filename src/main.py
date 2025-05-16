"""Main module"""
import logging
import sys
from getpass import getpass
from datetime import datetime, timedelta

from requests import HTTPError

from api import APIClient
from data import Product
from export import export_csv, save_postbox_document

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = APIClient()
    username = input('username:')
    pw = getpass('password:')
    try:
        client.fetch_token(username, pw)
    except HTTPError as e:
        logging.error('Error fetching token: %s', e)
        input("Press Enter to exit...")
        sys.exit(1)
    business_partner_ids = client.get_business_partner_id()
    products = []
    for bp_id in business_partner_ids:
        res = client.get_products(bp_id)
        for product in res:
            products.append(
                Product(product["name"], product["ipsId"], bp_id, product["createdAt"])
            )
    for product in products:
        logging.debug('Fetching and exporting data from %s', product)
        res = client.get_product_history(product.business_partner_id, product.product_id)
        product.set_history({entry['d']: entry['v'] for entry in res["history"]})
        product.set_deposit({entry['d']: entry['v'] for entry in res["rendite"]})
        export_csv(product)
        logging.info('Successfully exported data from %s', product)
    now = datetime.now()
    three_months_ago = now - timedelta(days=90)
    from_date = three_months_ago.strftime('%Y-%m-%d')
    to_date = now.strftime('%Y-%m-%d')
    postbox_items = client.get_postbox_items(status='ALL', from_date=from_date, to_date=to_date)
    if len(postbox_items) > 0:
        logging.info('Found %d unread postbox items', len(postbox_items))
        input_str = input("Do you want to download the documents? (y/n): ")
        if input_str.lower() != 'y':
            logging.info('User chose not to download documents')
            sys.exit(0)
    else:
        logging.info('No unread postbox items found')
        sys.exit(0)
    for item in postbox_items:
        logging.debug('Fetching and downloading data from %s', item['displayName'])
        res = client.get_postbox_document(item['id'])
        save_postbox_document(item, res)
        logging.info('Successfully downloaded and saved document from %s', item['displayName'])
    logging.info('Successfully downloaded %d documents', len(postbox_items))
