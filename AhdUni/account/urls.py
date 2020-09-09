from django.urls import path
from .views import (RegisterView, logout_view, email_activation_view,
                    ForgotPasswordView, PasswordSetterView, logout_view,
                    ProfileView, LoginView)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>',
         email_activation_view, name='activate'),
    path('forgot_password', ForgotPasswordView.as_view(), name='get_email'),
    path('set_password', PasswordSetterView.as_view(), name='set_password'),
    path('set_password/<enrollment_number64>/<token>',
         PasswordSetterView.as_view(), name='set_password'),
    path('logout', logout_view, name='logout'),
    path('edit_profile/', ProfileView.as_view(), name='edit_profile'),
]
