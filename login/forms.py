from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def clean_email(self):
        email=self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("해당 e-mail 주소는 이미 존재합니다.")
        except User.DoesNotExist:
            return email
    


            


##, "first_name", "last_name"