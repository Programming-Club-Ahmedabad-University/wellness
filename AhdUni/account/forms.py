from django import forms

from .models import (Account, UserDetails, GENDER_CHOICES, CATEGORY_JUNK,
                     CATEGORY_MED, CATEGORY_REASON, CATEGORY_SG,
                     CATEGORY_WP, CATEGORY_MC)


class UserDetailsForm(forms.Form):
    """
        Form to collect and update user details
    """

    age = forms.IntegerField(label='Age', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Your Age'}
    ))
    height = forms.IntegerField(label='Height', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Height in cm'}
    ))
    current_weight = forms.IntegerField(label='Weight', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Weight in kg'}
    ))
    daily_water = forms.IntegerField(label='Water Consumption(Glasses per day)',
    	widget=forms.NumberInput(attrs={'class': 'form-control mb-3 fields',
        'autocomplete': 'off', 'placeholder': 'Daily consumption in glasses'}
    ))
    workout_patterns = forms.MultipleChoiceField(label='Workout-pattern',
    	choices=CATEGORY_WP, widget=forms.SelectMultiple(attrs={
        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
        'placeholder': 'Your workout pattern'}
    ))
    reason = forms.MultipleChoiceField(label='Source of motivation',
    	choices=CATEGORY_REASON, widget=forms.SelectMultiple(attrs={
        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
        'placeholder': 'Your Motivation'}
    ))
    set_goal = forms.ChoiceField(label='Goal to reduce(in kgs)', 
        choices=CATEGORY_SG, widget=forms.Select(attrs={
        'class': 'form-control mb-3 fields','autocomplete': 'off', 
        'placeholder': 'Weight-reduction in kg'}
    ))
    menstural_cycle = forms.ChoiceField(label='Menstrual Cycle(No.of days)',
		choices=CATEGORY_MC ,widget=forms.Select(
		attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 
        'placeholder': 'Menstrual Cycle', 'required': False}
    ))
    ongoing_med = forms.ChoiceField(label='Ongoing Medicines',
        choices=CATEGORY_MED, widget=forms.Select(attrs={
        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
        'placeholder': 'Ongoing Medicines'}
    ))
    ongoing_med_reason = forms.CharField(label='Reason for ongoing medicines',
        widget=forms.TextInput(attrs={'required': False, 
        'class': 'form-control mb-3 fields', 'autocomplete': 'off', 
        'placeholder': 'Reason for Medicine'}
    ))
    hours_sleep = forms.IntegerField(label='Sleep', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Sleep in hrs'}
    ))
    smoking = forms.IntegerField(label='Smoking', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Consumption in a day'}
    ))
    alcohol = forms.IntegerField(label='Alcohol', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Consumption in a month'}
    ))
    junkfood = forms.ChoiceField(label='Junkfood', choices=CATEGORY_JUNK, 
        widget=forms.Select(attrs={'class': 'form-control mb-3 fields', 
        'autocomplete': 'off', 'placeholder': 'Weekly Consumption'}
    ))

    class Meta:
        fields = '__all__'


class RegisterForm(forms.Form):

    full_name = forms.CharField(label='Fullname', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Fullname'}
    ))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3 fields',
               'autocomplete': 'off', 'placeholder': 'Email'}
    ))
    enrollment_number = forms.CharField(label='Enrollment Number', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Enrollment No. (eg 1841005)'}
    ))
    contact_number = forms.IntegerField(label='Contact Number', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields',
               'autocomplete': 'off', 'placeholder': 'Contact No.'}
    ))
    programme = forms.CharField(label='Programme', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Programme'}
    ))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control mb-3 fields',
        'autocomplete': 'off', 'placeholder': 'Gender'}
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 'id': 'password',
               'placeholder': 'Password'}
    ))

    class meta:
        fields = '__all__'


class LoginForm(forms.Form):

    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Email'}
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off', 
        'id': 'password', 'placeholder': 'Password'}
    ))

    class meta:
        fields = '__all__'
