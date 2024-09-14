from django.shortcuts import render
from django.http import HttpResponse

# Views

def home(request):
    return HttpResponse("Hello Test")
