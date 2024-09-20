from ..models import Meal
import json, urllib.request

MAX_MEALS = 10

lives = 3
points = 0
meal_index = 0

def add_point():
    global points
    points += 1
    
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
    

def Load_Meals():
    i = 0
    
    rec_meals = []
    
    if len(Meal.objects.all()) > 0:
        return
    
    while(i < MAX_MEALS):
        
        # Get random picture 
        mealAPI = "https://www.themealdb.com/api/json/v1/1/random.php"
        
        with urllib.request.urlopen(mealAPI) as url:
            api_data = json.load(url)
            
        meal_img = api_data['meals'][0]['strMealThumb']
        meal_name = api_data['meals'][0]['strMeal']
        
        if meal_name in rec_meals:
            continue
        
        Meal.objects.create(meal_id= i, Name= meal_name, Source= meal_img)
        rec_meals.append(meal_name)
        i += 1
        
    rec_meals.clear      
    