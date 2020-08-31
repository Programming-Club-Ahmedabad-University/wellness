from django import forms

from .models import Account
from django.forms import ModelForm
from .models import User_Details




class User_DetailsForm(ModelForm):
    class Meta:
        model = User_Details
        fields = '__all__'



gender_choices =( 
    ("1", "male"), 
    ("2", "female"), 
    ("3", "rather not say"), 
)

class RegisterForm(forms.Form):
    full_name = forms.CharField(label='Fullname', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Fullname'}
    ))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 'placeholder': 'Email'}
    ))
    enrollment_number = forms.CharField(label='Enrollment Number', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Enrollment No.'}
    )) 
    contact_number = forms.IntegerField(label='Contact Number', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 'placeholder': 'Contact No.'}
    ))
    programme = forms.CharField(label='Programme', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Programme'}
    ))
    gender = forms.ChoiceField(label='Gender', choices=gender_choices,
        widget=forms.Select(attrs={'class': 'form-control mb-3 fields', 
        'autocomplete': 'off', 'placeholder': 'Gender'}
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 'id': 'password',
               'placeholder': 'Password'}
    ))

    class meta:
        fields = ['full_name', 'email', 'enrollment_number',
            'contact_number', 'programme', 'gender', 'password' ]

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Email'}
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 'id': 'password',
               'placeholder': 'Password'}
    ))

    class meta:
        fields = ['email', 'password']