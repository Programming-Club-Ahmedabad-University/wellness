from django.urls import path

from .views import post_list_view, post_detail_view

urlpatterns = [
    path('blog/', post_list_view, name='blog'),
    path('blog/<slug:slug>/', post_detail_view, name='post_detail'),
]