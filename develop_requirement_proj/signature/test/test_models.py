""" Signature Model Test """
from django.test import TestCase

from ..models import Account, Project


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
        self.assertEqual(self.select_account.__str__(), '<Account 20 : WT-EBG>')

    def test_model_repr(self):
        """ Test Account Model representation """
        self.assertEqual(self.select_account.__repr__(), 'Account(20, WT-EBG, WT-EBG, None, 1)')


class ProjectModelTestCase(TestCase):
    """ Project Model Test Case"""
    def setUp(self):
        """ Setup test environment """
        print(self.id())
        project_info = {
            "id": 3,
            "wistron_name": None,
            "customer_name": "Anders4",
            "wistron_code": "A191TB1",
            "plm_code_1": "QRQY00000718",
            "plm_code_2": "5PD05L010001",
            "deleted_at": None,
            "name": "Anders4",
            "plm_code": "QRQY00000718",
            "type": "NPI",
            "status": "On-going",
            "product_line": "Server",
            "business_model": "JDM",
            "account": {
                "id": 2,
                "name": "HPE",
                "code": "Apollo",
                "business_unit": 2
            }
        }
        self.select_project = Project(**project_info)

    def test_model_str(self):
        """ Test Project Model string """
        self.assertEqual(self.select_project.__str__(), '<Project 3 : Anders4>')

    def test_model_repr(self):
        """ Test Project Model representation """
        self.assertEqual(
            self.select_project.__repr__(),
            (
                f"Project(3, None, Anders4, A191TB1, QRQY00000718, 5PD05L010001, "
                f"None, NPI, Anders4, QRQY00000718, On-going, Server, JDM, "
                f"{{'id': 2, 'name': 'HPE', 'code': 'Apollo', 'business_unit': 2}})"
            )
        )
