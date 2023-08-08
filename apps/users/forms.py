from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm)

# internals
from apps.users.models import Profile

User = get_user_model()


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _("Email")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _("Email")
        self.fields['first_name'].label = _("Firstname")
        self.fields['last_name'].label = _("Lastname")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        required_fields = ["username", "email"]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about'].label = _("About")
        self.fields['phone'].label = _("Phone")
        self.fields['phone'].error_messages['invalid'] = _(
            "Phone number format is wrong. Example format 5554443322"
            )

    class Meta:
        model = Profile
        fields = ["about", "phone"]
        required_fields = ["phone"]


class ProfileUpdateForm(ProfileForm):
    pass


class ProfileCreationForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs['placeholder'] = _(
            "Example 5554442344")

    class Meta:
        model = Profile
        fields = ["phone", "about"]


class SearchForm(forms.Form):
    query = forms.CharField()
