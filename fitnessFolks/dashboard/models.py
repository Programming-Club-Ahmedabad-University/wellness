from django.db import models

from my_auth.models import User


class DailyUpdates(models.Model):
    workout = models.IntegerField()
    water_consumption = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='daily_updates')

    def __str__(self):
        return f"daily_updates_{self.user.first_name}_{self.id}"


class WeeklyUpdates(models.Model):
    weight = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='weekly_updates')

    def __str__(self):
        return f"weekly_updates_{self.user.first_name}_{self.id}"
