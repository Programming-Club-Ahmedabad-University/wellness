from django.contrib import admin
from .models import Account, UserDetails


class WeightFilter(admin.SimpleListFilter):
    title = 'Weight(kg)'
    parameter_name = 'current_weight'

    def lookups(self, request, model_admin):
        return [
            ('<60', 'less than 60'),
            ('60-80', '60-80'),
            ('80-100', '80-100'),
            ('>100', 'above 100'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<60':
            return queryset.distinct().filter(current_weight__lt=60)
        elif self.value() == '60-80':
            return queryset.distinct().filter(current_weight__gte=60, current_weight__lt=80)
        elif self.value() == '80-100':
            return queryset.distinct().filter(current_weight__gte=80, current_weight__lt=100)
        elif self.value() == '>100':
            return queryset.distinct().filter(current_weight__gte=100)

class HeightFilter(admin.SimpleListFilter):
    title = 'Height(cm)'
    parameter_name = 'height'

    def lookups(self, request, model_admin):
        return [
            ('<160', 'less than 160'),
            ('160-180', '160-180'),
            ('180-200', '180-200'),
            ('200', 'above 200'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<160':
            return queryset.distinct().filter(height__lt=160)
        elif self.value() == '160-180':
            return queryset.distinct().filter(height__gte=160, height__lt=180)
        elif self.value() == '180-200':
            return queryset.distinct().filter(height__gte=180, height__lt=200)
        elif self.value() == '>200':
            return queryset.distinct().filter(height__gte=200)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'enrollment_number', 'programme')
    list_filter = ('gender', 'programme')
    search_fields = ['full_name']


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'current_weight', 'birthdate')
    list_filter = (WeightFilter, HeightFilter, )
    # search_fields = ['user']


admin.site.register(Account, AccountAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
