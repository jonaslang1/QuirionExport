"""Export module"""
from datetime import datetime
import logging
import os
import base64


def export_csv(p):
    """Export product history to csv file"""
    direction = 'output'
    if not os.path.exists(direction):
        os.makedirs(direction)
        logging.debug('Created directory %s', direction)

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


def save_postbox_document(document_item, content):
    """Save postbox document to file"""
    directory = 'output/documents'
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.debug('Created directory %s', directory)

    pdf_bytes = base64.b64decode(content)
    with open(f"{directory}/{document_item['fileName']}", 'wb') as f:
        f.write(pdf_bytes)
        logging.debug('Saved document %s', document_item['displayName'])
