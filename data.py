from datetime import datetime


class Product:
    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, name, product_id, business_partner_id, created_at):
        self.name = name
        self.product_id = product_id
        self.business_partner_id = business_partner_id
        self.created_at = datetime.strptime(created_at, self.format_string)
        self.history = {}
        self.deposit = {}

    def __str__(self):
        return f'Product(name={self.name}, ipsID={self.product_id}, created_at={self.created_at})'

    def __repr__(self):
        return str(self)

    def set_history(self, history):
        self.history = history

    def set_deposit(self, deposit):
        self.deposit = deposit
