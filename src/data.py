"""Data module"""
from datetime import datetime


class Product:
    """Product class"""

    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, name, product_id, business_partner_id, created_at):
        """Initialize product"""
        self.name = name
        self.product_id = product_id
        self.business_partner_id = business_partner_id
        self.created_at = datetime.strptime(created_at, self.format_string)
        self.history = {}
        self.deposit = {}

    def __str__(self):
        """Return string representation"""
        return f'Product(name={self.name}, ipsID={self.product_id}, created_at={self.created_at})'

    def __repr__(self):
        """Return string representation"""
        return str(self)

    def set_history(self, history):
        """Setter for history"""
        self.history = history

    def set_deposit(self, deposit):
        """Setter for deposit"""
        self.deposit = deposit
