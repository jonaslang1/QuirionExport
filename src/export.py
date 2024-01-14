"""Export module"""
from datetime import datetime
import logging
import os


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
