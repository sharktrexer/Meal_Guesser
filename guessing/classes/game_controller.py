from ..models import Meal
import json, urllib.request, re

MAX_MEALS = 10
MAX_CHANCES = 3

''' list of words to be substitued so that player input 
and meal names can be compared easier '''
subs = { 
        'and' : '&',
        }

points = 0                      # total points player earned
potential_points = -1           # points that can be cashed in before chances expire
chances = MAX_CHANCES           # num of guess attempts player has remaining
meal_index = 0                  # index of current meal displayed
playing = False                 # if the game is playing
 
max_point_per_meal = []         # number of possible points per meal (words in meal name)
                                # index lines up with pk of meals in database

def Get_Max_Poss_Points():
    global max_point_per_meal
    
    max = 0
    for i in max_point_per_meal:
        max += i
    return max
 
def Reset_Round_Vars():
    global potential_points, chances
    
    potential_points = -1
    chances = MAX_CHANCES
 
def Start():
    global points, meal_index, playing, max_point_per_meal
    
    Reset_Round_Vars()
    points = 0
    meal_index = 0
    playing = True
    max_point_per_meal.clear
    
    Load_Meals()
 
# increments index, adds points, & returns if that index is valid anymore   
def Next_Meal():
    global meal_index, playing, potential_points, points
    
    Reset_Round_Vars()
    
    points += potential_points
    
    meal_index = meal_index + 1
    print("index ", meal_index)
    if meal_index >= MAX_MEALS:
        playing=False
        return False
    return True

def Get_Cur_Meal():
    meal_results = Meal.objects.all()
    return meal_results.get(pk= meal_index)

'''
splits user input, checks if any of the split words are included in the meal name
points are rewarded for every matching word
split words are also kept track of, preventing input like "bacon bacon" giving out 2 points for "Bacon Eggs"
returns true if points were awarded
'''
def Validate_Name_Input(name_input):
    global potential_points, chances
    
    chances -= 1
    
    # Lists
    input_vals = name_input.lower().split()
    meal_name = str(Meal.objects.get(pk= meal_index).cleaned_name)
    used_tokens = []
    
    p = 0
    
    # Loop
    for token in input_vals:
        if token in meal_name and token not in used_tokens:
            p += 1
        used_tokens.append(token)
      
    # Adds points to potential in case user wants to guess for a better chance of points  
    print('points: ', p)    
    if p == 0:
        return False
    if p > potential_points:
        potential_points = p
    return True
#end method

'''
Fetches 10 unique random meals from TheMealDB API
'''
def Load_Meals():
    global max_point_per_meal
    
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
        
        # Clean meal name of uncessary chars using REGEX!!!!
        meal_name_clean = re.sub('\(|\)|\,', '', meal_name) #deletes '(' and ')' 
        meal_name_clean = re.sub('\-', ' ', meal_name_clean) #replaces '-' with ' '
        meal_name_clean = meal_name_clean.lower()
        
        num_of_meal_tokens = len(meal_name_clean.split(' '))
        
        max_point_per_meal.append(num_of_meal_tokens)
        
        if meal_name in rec_meals:
            continue
        
        # Adding to SQLite database
        Meal.objects.create(meal_id= i, Name= meal_name, Source= meal_img, cleaned_name= meal_name_clean)
        rec_meals.append(meal_name)
        i += 1
#end method         
 