from django.contrib import admin
<<<<<<< Updated upstream
from .models import Account , UserDetails
# Register your models here.

admin.site.register(Account)
admin.site.register(UserDetails)
=======
from .models import Account , User_Details, User_graph_workout
# Register your models here.

admin.site.register(Account)
admin.site.register(User_Details)
admin.site.register(User_graph_workout)
>>>>>>> Stashed changes
