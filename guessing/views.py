from django.shortcuts import render
from django.http import HttpResponse
from .classes.game_controller import Game_Controller

gc = Game_Controller()
  
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
        gc.Validate_Name_Input(guess)
        if 'final' in request.POST:
            print("final")
            goto_next_meal = True
        else:
            print("check")
    else:
        guess = ''
    
    #move onto next meal data
    if goto_next_meal:
        gc.Next_Meal()
    
    #Game beginning
    if not gc.playing:
        gc.Start()
    
    #fetch meal vars
    cur_meal = gc.Get_Cur_Meal()
    global meal_index
    #pass info to html
    return render(
        request,
        'guessing/meal.html',
        {
            'meal_img': cur_meal.Source,
            'meal_name': cur_meal.Name,
            'last_guess': guess,
            'pot_points': gc.potential_points,
            'index': gc.meal_index
        }
    )