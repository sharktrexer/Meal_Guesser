import re
from django.shortcuts import render
from django.http import HttpResponse

# Views

def home(request):
    return HttpResponse("Hello Test")

def name_test(request, name):
    
    return render(
        request,
        'guessing/index.html',
        {
            'name': name
        }
    )