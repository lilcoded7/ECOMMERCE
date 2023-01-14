from django import forms 
from .models import Customer





class registerForm(forms.ModelForm):
    name = forms.CharField(
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

    password = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Enter password',
                'type'       : 'password',
                'class'      : 'form-control'
            }
        )
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Confirm password',
                'type'       : 'password',
                'class'      : 'form-control'
            }
        )
    )

    class Meta:
        model = Customer
        fields = ['name', 'email', 'password', 'confirm_password']


  


class loginForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'username/email',
                'type'       : 'text',
                'class'      : 'form-control'
            }
        )
    )

    password = forms.CharField(
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
    