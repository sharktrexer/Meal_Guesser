from django.shortcuts import render, redirect
from django.http import Http404
from .classes.game_controller import Game_Controller

gc = Game_Controller()
  
# Views
def home(request):
    return render(
        request,
        "guessing/index.html")
    
def rand_meal(request):
    
    goto_next_meal = False
    guess = ''
    
    # user coming from home should reset the game!
    if request.method == "GET" and gc.playing:
        gc.playing = False
        
    
    #Get info from form
    if request.method == "POST":
        # deletion means no other data was posted
        if 'delete' in request.POST:
            gc.delete_meals()
        else: 
            guess = request.POST['your_guess']
            gc.validate_name_input(guess)
            
            if 'final' in request.POST or gc.chances < 0:
                goto_next_meal = True    
            
    
    #move onto next meal data
    if goto_next_meal:
        if not gc.next_meal():
            return redirect(ending)
        guess = ''
    
    #Game beginning
    if not gc.playing:
        try:
            gc.start()
        except:
            raise Http404("Could Not Establish Connection to the TheMealDB API")
    
    #fetch meal vars
    cur_meal = gc.get_cur_meal()
    
    #pass info to html
    return render(
        request,
        'guessing/meal.html',
        {
            'meal_img': cur_meal.Source,
            'meal_name': cur_meal.Name,
            'last_guess': guess,
            'pot_points': gc.potential_points,
            'index': gc.meal_index,
            'points': gc.points,
            'chances': gc.chances,
            'poss_points': cur_meal.Value
        }
    )
    
def ending(request):
    
    return render (
        request,
        'guessing/end.html',
        {
            'points': gc.points,
            'max_points': gc.get_max_poss_points()
        }
    )