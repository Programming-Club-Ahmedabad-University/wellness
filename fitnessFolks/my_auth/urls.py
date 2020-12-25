from django.urls import path
from .views import logout_view, ProfileView


urlpatterns = [
    path('logout', logout_view, name='logout'),
    path('edit_profile/', ProfileView.as_view(), name='edit_profile'),
]