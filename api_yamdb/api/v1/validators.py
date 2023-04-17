from django.core.validators import RegexValidator

regexp_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    message='not valid regexp'
)
