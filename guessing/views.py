from django.shortcuts import render
from django.http import HttpResponse
from .models import Meal
from .classes.game_controller import game_controller
  
# Views

def home(request):
    return render(
        request,
        "guessing/index.html")
    
def rand_meal(request):
    
    #make sure to do rand pic fetching before creating view so that refresh
    # doesn't change the picture
    #game_controller.Load_Meals()
    query_results = Meal.objects.all()

    meal_img = str(query_results.get(id=1).Source)
    meal_name = str(query_results.get(id=1).Name)

    return render(
        request,
        'guessing/meal.html',
        {
            'meal_img': meal_img,
            'meal_name': meal_name
        }
    )