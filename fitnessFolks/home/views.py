from django.shortcuts import render

from .models import Categories
from my_auth.models import ExtraDetails


def check_extra_details(user):
    '''
        Function to create a extra_detail object for a user,
        if it is not there
    '''
    if user.is_authenticated:
        extra_details = None

        try:
            extra_details = ExtraDetails.objects.get(user=user)
        except Exception as identifier:
            pass

        if extra_details is None:
            extra_details = ExtraDetails.objects.create(user=user)


def home_page_view(request):
    check_extra_details(request.user)

    context = {}
    return render(request, 'home/home.html', context)


def faq_page_view(request):
    categories = Categories.objects.all()

    context = {'categories': categories}
    return render(request,'home/faq.html', context)   