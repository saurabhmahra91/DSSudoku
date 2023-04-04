from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", min_length=6, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class SigninForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(SigninForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
