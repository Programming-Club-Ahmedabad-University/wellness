from django.contrib import admin
from .models import Account , UserDetails


class AccountAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'enrollment_number', 'programme')
	list_filter = ('gender', 'programme')
	search_fields = ['full_name']

class UserDetailsAdmin(admin.ModelAdmin):
	list_display = ('user', 'height', 'current_weight', 'age')
	# search_fields = ['user.full_name']

admin.site.register(Account, AccountAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)