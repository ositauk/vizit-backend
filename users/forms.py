from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from.models import profile


# Login Authentication Form
class User_form(AuthenticationForm):
    pass


# Registration Form
class User_creation(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    role = forms.CharField(label='Role')
    # user_id = forms.CharField(label='UserID')

    class Meta:
        model = User
        fields = ['username', 'role', 'first_name', 'email']
        labels = {'first_name': 'Name'}


# USer Update Form
class update_user(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['role', 'fname', 'email']
        labels = {'fname': 'Name'}


# User Name Form
class update_user_info(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']   # 'password'
