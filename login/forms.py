from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

    def clean_email(self):
        email=self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("해당 e-mail 주소는 이미 존재합니다.")
        except User.DoesNotExist:
            return email


class UserPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email=self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise forms.ValidationError("존재하지 않는 e-mail 주소입니다.")