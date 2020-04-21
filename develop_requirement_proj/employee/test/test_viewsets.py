""" Employee test """
import factory
from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.users.models import CustomUser

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase


class EmployeeViewSetTestCase(APITestCase):
    """ Test EmployeeViewSet Class """
    url_list = reverse('api:employee-list')
    url_current_user = reverse('api:employee-current-user')
    databases = {'default', 'hr'}

    def setUp(self):
        print(self.id())
        user_content = {
            'username': 'Z10612777',
            'password': 'test_123',
            'email': 'david_wang@wistron.com',
            'location': 'Neihu W-1F W1W4',
            'chinese_name': '王大明',
            'english_name': 'David Wang',
            'display_name': 'David Wang/WNH/Wistron',
            'extension': '17885432'
        }
        self.select_employee_response = {
            'employee_id': 'Z10612777',
            'extension': '17885432',
            'display_name': 'David Wang/WNH/Wistron',
            'avatar': None
        }
        self.select_employee_info = {
            "employee_id": "Z10612777",
            "chinese_name": "王大明",
            "english_name": "David Wang",
            "department_id": "ESQD200",
            "department_name": "部門中文名稱",
            "job_title": "工程師",
            "extension": "17885432",
            "mail": "david_wang@wistron.com",
            "supervisor_id": "9505005",
            "site": "WNH",
        }
        for i in range(100):
            employee_info = {
                "employee_id": factory.Faker('bothify', text='??#######').generate(),
                "chinese_name": factory.Faker('name', locale='zh_TW').generate(),
                "english_name": factory.Faker('romanized_name', locale='zh_TW').generate(),
                "department_id": factory.Faker('bothify', text='E??#00').generate(),
                "department_name": factory.Faker('company_prefix', locale='zh_TW').generate(),
                "job_title": factory.Faker('job', locale='zh_TW').generate(),
                "extension": factory.Faker('bothify', text='########').generate(),
                "mail": factory.Faker('romanized_name', locale='zh_TW').generate() + '@wistron.com',
                "supervisor_id": factory.Faker('bothify', text='??#######').generate(),
                "site": factory.Faker('bothify', text='W??').generate()[0:2]
            }
            Employee.objects.using('hr').create(**employee_info)
        self.select_employee = Employee.objects.using('hr').create(**self.select_employee_info)
        self.employee_all = Employee.objects.using('hr').all()
        self.users = CustomUser.objects.create(**user_content)
        self.client = APIClient()
        self.client.force_authenticate(user=self.users)

    def test_list(self):
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(len(response.data['rows']), 10)
        self.assertEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_query_employee_id(self):
        param = {
            'employee_id__icontains': 'Z1061277'
        }
        response = self.client.get(self.url_list, param, format="json")
        self.assertIn(self.select_employee_response, response.data['rows'])
        self.assertEqual(len(response.data['rows']), 1)
        self.assertNotEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_query_english_name(self):
        param = {
            'english_name__icontains': 'David'
        }
        response = self.client.get(self.url_list, param, format="json")
        self.assertIn(self.select_employee_response, response.data['rows'])
        self.assertEqual(len(response.data['rows']), 1)
        self.assertNotEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_query_department_id(self):
        param = {
            'department_id__icontains': 'ESQD'
        }
        response = self.client.get(self.url_list, param, format="json")
        self.assertIn(self.select_employee_response, response.data['rows'])
        self.assertEqual(len(response.data['rows']), 1)
        self.assertNotEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_query_extension(self):
        param = {
            'extension__icontains': '1788543'
        }
        response = self.client.get(self.url_list, param, format="json")
        self.assertIn(self.select_employee_response, response.data['rows'])
        self.assertEqual(len(response.data['rows']), 1)
        self.assertNotEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_query_site(self):
        param = {
            'site': 'WNH'
        }
        response = self.client.get(self.url_list, param, format="json")
        self.assertIn(self.select_employee_response, response.data['rows'])
        self.assertEqual(len(response.data['rows']), 1)
        self.assertNotEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_pageination(self):
        param = {
            'page': 3,
            'page_size': 20
        }
        response = self.client.get(self.url_list, param, format="json")
        self.assertEqual(response.data['total'], len(self.employee_all))
        self.assertEqual(response.data['totalNotFilter'], len(self.employee_all))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_user(self):
        response = self.client.get(self.url_current_user, format="json")
        self.assertEqual(response.data, self.select_employee_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
