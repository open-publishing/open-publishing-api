"""Unit tests for testing record reference service."""
import os
import uuid
from unittest import TestCase
from random import randint
from nose.plugins.attrib import attr
import open_publishing as op
import requests


class TestAuthentification(TestCase):
    """Simple Test."""
    HREF = '/rpc/record_reference'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'NG_DEVNAME' not in os.environ:
            raise Exception("APIHOST not set in environment.")
        self.api_host = 'api.{}.dev.openpublishing.com'.format(os.environ['NG_DEVNAME'])

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @attr("simple")
    def test_record_reference(self):
        """Test writing and reading record reference value."""
        record_reference = self.create_random_record_reference()
        ean = self.create_random_ean()
        app_name = self.create_random_app_name()
        self.store_record_reference(ean, app_name, record_reference)
        self.assertEqual(record_reference, self.get_record_reference(ean, app_name))

    @attr("simple")
    def get_url(self):
        """Returns url of Record Reference service."""
        return 'https://' + self.api_host + self.HREF

    @attr("simple")
    def authenticate(self):
        """Authenticate as an app."""
        with op.context(host=self.api_host) as ctx:
            ctx.auth(app_id=100, app_secret="app-secret-100")
            return ctx.auth_context.auth_token

    @attr("simple")
    def store_record_reference(self, ean, app_name, record_reference):
        """Method to send the record reference to service in order to store it."""
        auth_token = self.authenticate()
        headers = {'Authorization': 'Bearer ' + auth_token}
        params = {'method': 'store',
                  'ean': ean,
                  'record_reference': record_reference,
                  'app_name': app_name,
                  'log': 'Test Record reference'}
        response = requests.post(self.get_url(), headers=headers, params=params)
        self.assertEqual(response.status_code, 200)

    @attr("simple")
    def get_record_reference(self, ean, app_name):
        """Method to request the record reference from the service."""
        auth_token = self.authenticate()
        headers = {'Authorization': 'Bearer ' + auth_token}
        params = {'method': 'get',
                  'ean': ean,
                  'app_name': app_name}
        response = requests.get(self.get_url(), headers=headers, params=params)
        self.assertEqual(response.status_code, 200)
        return response.json()['result']['record_reference']

    @staticmethod
    def create_random_ean():
        """Creates a random ean."""
        return '978' + ''.join(["%s" % randint(0, 9) for num in range(0, 10)])

    @staticmethod
    def create_random_record_reference():
        """Creates a random record reference."""
        return uuid.uuid4().hex

    @staticmethod
    def create_random_app_name():
        """Creates a random app name."""
        return uuid.uuid4()
