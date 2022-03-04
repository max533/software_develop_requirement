from develop_requirement_proj.users.models import CustomUser

from django.test import TestCase
from django.utils.translation import gettext_lazy as _


class CustomUserModelTest(TestCase):

    def setUp(self):
        """Setup test environment"""
        content = {
            'username': 'Z10612704',
            'email': 'Wistron Stark@wistron.com',
            'location': 'Neihu W-1F W1W4',
            'chinese_name': '王大明',
            'english_name': 'David_Wang@wistron.com',
            'display_name': 'David Wang/WHQ/Wistron',
            'extension': '1788-5432'
        }
        self.user = CustomUser.objects.create(**content)

    def test_username_label(self):
        """Test username label"""
        field_label = CustomUser._meta.get_field('username').verbose_name
        self.assertEqual(field_label, _('username'))

    def test_email_label(self):
        """Test email label"""
        field_label = CustomUser._meta.get_field('email').verbose_name
        self.assertEqual(field_label, _('email address'))

    def test_location_label(self):
        """Test location label"""
        field_label = CustomUser._meta.get_field('location').verbose_name
        self.assertEqual(field_label, _('location'))

    def test_chinese_name_label(self):
        """Test chinese_name label"""
        field_label = CustomUser._meta.get_field('chinese_name').verbose_name
        self.assertEqual(field_label, _('chinese_name'))

    def test_english_name_label(self):
        """Test english_name label"""
        field_label = CustomUser._meta.get_field('english_name').verbose_name
        self.assertEqual(field_label, _('english_name'))

    def test_display_name_label(self):
        """Test display_name label"""
        field_label = CustomUser._meta.get_field('display_name').verbose_name
        self.assertEqual(field_label, _('display_name'))

    def test_extension_label(self):
        """Test extension label"""
        field_label = CustomUser._meta.get_field('extension').verbose_name
        self.assertEqual(field_label, _('extension'))

    def test_chinese_name_max_length(self):
        """Test max length of chineses_name field"""
        max_length = CustomUser._meta.get_field('chinese_name').max_length
        self.assertEqual(max_length, 50)

    def test_english_name_max_length(self):
        """Test max length of english_name field"""
        max_length = CustomUser._meta.get_field('english_name').max_length
        self.assertEqual(max_length, 50)

    def test_display_name_max_length(self):
        """Test max length of display_name field"""
        max_length = CustomUser._meta.get_field('display_name').max_length
        self.assertEqual(max_length, 50)

    def test_location_max_length(self):
        """Test max length of location field"""
        max_length = CustomUser._meta.get_field('location').max_length
        self.assertEqual(max_length, 100)

    def test_extension_max_length(self):
        """Test max length of extension field"""
        max_length = CustomUser._meta.get_field('extension').max_length
        self.assertEqual(max_length, 30)

    def test_username_max_length(self):
        """Test max length of username field"""
        max_length = CustomUser._meta.get_field('username').max_length
        self.assertEqual(max_length, 100)

    def test_string_representation(self):
        """Test string representation method"""
        expected_result = f'{self.user.username}<{self.user.display_name}>'
        self.assertEqual(expected_result, str(self.user))

    def test_get_username(self):
        """Test get_username() method"""
        self.assertEqual(self.user.username, self.user.get_username())

    def test_get_chinese_name(self):
        """Test get_chinese_name() method"""
        self.assertEqual(self.user.chinese_name, self.user.get_chinese_name())

    def test_get_english_name(self):
        """Test get_english_name() method"""
        self.assertEqual(self.user.english_name, self.user.get_english_name())

    def test_get_email(self):
        """Test get_email() method"""
        self.assertEqual(self.user.email, self.user.get_email())

    def test_get_display_name(self):
        """Test get_display_name() method"""
        self.assertEqual(self.user.display_name, self.user.get_display_name())

    def test_get_extension(self):
        """Test get_extension() method"""
        self.assertEqual(self.user.extension, self.user.get_extension())

    def test_get_joined_time(self):
        """Test get_joined_time() method"""
        self.assertEqual(self.user.joined_time, self.user.get_joined_time())

    def test_get_last_login(self):
        """Test get_last_login() method"""
        self.assertEqual(self.user.last_login, self.user.get_last_login())
