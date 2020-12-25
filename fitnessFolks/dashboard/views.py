import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from .models import DailyUpdates, WeeklyUpdates
from my_auth.models import UserDetails


def find_avg(some_dict):
    return (0 if len(some_dict) == 0
            else sum(some_dict.values()) / len(some_dict))


class DashboardView(View):
    """
        To get updates and display graphs
    """

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            context = {
                'error_message': 'You must login before viewing this page.'}
            return render(request, 'error.html', context)

        daily_updates = request.user.daily_updates.all()
        weekly_updates = request.user.weekly_updates.all()
        workout_dict = dict()
        water_consumption_dict = dict()
        weight_dict = dict()

        for update in daily_updates:
            workout_dict[str(update.pk)] = update.workout
            water_consumption_dict[str(update.pk)] = update.water_consumption

        for update in weekly_updates:
            weight_dict[str(update.pk)] = update.weight

        avg_workout = find_avg(workout_dict)
        avg_water_consumption = find_avg(water_consumption_dict)
        avg_weight = find_avg(weight_dict)

        context = {'workout': json.dumps(workout_dict),
                   'water_consumption': json.dumps(water_consumption_dict),
                   'weight': json.dumps(weight_dict), 'avg_workout': avg_workout,
                   'avg_water_consumption': avg_water_consumption,
                   'avg_weight': avg_weight}
        return render(request, 'dashboard/dashboard.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        update_type = request.POST.get('type')
        details = None

        try:
            details = UserDetails.objects.get(user=request.user)
        except Exception as identifier:
            pass

        if details is None:
            messages.error(
                request, 'You must fill up your profile before updating the data')
            return redirect('edit_profile')

        if update_type == "daily":
            workout = request.POST.get('workout')
            water_consumption = request.POST.get('water_consumption')
            update = DailyUpdates(
                workout=workout, water_consumption=water_consumption, user=user)
            update.save()
            details.water_consumption = water_consumption

        else:
            weight = request.POST.get('weight')
            update = WeeklyUpdates(weight=weight, user=user)
            update.save()
            details.weight = weight

        details.save()
        messages.info(request, 'Record Updated Successfully')
        return redirect('dashboard')