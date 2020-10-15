from django.shortcuts import render

# Create your views here.


def home_page_view(request, *args, **kwargs):
    context = {}
    return render(request, 'home/home.html', context)

def faq_page_view(request):
    return render(request,'home/faq.html')    