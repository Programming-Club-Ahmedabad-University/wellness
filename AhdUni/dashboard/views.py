import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from .models import DailyUpdates, WeeklyUpdates

class DashboardView(View):

	def get(self, request, *args, **kwargs):
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

		context = {'workout': json.dumps(workout_dict),
				   'water_consumption': json.dumps(water_consumption_dict),
				   'weight': json.dumps(weight_dict) }
		return render(request, 'dashboard/dashboard.html', context)

	def post(self, request, *args, **kwargs):
		user = request.user
		update_type = request.POST.get('type')

		if update_type == "daily":
			workout = request.POST.get('workout')
			water_consumption = request.POST.get('water_consumption')
			update = DailyUpdates(workout=workout, water_consumption=water_consumption, user=user)
			update.save()
		else:
			weight = request.POST.get('weight')
			update = WeeklyUpdates(weight=weight, user=user)
			update.save()
		
		messages.info(request, 'Record Updated Successfully')
		return redirect('dashboard')