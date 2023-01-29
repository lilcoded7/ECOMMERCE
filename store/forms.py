from django import forms 
from .models import Customer
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 



class RegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter username',
                'type'       : 'text',
                'class'      : 'form-control'
            }
        )
    )


    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter email',
                'type'       : 'text',
                'class'      : 'form-control'
            }
        )
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter password',
                'type'       : 'password',
                'class'      : 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'confirm password',
                'type'       : 'password',
                'class'      : 'form-control'
            }
        )
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']



class loginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'username/email',
                'type'       : 'text',
                'class'      : 'form-control'
            }
        )
    )

    password1  = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter password',
                'type'       : 'password',
                'class'      : 'form-control'
            }
        )
    )

    

   
class VerifyForm(forms.Form):
    code = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter verification code',
                'type'       : 'text',
                'class'      : 'form-control'
            }
        )
    )
    