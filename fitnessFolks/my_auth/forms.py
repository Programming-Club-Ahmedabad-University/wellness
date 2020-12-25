from django import forms

from .models import (GENDER, JUNK,
                     MEDICINES, REASON, GOAL,
                     WORKOUT, MENSTRUAL_CYCLE)


class UserDetailsForm(forms.Form):
    """
        Form to collect and update user details
    """
    birthdate = forms.IntegerField(label='Birth Date*', widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Your Birth Date'}
    ))
    height = forms.IntegerField(label='Height(in cm)*', widget=forms.NumberInput(
        attrs={'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Height in cm'}
    ))
    weight = forms.IntegerField(label='Weight(in kg)*', widget=forms.NumberInput(
        attrs={'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Weight in kg'}
    ))
    water_consumption = forms.IntegerField(label='Water Consumption(Glasses per day)*',
        widget=forms.NumberInput(attrs={'class': 'mb-3',
        'class': 'form-control fields', 'autocomplete': 'off', 
        'placeholder': 'Daily consumption in glasses'}
    ))
    workout_pattern = forms.MultipleChoiceField(label='Workout-pattern*',
        choices=WORKOUT, widget=forms.SelectMultiple(attrs={
        'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Your workout pattern'}
    ))
    reason = forms.MultipleChoiceField(label='Source of motivation*',
        choices=REASON, widget=forms.SelectMultiple(attrs={
        'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Your source of Motivation'}
    ))
    goal = forms.ChoiceField(label='Goal to reduce(in kgs)*',
        choices=GOAL, widget=forms.Select(attrs={
        'class': 'mb-3', 'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Your goal in kg'}
    ))
    gender = forms.ChoiceField(label='Gender*',
        choices=GENDER, widget=forms.Select(attrs={
        'class': 'mb-3', 'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Your gender'}
    ))
    menstural_cycle = forms.ChoiceField(label='Menstrual Cycle(No.of days)*',
        choices=MENSTRUAL_CYCLE, widget=forms.Select(
        attrs={'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Menstrual Cycle in days', 'required': False}
    ))
    med = forms.ChoiceField(label='Ongoing Medicines*',
        choices=MEDICINES, widget=forms.Select(attrs={
        'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Ongoing Medicines'}
    ))
    sleep = forms.IntegerField(label='Sleep(in hrs)*', widget=forms.NumberInput(
        attrs={'class': 'form-control fields', 'autocomplete': 'off',
               'placeholder': 'Sleep in hrs'}
    ))
    smoking = forms.IntegerField(label='Smoking(times per day)*', widget=forms.NumberInput(
        attrs={'class': 'form-control fields', 'autocomplete': 'off',
               'placeholder': 'Consumption in a day'}
    ))
    junkfood = forms.ChoiceField(label='Junkfood*', choices=JUNK,
        widget=forms.Select(attrs={'class': 'form-control fields',
        'autocomplete': 'off', 'placeholder': 'Weekly Consumption'}
    ))
    med_reason = forms.CharField(label='Reason for ongoing medicines',
        widget=forms.TextInput(attrs={'required': False,
        'class': 'form-control fields', 'autocomplete': 'off',
        'placeholder': 'Reason for Medicine'}
    ))

    class Meta:
        fields = '__all__'
