from ..models import Meal
import json, urllib.request, re

MAX_MEALS = 10
MAX_CHANCES = 3

''' list of words to be substitued so that player input 
and meal names can be compared easier '''
SUBS = { 
        'and' : '&',
        }

class Game_Controller:
    points = 0                      # total points player earned
    potential_points = -1           # points that can be cashed in before chances expire
    max_points = 0                  # number of possible points per meal (words in every meal name)
    chances = MAX_CHANCES           # num of guess attempts player has remaining
    meal_index = 0                  # index of current meal displayed
    playing = False                 # if the game is playing

    
    ''' adds up all possible points, fetching from database
        subsequent calls skip database query since the data has been saved already
    '''
    def get_max_poss_points(self):
        if self.max_points == 0:
            meal_results = Meal.objects.all()
            for m in meal_results:
                self.max_points += int(m.Value)
                
        return self.max_points            
    
    # these vars are required every time user wants to guess on a new meal
    def reset_round_vars(self):

        self.potential_points = -1 # -1 means guess has not been recieved
        self.chances = MAX_CHANCES
    
    # sets up vars so the game can be played again
    def start(self):
        
        self.reset_round_vars()
        self.points = 0
        self.meal_index = 0
        self.playing = True
        self.max_points = 0
        
        self.load_meals()
    
    # increments index, adds points, & returns if that index is valid anymore   
    def next_meal(self):
        
        self.points += self.potential_points
        
        self.reset_round_vars()

        self.meal_index += 1

        if self.meal_index >= MAX_MEALS:
            self.playing = False

        return self.playing
    #end method
    
    # uses index as pk for meal obj getting
    def get_cur_meal(self):
        meal_results = Meal.objects.all()
        return meal_results.get(pk= self.meal_index)

    '''
    splits user input, checks if any of the split words are included in the meal name
    points are rewarded for every matching word
    split words are also kept track of, preventing input like "bacon bacon" giving out 2 points for "Bacon Eggs"
    returns true if points were awarded
    '''
    def validate_name_input(self, name_input):
        
        self.chances -= 1
        
        # Lists
        input_vals = name_input.lower().split()
        meal_name = str(Meal.objects.get(pk= self.meal_index).cleaned_name)
        meal_words = meal_name.split() # individual words of the name to be checked against
        used_tokens = []
        
        # points earned
        p = 0
        
        # Loop
        for token in input_vals:
            if token in meal_words and token not in used_tokens:
                p += 1
            used_tokens.append(token)
        
        # Points are temporaily "potential" so user has multiple chances of improving their guess  
        self.potential_points = p  
            
        return p != 0
    #end method

    '''
    Fetches 10 unique random meals from TheMealDB API
    '''
    def load_meals(self):
        
        i = 0
        rec_meals = []
        
        # don't add more than 10 meals to database
        if Meal.objects.all():
            return
        
        while(i < MAX_MEALS):
            
            # Get meal JSON info from API call
            mealAPI = "https://www.themealdb.com/api/json/v1/1/random.php"
            
            with urllib.request.urlopen(mealAPI) as url:
                api_data = json.load(url)
                
            meal_img = api_data['meals'][0]['strMealThumb']
            meal_name = api_data['meals'][0]['strMeal']
            
            # skip over already added meals
            if meal_name in rec_meals:
                continue
            
            # Clean meal name of uncessary chars using REGEX!!!!
            meal_name_clean = re.sub('\(|\)|\,', '', meal_name) #deletes '(' and ')' and ','
            meal_name_clean = re.sub('\-', ' ', meal_name_clean) #replaces '-' with ' '
            meal_name_clean = meal_name_clean.lower()
            
            num_of_meal_tokens = len(meal_name_clean.split())        
            
            # Adding to SQLite database
            Meal.objects.create(meal_id= i, Name= meal_name, 
                                Source= meal_img, cleaned_name= meal_name_clean,
                                Value= num_of_meal_tokens)
            rec_meals.append(meal_name)
            i += 1
    #end method         

    # DELETES ALL meal objs
    def delete_meals(self):
        if Meal.objects.all():
            Meal.objects.all().delete()