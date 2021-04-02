from django.urls import path

from .views import screening_test_view, answers_view, submission_view


urlpatterns = [
	path('questions/', screening_test_view, name='questions'), 
	path('answers/', answers_view, name='answers'),
	path('submit/', submission_view, name='submit')
]