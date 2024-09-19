from ..models import Meal
import json, urllib.request

MAX_MEALS = 10

class game_controller:
    lives = 3
    points = 0
    meal_index = 0

    def __init__(self):
        b = 2

    def add_point(self):
        self.points += 1
        
    def next_meal(self):
        self.meal_index += 1
    
    def reset(self):
        self.lives = 3
        self.points = 0
        self.meal_index = 0
        
    
    def Load_Meals():
        i = 0
        
        rec_meals = []
        while(i < MAX_MEALS):
            # Get random picture 
            mealAPI = "https://www.themealdb.com/api/json/v1/1/random.php"
            
            with urllib.request.urlopen(mealAPI) as url:
                api_data = json.load(url)
                
            meal_img = api_data['meals'][0]['strMealThumb']
            meal_name = api_data['meals'][0]['strMeal']
            
            if meal_name in rec_meals:
                continue
            
            Meal.objects.create(Name= meal_name, Source= meal_img)
            rec_meals.append(meal_name)
            i += 1
            
        rec_meals.clear      
    