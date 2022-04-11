from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from mathchamp.accounts.managers import CustomUserManager

GRADE_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
)


def characters_validator(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError("Ensure this value contains only letters.")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_student = models.BooleanField(
        default=False,
    )
    is_teacher = models.BooleanField(
        default=False,
    )
    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


class Student(models.Model):
    FIRST_NAME_MAX_LEN = 20
    FIRST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 20
    LAST_NAME_MIN_LEN = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            characters_validator,
            MinLengthValidator(FIRST_NAME_MIN_LEN),
        ),
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            characters_validator,
            MinLengthValidator(LAST_NAME_MIN_LEN),
        ),
        null=True,
        blank=True,
    )

    image = models.ImageField(
        null=True,
        blank=True,
        default='default_profile_pic.jpeg',
        upload_to='mediafiles/',
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    grade = models.CharField(
        max_length=2,
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Teacher(models.Model):
    FIRST_NAME_MAX_LEN = 20
    FIRST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 20
    LAST_NAME_MIN_LEN = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            characters_validator,
            MinLengthValidator(FIRST_NAME_MIN_LEN),
        ),
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            characters_validator,
            MinLengthValidator(LAST_NAME_MIN_LEN),
        ),
        null=True,
        blank=True,
    )

    image = models.ImageField(
        null=True,
        blank=True,
        default='default_profile_pic.jpeg',
        upload_to='mediafiles/',
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
