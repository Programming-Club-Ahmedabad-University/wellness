from django.urls import path

from .views import QuestionsView, answers_view, submission_view

urlpatterns = [
	path('questions/', QuestionsView.as_view(), name='questions'), 
	path('answers/', answers_view, name='answers'),
	path('submit/', submission_view, name='submit')
]