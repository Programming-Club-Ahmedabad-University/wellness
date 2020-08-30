from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Questions, Answers
from AhdUni.settings import TOTAL_QUES


class QuestionsView(ListView):
    paginate_by = 1
    model = Questions
    template_name = 'screening/questions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionsView, self).get_context_data(**kwargs)
        context['range'] = range(TOTAL_QUES)
        return context


def answers_view(request, *args, **kwargs):
    answer_type = request.POST.get('answer_type')
    answer_no = int(request.POST.get('answer_no'))
    answer_user = request.user
    answer_test_no = request.user.last_screening_number

    current_answer = None

    # Check if the answer already exists
    try:
        current_answer = request.user.answers.get(
            answer_number=answer_no, answer_test=int(answer_test_no))
    except Exception as identifier:
        current_answer = None

        # If it exists update, else create new
    if answer_type == "1":
        answer_value = request.POST.get('value')

        if current_answer == None:
            new_answer = Answers(answer_user=answer_user, answer_number=answer_no,
                                 answer_type=answer_type, answer_test=answer_test_no,
                                 answer_value=answer_value)
            new_answer.save()
        else:
            current_answer.answer_value = answer_value
            current_answer.save()
    else:
        yes_or_no = request.POST.get('yes_or_no')
        yes_or_no = "yes" if yes_or_no == '1' else "no"
        answer_text = request.POST.get('answer_text')

        if current_answer == None:
            new_answer = Answers(answer_user=answer_user, answer_number=answer_no,
                                 answer_type=answer_type, answer_test=answer_test_no,
                                 yes_or_no=yes_or_no, answer_text=answer_text)
            new_answer.save()
        else:
            current_answer.yes_or_no = yes_or_no
            current_answer.answer_text = answer_text
            current_answer.save()

    messages.info(request, f"Quesiton {answer_no} submitted successfully")

    if answer_no != TOTAL_QUES:
        answer_no += 1
    else:
        answer_no = 1

    redirect_url = f"/questions?page={answer_no}"
    return redirect(redirect_url)


def submission_view(request, *args, **kwargs):
    user = request.user
    answered_questions = len(user.answers.filter(
        answer_test=user.last_screening_number))
    if answered_questions != TOTAL_QUES:
        messages.error(
            request, 'You must answer all the questions before finishing the test')
        return redirect('questions')
    else:
        request.user.set_screening_number()
        request.user.last_screening_date = datetime.now()
        request.user.save()
        messages.info(request, 'Your test was completed successfully')
        return redirect('home')
