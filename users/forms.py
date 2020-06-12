from django import forms


class PasswordForm(forms.Form):
     password = forms.CharField(max_length=16, min_length=8)
     confirm_password = forms.CharField(max_length=16, min_length=8)

     def clean(self):
        super(PasswordForm, self).clean()
        if self.cleaned_data.get("password") and self.cleaned_data.get("confirm_password"):
            if self.cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
                 self.add_error('confirm_password', 'Passwords must match')
        
