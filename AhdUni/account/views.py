import os
from decouple import config

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags
from django.contrib import messages
from django.db.models import Q

from .forms import LoginForm, RegisterForm, User_DetailsForm
from .models import Account, AccountManager, User_Details
from .utils import (generate_token, is_valid_contact,
                    is_valid_enrollment, is_valid_email)
# Create your views here.


EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')

# Generating token and sending mail for activating account


def send_activation_email(request, user, email):
    current_site = get_current_site(request)
    subject = 'CEL-Activate your account'
    context = {'user': user, 'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': generate_token.make_token(user)}
    message = render_to_string('account/activate_link.html', context)
    plain_message = strip_tags(message)

    send_mail(subject, plain_message, EMAIL_HOST_USER,
              [email], html_message=message)


class RegisterView(View):
    """
        Register View
        Renders registration page, verifies new user.
        On verification sends activation link.
    """

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        enrollment_number = request.POST.get('enrollment_number')
        contact_number = request.POST.get('contact_number')
        programme = request.POST.get('programme')
        gender = request.POST.get('gender')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(
                Q(enrollment_number=enrollment_number) | Q(email=email) |
                Q(contact_number=contact_number))
        except Exception as identifier:
            user = None

        if user:
            messages.error(request, 'Account already exists!!')
            return redirect('register')
        if not is_valid_email(email):
            messages.error(
                request, 'Enter a valid Ahmedabad University emails id!!')
            return redirect('register')
        if not is_valid_enrollment(enrollment_number):
            messages.error(request, 'Enter a valid enrollment number!!')
            return redirect('register')
        if not is_valid_contact(contact_number):
            messages.error(request, 'Enter a valid contact number!!')
            return redirect('register')

        user = Account(full_name=full_name, email=email,
                       enrollment_number=enrollment_number,
                       contact_number=contact_number,
                       programme=programme, gender=gender)
        user.set_password(password)
        user.save()

        # Email verification is done by encoding user's primary key and generating a token
        send_activation_email(request, user, email)

        messages.info(request,'Verification link sent. Check your email! \
            Please wait for 5-7 minutes and check \
            for SPAM/Promotions Folder in Gmail!'
            )
        return redirect('login')


class LoginView(View):
    """
        Login View
        Renders login page and authenticates user.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        context = {'form': form}
        return render(request, 'account/login.html', context)

    def post(self, request, *args, **kwargs):
        enrollment_number = request.POST.get('enrollment_number')
        password = request.POST.get('password')

        try:
            user = authenticate(
                request, enrollment_number=enrollment_number, password=password)
        except Exception as identifier:
            user = None

        if user:
            if not user.is_activated:
                messages.error(
                    request, 'Account not activated. Contact administrator')
                return redirect('login')
            login(request, user)
            messages.info(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Enrollment Number or Password.')
            return redirect('login')


class ActivateAccountView(View):
    """
        Email Activation.
        Verification by decoding primary key and checking token
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is None:
            messages.error(request, 'Verification failed!!')
        else:
            if generate_token.check_token(user, token):
                user.is_activated = True
                user.save()
                messages.info(request, 'Link verified successfully!!')
            else:
                messages.error(request, 'Verification failed!!')
        return redirect('login')


class ForgotPasswordView(View):
    """
        Forgot password view
        Getting email of the user and sending reset link.
    """

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'account/reset_email.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
        except Exception as identifier:
            user = None

        if user is None:
            messages.error(request, 'Enter valid email address')
            return redirect('forgot_password')
        else:
            current_site = get_current_site(request)
            subject = 'Programming Club-Reset Password'

            context = {'user': user, 'domain': current_site.domain,
                       'encoded_enrollment': urlsafe_base64_encode(
                            force_bytes(user.enrollment_number)
                           ),
                       'token': generate_token.make_token(user)}
            message = render_to_string('account/reset_link.html', context)
            plain_message = strip_tags(message)

            send_mail(subject, plain_message, EMAIL_HOST_USER,
                      [user.email], html_message=message)
            messages.info(request,'Reset link sent. Check your email! \
                Please wait for 5-7 minutes and check \
                for SPAM/Promotions Folder in Gmail!'
                )
            return redirect('login')


class PasswordSetterView(View):
    """
        Resetting new password
        Getting new password and updating it.
    """

    def get(self, request, enrollment_number64, token, *args, **kwargs):
        try:
            enrollment_number = force_text(
                urlsafe_base64_decode(enrollment_number64))
            user = Account.objects.get(enrollment_number=enrollment_number)
        except Exception as identifier:
            user = None

        if user is None:
            messages.error(request, 'Link verification failed1!!')
            return redirect('get_email')
        else:
            if generate_token.check_token(user, token):
                context = {'enrollment_number': user.enrollment_number}
                return render(request, 'account/new_password.html', context)
            else:
                messages.error(request, 'Link verification failed!!')
                return redirect('get_email')

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        enrollment_number = request.POST.get('enrollment_number')

        user = Account.objects.get(enrollment_number=enrollment_number)
        user.set_password(password)
        user.save()

        messages.info(request, 'Password changed successfully!!')
        return redirect('login')


# class ProfileView(LoginRequiredMixin, View):
#     """
#         View for profile page
#         Details of the users are displayed.
#         User can update password and CF id.
#     """
#     login_url = '/login/'
#     redirect_field_name = 'profile'

#     def get(self, request, *args, **kwargs):
#         context = {}
#         return render(request, 'account/profile/profile.html', context)

#     def post(self, request, *agrs, **kwargs):
#         field = request.POST.get('field')

#         if field == 'password':
#             old_password = request.POST.get('old')
#             try:
#                 user = authenticate(
#                     request, enrollment_number=request.user.enrollment_number, password=old_password)
#             except Exception as identifier:
#                 user = None

#             if user is None:
#                 messages.error(request, 'Password couldn\'t be verified')
#             else:
#                 password1 = request.POST.get('password1')
#                 password2 = request.POST.get('password2')

#                 if password1 == password2:
#                     request.user.set_password(password2)
#                     request.user.save()
#                     messages.info(request, 'Password changed successfully')
#                 else:
#                     messages.error(request, 'New Password didn\'t match')

#             return redirect('profile')

#         else:
#             password = request.POST.get('password')
#             try:
#                 user = authenticate(
#                     request, enrollment_number=request.user.enrollment_number, password=password)
#             except Exception as identifier:
#                 user = None

#             if user is None:
#                 messages.error(request, 'Password couldn\'t be verified')
#             else:
#                 request.user.cf_enrollment_number = request.POST.get('cf_enrollment_number')
#                 request.user.save()
#                 messages.info(request, 'enrollment_number updated successfully')

#             return redirect('profile')


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')

def edit_profile(request):
   # current_user = request.user
    #details = User_Details.objects.get(id=current_user.id)
    form = User_DetailsForm()
    if request.method =='POST':
        form = User_DetailsForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/')

   
    context = {'form': form}
    
    return render(request, 'account/edit_profile.html',context)
