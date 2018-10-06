from django.core.validators import RegexValidator

user_val = RegexValidator(regex=r'^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$', message=u'Phone number must be like: +79999999999')
