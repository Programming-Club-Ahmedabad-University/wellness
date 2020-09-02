from django import forms

from .models import (Account, UserDetails, GENDER_CHOICES, CATEGORY_JUNK,
                     CATEGORY_MED, CATEGORY_REASON, CATEGORY_SG,
                     CATEGORY_WI, CATEGORY_WP)

# age = models.IntegerField()
#     height = models.IntegerField()
#     current_weight = models.IntegerField()
#     goal = models.CharField(max_length=200, choices=CATEGORY_SG)
#     workout_pattern = MultiSelectField(choices=CATEGORY_WP)
#     water_consumption = models.CharField(max_length=200, choices=CATEGORY_WI)
#     # current_diet
#     motivation = MultiSelectField(max_length=200, choices=CATEGORY_REASON)
#     ongoing_med = models.CharField(max_length=200, choices=CATEGORY_MED)
#     ongoing_med_reason = models.CharField(max_length=200, null=True)
#     menstural_cycle = models.CharField(max_length=200, null=True)
#     hours_sleep = models.IntegerField()
#     smoking = models.IntegerField()  # how many times a day
#     alcohol = models.IntegerField()  # how many times a month
#     junkfood


class UserDetailsForm(forms.Form):
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Your Age'}
    ))
    height = forms.IntegerField(label='Height', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Height in cm'}
    ))
    weight = forms.IntegerField(label='Weight', widget=forms.NumberInput(
        attrs={'class': 'form-control mb-3 fields', 'autocomplete': 'off',
               'placeholder': 'Weight in kg'}
    ))
    water_consumption = forms.ChoiceField(label='Water Consumption',
    	choices=CATEGORY_WI, widget=forms.Select(attrs={
        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
        'placeholder': 'Daily consumption in litres'}
    ))
    workout_pattern = forms.MultipleChoiceField(label='Workout-pattern',
    	choices=CATEGORY_WP, widget=forms.SelectMultiple(attrs={
        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
        'placeholder': 'Your workout pattern'}
    ))
    motivation = forms.MultipleChoiceField(label='Motivation',
    	choices=CATEGORY_REASON, widget=forms.SelectMultiple(attrs={
        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
        'placeholder': 'Your Motivation'}
    ))
    goal = forms.ChoiceField(label='Goal', choices=CATEGORY_SG,
        widget=forms.Select(attrs={'class': 'form-control mb-3 fields',
        'autocomplete': 'off', 'placeholder': 'Weight-reduction in kg'}
    ))
    menstural_cycle = forms.CharField(label='Menstrual Cycle',
                                      widget=forms.TextInput(attrs={'class': 'form-control mb-3 fields',
                                                                    'autocomplete': 'off', 'placeholder': 'Menstrual Cycle'}
                                                             ))
    ongoing_med = forms.ChoiceField(label='Ongoing Medicines',
                                  choices=CATEGORY_MED, widget=forms.Select(attrs={
                                        'class': 'form-control mb-3 fields', 'autocomplete': 'off',
                                      'placeholder': 'Ongoing Medicines'}
                                  ))
    ongoing_med_reason = forms.CharField(label='Ongoing Medicines Reason',
                                         widget=forms.TextInput(attrs={'class': 'form-control mb-3 fields',
                                                                       'autocomplete': 'off', 'placeholder': 'Ongoing Medicines Reason'}
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
    junkfood = forms.ChoiceField(label='Junkfood',
                               choices=CATEGORY_JUNK, widget=forms.Select(attrs={
                                   'class': 'form-control mb-3 fields', 'autocomplete': 'off',
                                   'placeholder': 'Weekly Consumption'}
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
               'placeholder': 'Enrollment No.'}
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
        fields = ['full_name', 'email', 'enrollment_number',
                  'contact_number', 'programme', 'gender', 'password']


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
