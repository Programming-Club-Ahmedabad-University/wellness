import os
from decouple import config

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q

from .forms import UserDetailsForm
from .models import UserDetails
from home.views import check_extra_details


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('home')


class ProfileView(View):
    """
        For rendering current profile and updating the profile
    """

    def get(self, request, *args, **kwargs):
        current_user = request.user
        check_extra_details(current_user)

        form = UserDetailsForm()
        current_details = dict()
        user_details = UserDetails.objects.filter(user=current_user).values()

        # If the user has already filled the details,
        # pass the data to prepoluate the form
        if len(user_details) != 0:
            for data in user_details:
                current_details = data

            current_details.pop('id')
            current_details.pop('user_id')
            form = UserDetailsForm(data=current_details)

        context = {'form': form, 'current_details': user_details}
        return render(request, 'my_auth/edit_profile.html', context)

    # Update/create the details
    def post(self, request, *args, **kwargs):
        details = None
        menstrual_cycle = None
        med_reason = None

        try:
            menstrual_cycle = request.POST.get('menstural_cycle')
        except Exception as identifier:
            pass

        try:
            med_reason = request.POST.get('med_reason')
        except Exception as identifier:
            pass

        try:
            details = UserDetails.objects.get(user=request.user)
        except Exception as identifier:
            pass

        if details is not None:
            details.delete()
        else:
            request.user.extra_details.updated_profile = True
            request.user.save()

        new_detail = UserDetails(
            birthdate			= request.POST.get('birthdate'),
            height				= request.POST.get('height'),
            weight				= request.POST.get('weight'),
            goal				= request.POST.get('goal'),
            workout_pattern		= request.POST.getlist('workout_pattern'),
            water_consumption	= request.POST.get('water_consumption'),
            reason				= request.POST.getlist('reason'),
            med					= request.POST.get('med'),
            med_reason			= med_reason,
            menstural_cycle		= menstrual_cycle,
			gender				= request.POST.get('gender'),
            sleep				= request.POST.get('sleep'),
            smoking				= request.POST.get('smoking'),
            junkfood			= request.POST.get('junkfood'),
            user				= request.user
        )
        new_detail.save()

        messages.info(request, 'Profile updated successfully')
        return redirect('home')