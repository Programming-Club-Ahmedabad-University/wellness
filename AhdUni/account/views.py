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

from .forms import LoginForm, RegisterForm, UserDetailsForm
from .models import Account, AccountManager, UserDetails
from .utils import (generate_token, is_valid_contact,
                    is_valid_enrollment, is_valid_email)


EMAIL_HOST_USER = config('EMAIL_HOST_USER')


# Generating token and sending mail for activating account
def send_activation_email(request, user, email):
    current_site = get_current_site(request)
    subject = 'WELLNESS-Activate your account'
    context = {'user': user, 'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': generate_token.make_token(user)}
    message = render_to_string('account/activate_link.html', context)
    plain_message = strip_tags(message)
    send_mail(subject, plain_message, EMAIL_HOST_USER,
              [email], html_message=message)


class RegisterView(View):
    """
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
            # user = Account.objects.get(
            #     Q(enrollment_number=enrollment_number) | Q(email=email) |
            #     Q(contact_number=contact_number))
            user = Account.objects.get(email=email)
        except Exception as identifier:
            user = None

        if user:
            messages.error(request, 'Account already exists!!')
            return redirect('register')

        if not is_valid_enrollment(enrollment_number):
            messages.error(request, 'Enter a valid enrollment number!!')
            return redirect('register')
        if not is_valid_contact(contact_number):
            messages.error(request, 'Enter a valid contact number!!')
            return redirect('register')
        if not is_valid_email(email):
            messages.error(
                request, 'Enter a valid Ahmedabad University email!!')
            return redirect('register')

        user = Account(full_name=full_name, email=email,
                       enrollment_number=enrollment_number,
                       contact_number=contact_number,
                       programme=programme, gender=gender)
        user.set_password(password)
        user.save()

        # Email verification is done by encoding user's primary key and generating a token
        send_activation_email(request, user, email)

        messages.info(request, 'Verification link sent. Check your email! \
            Please wait for 5-7 minutes and check \
            for SPAM/Promotions Folder in Gmail!'
                      )
        return redirect('login')


class LoginView(View):
    """
        Renders login page and authenticates user.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        context = {'form': form}
        return render(request, 'account/login.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(
                request, email=email, password=password)
        except Exception as identifier:
            user = None

        if user:
            if not user.is_activated:
                messages.error(
                    request, 'Account not activated. Contact administrator')
                return redirect('login')
            login(request, user)
            messages.info(request, 'Logged in successfully.')
            if request.user.has_updated_profile:
                return redirect('dashboard')
            else:
                return redirect('edit_profile')
        else:
            messages.error(request, 'Invalid Email or Password.')
            return redirect('login')


# Verification by decoding primary key and checking token
def email_activation_view(request, uidb64, token):
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
            messages.info(request, 'Reset link sent. Check your email! \
                Please wait for 5-7 minutes and check \
                for SPAM/Promotions Folder in Gmail!'
                          )
            return redirect('login')


class PasswordSetterView(View):
    """
        Verifying the reset link. 
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


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')


class ProfileView(View):
    """
        For rendering current profile and updating the profile
    """

    def get(self, request, *args, **kwargs):
        current_user = request.user
        form = UserDetailsForm()
        current_details = dict()
        user_details = UserDetails.objects.filter(user=request.user).values()

        if len(user_details) != 0:
            for data in user_details:
                current_details = data

            current_details.pop('id')
            current_details.pop('user_id')
            form = UserDetailsForm(data=current_details)

        context = {'form': form, 'current_details': user_details}
        return render(request, 'account/edit_profile.html', context)

    def post(self, request, *args, **kwargs):
        details = None
        menstrual_cycle = None
        ongoing_med_reason = None

        try:
            menstrual_cycle = request.POST.get('menstural_cycle')
        except Exception as identifier:
            pass

        try:
            ongoing_med_reason = request.POST.get('ongoing_med_reason')
        except Exception as identifier:
            pass

        try:
            details = UserDetails.objects.get(user=request.user)
        except Exception as identifier:
            pass

        if details is not None:
            details.delete()
        else:
            request.user.has_updated_profile = True
            request.user.save()

        new_detail = UserDetails(
            age=request.POST.get('age'),
            height=request.POST.get('height'),
            current_weight=request.POST.get('current_weight'),
            set_goal=request.POST.get('set_goal'),
            workout_patterns=request.POST.getlist('workout_patterns'),
            daily_water=request.POST.get('daily_water'),
            reason=request.POST.getlist('reason'),
            ongoing_med=request.POST.get('ongoing_med'),
            ongoing_med_reason=ongoing_med_reason,
            menstural_cycle=menstrual_cycle,
            hours_sleep=request.POST.get('hours_sleep'),
            smoking=request.POST.get('smoking'),
            alcohol=request.POST.get('alcohol'),
            junkfood=request.POST.get('junkfood'),
            user=request.user
        )
        new_detail.save()

        messages.info(request, 'Profile updated successfully')
        return redirect('home')
