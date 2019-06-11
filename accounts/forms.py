""" from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib import auth
from accounts.models import User


class  UserCreateForm(UserCreationForm):

    class Meta():
        fields = ['username', 'password1', 'password2']
        model = User """



from django import forms
from .import models
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))    

class AddUserForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ['username', 'password']

        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus'}),
            }


class AddGovUserForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ['username', 'email','password']

        widgets = {'password': forms.PasswordInput(attrs={'class':'form-control'}),
                'username':forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus'})
            }


class AddVoterForm(forms.ModelForm):

    class Meta():
        model = models.Voter
        exclude = ['user']

        widgets = {
            'phone_num': forms.NumberInput(attrs={'class':'form-control', 'autofocus':'autofocus'}),
            'booth_no': forms.NumberInput(attrs={'class':'form-control'}),
            'cons_no': forms.NumberInput(attrs={'class':'form-control'}),
        }


class AddGovPhoneForm(forms.ModelForm):

    class Meta():
        model = models.GovUser
        fields = ['phone_num']
        widgets = {
            'phone_num': forms.NumberInput(attrs={'class':'form-control', 'autofocus':'autofocus'})
        }

class OtpForm(forms.Form):
    otp = forms.IntegerField(widget=forms.PasswordInput(attrs={'class':'form-control', 'autofocus':'autofocus'}))


class ConstituencyForm(forms.ModelForm):

    class Meta():
        model = models.Constituency
        fields = '__all__'

        widgets = {
            'id': forms.NumberInput(attrs={'class':'form-control', 'autofocus':'autofocus'}),
            'booth': forms.NumberInput(attrs={'class':'form-control'}),
        }

class UpdateConstituencyForm(forms.Form):
    id = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'autofocus':'autofocus'}))
    booth = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))


class ComplaintTypeForm(forms.ModelForm):

    class Meta():
        model = models.ComplaintType
        fields = '__all__'

        widgets = {
            'type': forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus'}),
            
        }




    
    

