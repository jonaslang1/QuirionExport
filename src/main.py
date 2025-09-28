"""Main module"""
import logging
import sys
from getpass import getpass
from datetime import datetime, timedelta
import argparse

from requests import HTTPError

from api import APIClient
from data import Product
from export import export_csv_history, save_postbox_document, export_csv_transactions


def end_program(exit_code=0):
    """End program"""
    logging.debug('Program ended')
    input("Press Enter to exit...")
    sys.exit(exit_code)


if __name__ == '__main__':
    # Logging configuration
    parser = argparse.ArgumentParser(description='QuirionExport')
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level))
    logging.debug('Logging level set to %s', args.log_level)
    # Set up API client
    client = APIClient()
    # get user credentials
    username = input('username:')
    pw = getpass('password:')
    # fetch token
    try:
        client.fetch_token(username, pw)
    except HTTPError as e:
        logging.error('Error fetching token: %s', e)
        end_program(1)
    # get business partner ids
    business_partner_ids = client.get_business_partner_id()
    # get products
    products = []
    for bp_id in business_partner_ids:
        res = client.get_products(bp_id)
        for product in res:
            products.append(
                Product(product["name"], product["ipsId"], bp_id, product["createdAt"])
            )
    # get product history
    for product in products:
        logging.debug('Fetching and exporting data from %s', product)
        res = client.get_product_history(product.business_partner_id, product.product_id)
        product.set_history({entry['d']: entry['v'] for entry in res["history"]})
        product.set_deposit({entry['d']: entry['v'] for entry in res["rendite"]})
        export_csv_history(product)
        logging.info('Successfully exported data from %s', product)
    # get transactions
    from_date_str = input("Enter start date for transactions to "
                          "export (DD.MM.YYYY) or press Enter to skip: ")
    if from_date_str:
        try:
            day_count = (datetime.now() - datetime.strptime(from_date_str, '%d.%m.%Y')).days
            logging.debug('User entered start date %s, '
                          'which is %d days ago', from_date_str, day_count)
            if day_count < 1:
                logging.error('Start date must be in the past')
                end_program(1)
            for bp_id in business_partner_ids:
                logging.debug('Fetching transactions for business partner id %s', bp_id)
                transactions = client.get_transactions(bp_id, day_count=day_count)
                export_csv_transactions(transactions, bp_id)
                logging.info('Successfully exported %d transactions for business '
                             'partner id %s', len(transactions), bp_id)
        except ValueError:
            logging.error('Invalid date format. Please use DD.MM.YYYY')
            end_program(1)

    # get postbox items
    now = datetime.now()
    three_months_ago = now - timedelta(days=90)
    from_date = three_months_ago.strftime('%Y-%m-%d')
    to_date = now.strftime('%Y-%m-%d')
    postbox_items = client.get_postbox_items(status='UNREAD', from_date=from_date, to_date=to_date)
    if len(postbox_items) > 0:
        logging.info('Found %d unread postbox items', len(postbox_items))
        input_str = input("Do you want to download the documents? (y/n): ")
        if input_str.lower() != 'y':
            logging.info('User chose not to download documents')
        end_program(0)
    else:
        logging.info('No unread postbox items found')
        end_program(0)
    # download postbox documents
    for item in postbox_items:
        logging.debug('Fetching and downloading data from %s', item['displayName'])
        res = client.get_postbox_document(item['id'])
        save_postbox_document(item, res)
        logging.info('Successfully downloaded and saved document from %s', item['displayName'])
    logging.info('Successfully downloaded %d documents', len(postbox_items))
    end_program(0)
