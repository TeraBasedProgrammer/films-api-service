import logging

from rest_framework.serializers import ValidationError

logger = logging.getLogger('logger')


def validate_age(value):
    if not 0 <= value <= 120:
        validation_error_message = 'Age must be from 0 to 120'
        logger.warning(f'Validation error - "{validation_error_message}"')
        raise ValidationError(validation_error_message)
    return value
