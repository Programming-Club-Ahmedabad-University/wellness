from . import views
from django.urls import path

urlpatterns = [
    path('forum/', views.PostList.as_view(), name='forum'),
    path('forum/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]