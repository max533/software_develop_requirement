""" Signature ViewSet Test """
from develop_requirement_proj.users.models import CustomUser

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase


class AccountViewSetTestCase(APITestCase):
    """ Account Resource Test Case """
    list_url = reverse('api:account-list')

    def setUp(self):
        """ Setup test environment """
        print(self.id())
        self.select_account_response = {
            "id": 20,
            "name": "WT-EBG",
            "code": "WT-EBG",
            "business_unit": None,
            "project_count": 1
        }
        self.users_content = {
            'username': 'Z10612777',
            'password': 'test_123',
            'email': 'david_wang@wistron.com',
            'location': 'Neihu W-1F W1W4',
            'chinese_name': '王大明',
            'english_name': 'David Wang',
            'display_name': 'David Wang/WNH/Wistron',
            'extension': '17885432'
        }
        self.users = CustomUser.objects.create(**self.users_content)
        self.client = APIClient()
        self.client.force_login(self.users)

    def test_list(self):
        """ test account resource with `list` action """
        response = self.client.get(self.list_url, format='json')
        self.assertIn(self.select_account_response, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
