""" Signature ViewSet Test """
from develop_requirement_proj.users.models import CustomUser

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase


class OptionViewTestCase(APITestCase):
    """ Option Resource Test Case """
    url = reverse('api:option')

    def setUp(self):
        """ Setup test environment """
        print(self.id())
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
        self.client.force_authenticate(self.users)

    def test_view_without_parameter(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
