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
    
    goto_next_meal = False
    
    #Get info from form
    if request.method == "POST":
        guess = request.POST['your_guess']
        Validate_Name_Input(guess)
        if 'final' in request.POST:
            print("final")
            goto_next_meal = True
        else:
            print("check")
    else:
        guess = ''
    
    #move onto next meal data
    if goto_next_meal:
        print("MOVE ON")
        Next_Meal()
    
    #Game beginning
    if not playing:
        Start()
    
    #fetch meal vars
    cur_meal = Get_Cur_Meal()
    global meal_index
    #pass info to html
    return render(
        request,
        'guessing/meal.html',
        {
            'meal_img': cur_meal.Source,
            'meal_name': cur_meal.Name,
            'last_guess': guess,
            'pot_points': potential_points,
            'index': meal_index
        }
    )