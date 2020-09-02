from django.contrib import admin

from .models import DailyUpdates, WeeklyUpdates


admin.site.register(DailyUpdates)
admin.site.register(WeeklyUpdates)