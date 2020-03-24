from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifiers
    for authentication.
    """
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given username and password.
        """
        if not username:
            raise ValueError(_('The username(employee_id) must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        max_length=100
    )
    email = models.EmailField(_('email address'))
    location = models.CharField(_('location'), max_length=100)
    chinese_name = models.CharField(_('chinese_name'), max_length=50)
    english_name = models.CharField(_('english_name'), max_length=50)
    display_name = models.CharField(_('display_name'), max_length=50)
    extension = models.CharField(_('extension'), max_length=30)
    is_staff = models.BooleanField(
        _('staff_status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    joined_time = models.DateTimeField(_('joined time'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('custom_user')
        verbose_name_plural = _('custom_users')
        abstract = False

    def __str__(self):
        return f'{self.username}<{self.display_name}>'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_username(self):
        """
        Return the employee_id of the user.
        Ex/ 10612704
        """
        return self.username

    def get_chinese_name(self):
        """
        Return the chinese name of the user.
        Ex/ 王大明
        """
        return self.chinese_name

    def get_english_name(self):
        """
        Return the english name of the user.
        Ex/ Jeff SH Wang
        """
        return self.english_name

    def get_email(self):
        """
        Return the email of the user.
        Ex/ jeff_sh_wang@wistron.com
        """
        return self.email

    def get_display_name(self):
        """
        Return the display name of the user.
        Ex/ Jeff SH Wang/WHQ/Wistron
        """
        return self.display_name

    def get_location(self):
        """
        Return the location of the user.
        Ex/ Neihu W-3F W1W2
        """
        return self.location

    def get_joined_time(self):
        """
        Return the joined time of the user ( format --> iso8601 ).
        Ex/ 2020-03-20T01:56:24.864240Z
        """
        return self.joined_time

    def get_last_login(self):
        """
        Return the last login time of the user ( format --> iso8601 ).
        Ex/ 2020-03-20T01:56:24.864240Z
        """
        return self.last_login

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
