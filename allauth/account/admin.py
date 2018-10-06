from django.contrib import admin

from . import app_settings
from .adapter import get_adapter
from .models import EmailAddress, EmailConfirmation
from django import forms

class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'primary', 'verified')
    list_filter = ('primary', 'verified')
    search_fields = []
    raw_id_fields = ('user',)

    def get_search_fields(self, request):
        base_fields = get_adapter(request).get_user_search_fields()
        return ['email'] + list(map(lambda a: 'user__' + a, base_fields))


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'created', 'sent', 'key')
    list_filter = ('sent',)
    raw_id_fields = ('email_address',)


if not app_settings.EMAIL_CONFIRMATION_HMAC:
    admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)


username_regex_field = forms.RegexField (
        label = "Username",
        max_length = 30,
        regex = r"^[\w'\.\-@]+$",
        help_text = "Required. 30 characters or fewer. Letters, apostrophes, periods, hyphens and at signs.",
        error_message = "This value must contain only letters, apostrophes, periods, hyphens and at signs."
        )

class UserCreationForm(UserCreationForm):
    username = username_regex_field

class UserChangeForm(UserChangeForm):
    username = username_regex_field

class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
