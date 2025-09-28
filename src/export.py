"""Export module"""
from datetime import datetime
import logging
import os
import base64


def create_dir_if_not_exists(path):
    """Create directory if it does not exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.debug('Created directory %s', path)


def export_csv_history(p):
    """Export product history to csv file"""
    direction = 'output'
    create_dir_if_not_exists(direction)

    with open(f'{direction}/output_{p.name}.csv', 'w', encoding='UTF-8') as f:
        f.write('Datum;Kurs;Höchst;Tiefst;Umsatz\n')
        prev = 0
        for date, value in p.history.items():
            if date not in p.deposit:
                continue
            value = value / p.deposit[date] * 100
            if value == prev:
                continue
            date = datetime.strptime(date, "%Y-%m-%d").strftime('%d.%m.%Y')
            value_str = f'{value:.3f}'.replace('.', ',')
            f.write(f'{date};{value_str};;;\n')
            prev = value


def export_csv_transactions(transactions, bp_id):
    """Export transactions to csv file"""
    direction = 'output'
    create_dir_if_not_exists(direction)

    with open(f'{direction}/output_Verrechnungskonto_{bp_id}.csv', 'w', encoding='UTF-8') as f:
        f.write('Buchungsdatum;Wertstellungsdatum;Betrag;Verwendungszweck\n')
        for transaction in transactions:
            booking_date = datetime.strptime(transaction['bookingDate'], "%Y-%m-%d"
                                             ).strftime('%d.%m.%Y')
            value_date = datetime.strptime(transaction['valutaDate'], "%Y-%m-%d"
                                           ).strftime('%d.%m.%Y')
            amount = f"{transaction['amount']:.2f}".replace('.', ',')
            order_type = transaction['orderType']
            if '(' in order_type:
                order_type_str = order_type.split('(')[0][:-1]
            else:
                order_type_str = order_type
            purpose = (f"{transaction['type']} - {order_type_str}"
                       f" - {transaction['Verwendungszweck']}")
            f.write(f'{booking_date};{value_date};{amount};{purpose}\n')


def save_postbox_document(document_item, content):
    """Save postbox document to file"""
    directory = 'output/documents'
    create_dir_if_not_exists(directory)

    pdf_bytes = base64.b64decode(content)
    with open(f"{directory}/{document_item['fileName']}", 'wb') as f:
        f.write(pdf_bytes)
        logging.debug('Saved document %s', document_item['displayName'])
