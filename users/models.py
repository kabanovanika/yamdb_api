from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """
    This is custom class for create User model, where email field instead
    username field.
    """

    username = models.CharField(_('username'),
                                max_length=30,
                                blank=True,
                                unique=True)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
    confirmation_code = models.CharField(max_length=10, default='FOOBAR')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    @property
    def is_admin(self):
        """
        Function for quick change property 'role' of User model.
        """
        return (self.role == UserRoles.ADMIN or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        """
        Function for quick change property 'role' of User model.
        """
        return self.role == UserRoles.MODERATOR

    def get_full_name(self):
        """
        Function for concatinate full name of user, use firlst and last name.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
