"""API module for quirion"""
import time
import logging
import requests


class APIClient:
    """API Client for quirion"""

    def __init__(self):
        """Initialize API Client"""
        self.base_url = 'https://api.it-aws-prod.quirion.de/legacy/v1'
        self.access_token = None
        self.refresh_token = None
        self.id_token = None
        self.expires_in = 0
        self.last_refresh = 0

    def rest_call(self, method, path, options=None):
        """Rest call to quirion API

        Args:
                method (str): HTTP method
                path (str): Path to call
                options (dict, optional): Additional options. Defaults to None.
                    - is_protected (bool): Whether the endpoint requires authentication.
                     Defaults to False.
                    - headers (dict): Additional headers to include in the request.
                     Defaults to None.
                    - json_data (dict): JSON data to send in the request body.
                     Defaults to None.
                    - params (dict): Query parameters to include in the request.
                     Defaults to None.
                    - timeout (int): Timeout for the request in seconds.
                     Defaults to 5.

        Returns:
            requests.Response: Response object
            """
        if options is None:
            options = {}
        is_protected = options.get('is_protected', False)
        headers = options.get('headers', None)
        json_data = options.get('json_data', None)
        params = options.get('params', None)
        timeout = options.get('timeout', 5)

        if is_protected:
            if self.access_token is None:
                logging.info("Not authenticated")
            elif time.time() - self.last_refresh > self.expires_in:
                self.fetch_new_token()

        if headers is None:
            headers = {
                'authority': 'api.it-aws-prod.quirion.de',
                'accept': '*/*',
                'content-type': 'application/json; charset=UTF-8',
            }
        if is_protected:
            headers['authorization'] = 'Bearer ' + self.id_token

        response = requests.request(
            method,
            self.base_url + path,
            headers=headers,
            json=json_data,
            params=params,
            timeout=timeout
        )
        if response.status_code >= 300:
            logging.debug('Error %s: %s', response.status_code,
                          response.text if response.text else 'Empty response body'
                          )
        response.raise_for_status()
        return response

    def fetch_token(self, username, password):
        """Fetch token from quirion API"""
        logging.debug('Fetching token for %s and password with length %s', username, len(password))
        json_data = {
            'username': username,
            'password': password,
        }

        self.last_refresh = time.time()
        response = self.rest_call(
            'POST',
            '/auth/token',
            options={'json_data': json_data}
        )
        response.raise_for_status()
        self.access_token = response.json()["AuthenticationResult"]["AccessToken"]
        self.refresh_token = response.json()["AuthenticationResult"]["RefreshToken"]
        self.id_token = response.json()["AuthenticationResult"]["IdToken"]
        self.expires_in = response.json()["AuthenticationResult"]["ExpiresIn"]

    def fetch_new_token(self):
        """Fetch new token from quirion API"""
        logging.debug('Fetching new token')
        json_data = {
            'token': self.refresh_token
        }

        response = self.rest_call(
            'POST',
            '/auth/token/refresh',
            options={'json_data': json_data}
        )
        response.raise_for_status()
        self.access_token = response.json()["AuthenticationResult"]["AccessToken"]
        self.refresh_token = response.json()["AuthenticationResult"]["RefreshToken"]
        self.id_token = response.json()["AuthenticationResult"]["IdToken"]
        self.expires_in = response.json()["AuthenticationResult"]["ExpiresIn"]

    def get_endpoints(self):
        """Get endpoints from quirion API"""
        logging.debug('Fetching endpoints')
        response = self.rest_call('GET', '/endpoints')
        return response.json()

    def get_business_partner_id(self):
        """Get business partner id from quirion API"""
        logging.debug('Fetching business partner id for user')
        response = self.rest_call('GET', '/user', options={'is_protected': True})
        return list(map(lambda elem: elem["businessPartnerId"], response.json()["businessPartner"]))

    def get_products(self, business_partner_id):
        """Get products from quirion API"""
        logging.debug('Fetching products for business partner id %s', business_partner_id)
        params = {
            'clearing': 'true',
            'products': 'true',
            'history': 'false',
            'historyYear': 'false',
            'reference': 'true',
            'users': 'false',
            'wphg': 'false',
        }

        response = self.rest_call(
            'GET',
            f'/business-partners/{business_partner_id}',
            options={'is_protected': True, 'params': params}
        )
        return response.json()["products"]

    def get_product_history(self, business_partner_id, product_id):
        """Get product history from quirion API"""
        logging.debug('Fetching product history for product id %s', product_id)
        params = {
            'liquid': 'true',
            'debit': 'false',
            'condition': 'false',
            'savingsplans': 'false',
            'transactions': 'true',
            'depotitems': 'true',
            'history': 'true',
            'historyYear': 'false',
            'wphg': 'false',
        }

        response = self.rest_call(
            'GET',
            f'/business-partners/{business_partner_id}/products/{product_id}',
            options={'is_protected': True, 'params': params}
        )
        return response.json()

    def get_postbox_items(self, status="ALL", from_date=None, to_date=None):
        """Get postbox items from quirion API"""
        logging.debug('Fetching postbox items from %s to %s', from_date, to_date)
        params = {
            'status': status,
            'from': from_date,
            'to': to_date,
        }

        response = self.rest_call(
            'GET',
            '/postbox',
            options={'is_protected': True, 'params': params},
        )
        return response.json()['documents']

    def get_postbox_document(self, document_id):
        """Get postbox document from quirion API"""
        logging.debug('Fetching postbox document with id %s', document_id)
        response = self.rest_call(
            'POST',
            '/deprecated/get-post-box-document',
            options={'is_protected': True, 'json_data': {'doc': document_id}},
        )
        return response.content

    def get_transactions(self, business_partner_id, day_count=90):
        """Get transactions from quirion API"""
        logging.debug('Fetching transactions for business partner id %s for last %s days',
                      business_partner_id, day_count)
        json_data = {
            'range': day_count,
            'status': 'ALL',
            'type': 'ALL',
            'businessPartnerId': business_partner_id,
        }

        response = self.rest_call(
            'POST',
            '/transactions',
            options={'is_protected': True, 'json_data': json_data}
        )
        return response.json()
