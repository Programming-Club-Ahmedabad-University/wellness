from django.urls import path

from .views import *


urlpatterns = [
    path('', home_page_view, name='home'),
    path('FAQ/',faq_page_view,name='FAQ'),    
]