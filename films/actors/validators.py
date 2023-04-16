from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator


def validate_name(value):
    language_validator = RegexValidator(
        regex=r'^[A-Za-zА-Яа-яЇїІіЄєҐґ\',\- ]+$',
        message='Text format is not allowed',
    )

    try:
        language_validator(value)
    except ValidationError as e:
        raise ValidationError(e.message, code='invalid_text')


def validate_age(value):
    if not 0 <= value <= 120:
        raise ValidationError('Age must be from 0 to 120')
    return value
