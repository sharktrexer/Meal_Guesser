from django.shortcuts import render
from django.http import HttpResponse
import json, urllib.request



# Views

def home(request):
    return HttpResponse("Hello Test")

def name_test(request, name):
    
    return render(
        request,
        'guessing/index.html',
        {
            'name': name
        }
    )
    
def rand_meal(request):
    
    # Get random picture
    mealAPI = "https://www.themealdb.com/api/json/v1/1/random.php"
    
    with urllib.request.urlopen(mealAPI) as url:
        api_data = json.load(url)
        
    meal_img = api_data['meals'][0]['strMealThumb']
    meal_name = api_data['meals'][0]['strMeal']
    print(meal_img)
    return render(
        request,
        'guessing/meal.html',
        {
            'meal_img': meal_img,
            'meal_name': meal_name
        }
    )