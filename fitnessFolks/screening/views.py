from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Questions, Answers


TOTAL_QUES = 2
SCREENING_TEST_GAP = 1


def screening_test_view(request, *args, **kwargs):
    '''
        Renders the questions page if the test is 
        available for the user
    '''

    # Retrun error msg if test is not available
    if not request.user.is_authenticated:
        context = {'error_message': 'You must login before viewing this page.'}
        return render(request, 'error.html', context)

    elif not request.user.extra_details.is_test_active():
        context = {'error_message':
                   f'You must wait for { SCREENING_TEST_GAP } day/s before attempting again.'}
        return render(request, 'error.html', context)

    # Return the questions if test is available
    questions = Questions.objects.all()

    paginator = Paginator(questions, 1)
    page = request.GET.get('page')
    question = paginator.get_page(page)

    context = {'object_list': question, 'range': paginator.page_range}
    return render(request, 'screening/questions.html', context)


def answers_view(request, *args, **kwargs):
    '''
        Stores the answers and renders the next question
    '''
    if not request.user.is_authenticated:
        context = {'error_message': 'You must login before viewing this page.'}
        return render(request, 'error.html', context)

    answer_type = request.POST.get('answer_type')
    answer_no = int(request.POST.get('answer_no'))
    answer_user = request.user
    answer_test_no = request.user.extra_details.last_screening_number

    current_answer = None

    # Check if the answer already exists
    try:
        current_answer = request.user.answers.get(
            answer_number=answer_no, answer_test=int(answer_test_no))
    except Exception as identifier:
        current_answer = None

    if answer_type == "1":
        answer_value = request.POST.get('value')

        # If it exists update, else create new
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

        # If it exists update, else create new
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
    '''
        Checks if the answers are completed and 
        updates the user accordingly
    '''
    if not request.user.is_authenticated:
        context = {'error_message': 'You must login before viewing this page.'}
        return render(request, 'error.html', context)

    user = request.user
    answered_questions = len(user.answers.filter(
        answer_test=user.extra_details.last_screening_number))

    # Return eror msg if all questions are not answered
    if answered_questions != TOTAL_QUES:
        messages.error(
            request, 'You must answer all the questions before finishing the test')
        return redirect('questions')
    else:
        request.user.extra_details.set_screening_number()
        request.user.extra_details.last_screening_date = datetime.now()
        request.user.extra_details.save()
        messages.info(request, 'Your test was completed successfully')
        return redirect('home')
