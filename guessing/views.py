from django.shortcuts import render
from django.http import HttpResponse
from .models import Meal
from .classes.game_controller import *
  
# Views

def home(request):
    return render(
        request,
        "guessing/index.html")
    
def rand_meal(request):
    
    
    Load_Meals()
    query_results = Meal.objects.all()
    for m in query_results:
        meal_img = str(m.Source)
        meal_name = str(m.Name)
        break

    return render(
        request,
        'guessing/meal.html',
        {
            'meal_img': meal_img,
            'meal_name': meal_name
        }
    )