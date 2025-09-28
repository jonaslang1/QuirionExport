"""Main module"""
import logging
import os
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


def main():
    """Main function"""
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
        if not client.fetch_token(username, pw):
            mfa_code = input('MFA code:')
            client.handle_mfa(mfa_code, username)
    except HTTPError as error:
        logging.error('Error fetching token: %s', error)
        end_program(1)
    logging.info('Successfully fetched access token')
    business_partner_ids = client.get_business_partner_id()
    products = get_products(business_partner_ids, client)
    get_product_history(client, products)
    get_transactions(business_partner_ids, client)
    postbox_items = get_postbox_items(client)
    download_postbox_documents(client, postbox_items)

    end_program(0)


def get_products(business_partner_ids: list, client: APIClient):
    """Get products for all business partner ids"""
    products = []
    for bp_id in business_partner_ids:
        res = client.get_products(bp_id)
        for product in res:
            products.append(
                Product(product["name"], product["ipsId"], bp_id, product["createdAt"])
            )
    return products


def get_product_history(client: APIClient, products: list):
    """Get product history for all products"""
    for product in products:
        logging.debug('Fetching and exporting data from %s', product)
        res = client.get_product_history(product.business_partner_id, product.product_id)
        product.set_history({entry['d']: entry['v'] for entry in res["history"]})
        product.set_deposit({entry['d']: entry['v'] for entry in res["rendite"]})
        export_csv_history(product)
        logging.info('Successfully exported data from %s', product)


def get_transactions(business_partner_ids: list, client: APIClient):
    """Get transactions for all business partner ids"""
    for bp_id in business_partner_ids:
        logging.debug('Fetching transactions for business partner id %s', bp_id)

        # Check if file exists and get its modification time
        file_path = f'output/output_Verrechnungskonto_{bp_id}.csv'
        if os.path.exists(file_path):
            modification_time = os.path.getmtime(file_path)
            modification_date = datetime.fromtimestamp(modification_time)
            day_count = (datetime.now() - modification_date).days
            logging.info('Transaction file for business partner id %s already exists. '
                         'Last modified %s (%d days ago).',
                         bp_id, modification_date.strftime('%Y-%m-%d'), day_count)
            input_str = input("Do you want to export transactions "
                              "since last time exporting? (y/n): ")
            if input_str.lower() != 'y':
                logging.info('User chose not to export transactions '
                             'for business partner id %s', bp_id)
                continue
        else:
            from_date_str = input("Enter start date for transactions to "
                                  "export (DD.MM.YYYY) or press Enter to skip: ")
            if not from_date_str:
                logging.info('User chose not to export transactions '
                             'for business partner id %s', bp_id)
            try:
                day_count = (datetime.now() - datetime.strptime(from_date_str, '%d.%m.%Y')).days
            except ValueError:
                logging.error('Invalid date format. Please use DD.MM.YYYY')
                continue
            logging.debug('User entered start date %s, '
                          'which is %d days ago', from_date_str, day_count)

        if day_count < 1:
            logging.error('Start date must be in the past')
            continue

        transactions = client.get_transactions(bp_id, day_count=day_count)
        if len(transactions) == 0:
            logging.info('No transactions found for business partner '
                         'id %s in the last %d days', bp_id, day_count)
            continue

        export_csv_transactions(transactions, bp_id)
        logging.info('Successfully exported %d transactions for business '
                     'partner id %s', len(transactions), bp_id)


def get_postbox_items(client: APIClient):
    """Get unread postbox items from the last three months"""
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
    return postbox_items


def download_postbox_documents(client: APIClient, postbox_items):
    """Download postbox documents"""
    for item in postbox_items:
        logging.debug('Fetching and downloading data from %s', item['displayName'])
        res = client.get_postbox_document(item['id'])
        save_postbox_document(item, res)
        logging.info('Successfully downloaded and saved document from %s', item['displayName'])
    logging.info('Successfully downloaded %d documents', len(postbox_items))


if __name__ == '__main__':
    try:
        main()
    except Exception as e: # pylint: disable=broad-except
        logging.critical('Unhandled exception: %s', e, exc_info=True)
        end_program(1)
