from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=16, min_length=8)

    def clean(self):
        super(LoginForm, self).clean()
        if self.cleaned_data.get("email") and self.cleaned_data.get("password"):
            user = authenticate(username=self.cleaned_data["email"], password=self.cleaned_data["password"])
            if not user:
                self.add_error('email', 'Email or password is invalid')
                        