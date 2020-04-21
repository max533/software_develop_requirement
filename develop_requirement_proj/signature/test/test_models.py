""" Signature Model Test """
from django.test import TestCase

from ..models import Account


class AccountModelTestCase(TestCase):
    """ Account Model Test Case"""
    def setUp(self):
        """ Setup test environment """
        print(self.id())
        account_info = {
            "id": 20,
            "name": "WT-EBG",
            "code": "WT-EBG",
            "business_unit": None,
            "project_count": '1'
        }
        self.select_account = Account(**account_info)

    def test_model_str(self):
        """ Test Account Model string """
        self.assertEqual(self.select_account.__str__(), '20 : WT-EBG')

    def test_model_repr(self):
        """ Test Account Model representation """
        self.assertEqual(self.select_account.__repr__(), 'Account(20, WT-EBG, WT-EBG, None, 1)')
