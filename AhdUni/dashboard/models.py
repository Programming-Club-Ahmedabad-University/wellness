from django.db import models

from account.models import Account


class DailyUpdates(models.Model):
	workout = models.IntegerField()
	water_consumption = models.IntegerField()
	date = models.DateField(auto_now=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='daily_updates')

class WeeklyUpdates(models.Model):
	weight = models.IntegerField()
	date = models.DateField(auto_now=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='weekly_updates')