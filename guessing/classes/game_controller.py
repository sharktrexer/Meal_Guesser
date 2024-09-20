from ..models import Meal
import json, urllib.request

MAX_MEALS = 10

IGNORED_WORDS = ['and', '&']

lives = 3
points = 0
meal_index = 0

def add_points(num):
    global points
    points += num
    
def next_meal():
    global meal_index
    meal_index += 1

def reset():
    global lives 
    global points
    global meal_index
    
    lives = 3
    points = 0
    meal_index = 0

'''
splits user input, checks if any of the split words are included in the meal name
points are rewarded for every matching word
split words are also kept track of, preventing input like "bacon bacon" giving out 2 points for "Bacon Eggs"
returns true if points were awarded
'''
def Validate_Name_Input(name_input):
    # Lists
    input_vals = name_input.lower().split()
    meal_name = str(Meal.objects.get(meal_id= meal_index).Name).lower()
    used_tokens = []
    
    p = 0
    
    # Loop
    for token in input_vals:
        if token in IGNORED_WORDS:
            continue
        if token in meal_name and token not in used_tokens:
            p += 1
        used_tokens.append(token)
            
    if p == 0:
        return False
    
    add_points(p)
    return True
#end method

'''
Fetches 10 unique random meals from TheMealDB API
'''
def Load_Meals():
    i = 0
    
    rec_meals = []
    
    if len(Meal.objects.all()) > 0:
        return
    
    while(i < MAX_MEALS):
        
        # Get meal JSON info from API call
        mealAPI = "https://www.themealdb.com/api/json/v1/1/random.php"
        
        with urllib.request.urlopen(mealAPI) as url:
            api_data = json.load(url)
            
        meal_img = api_data['meals'][0]['strMealThumb']
        meal_name = api_data['meals'][0]['strMeal']
        
        if meal_name in rec_meals:
            continue
        
        # Adding to SQLite database
        Meal.objects.create(meal_id= i, Name= meal_name, Source= meal_img)
        rec_meals.append(meal_name)
        i += 1
#end method         
    