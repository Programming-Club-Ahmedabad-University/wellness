from django.urls import path

from .views import home_page_view, faq_page_view


urlpatterns = [
    path('', home_page_view, name='home'),
    path('faqs/',faq_page_view, name='faqs'),    
]