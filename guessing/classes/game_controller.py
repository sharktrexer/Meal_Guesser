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
    chances = MAX_CHANCES           # num of guess attempts player has remaining
    meal_index = 0                  # index of current meal displayed
    playing = False                 # if the game is playing
    
    max_point_per_meal = []         # number of possible points per meal (words in meal name)
                                    # index lines up with pk of meals in database
    
    
    def Get_Max_Poss_Points(self):
        
        max = 0
        for i in self.max_point_per_meal:
            max += i
        return max
    
    def Reset_Round_Vars(self):

        self.potential_points = -1 # -1 means guess has not been recieved
        self.chances = MAX_CHANCES
    
    def Start(self):
        global points, meal_index, playing, max_point_per_meal
        
        self.Reset_Round_Vars()
        self.points = 0
        self.meal_index = 0
        self.playing = True
        self.max_point_per_meal.clear
        
        self.Load_Meals()
    
    # increments index, adds points, & returns if that index is valid anymore   
    def Next_Meal(self):
        
        self.points += self.potential_points
        
        self.Reset_Round_Vars()

        self.meal_index += 1
        print("index ", self.meal_index)
        if self.meal_index >= MAX_MEALS:
            self.playing=False
            return False
        return True

    def Get_Cur_Meal(self):
        meal_results = Meal.objects.all()
        return meal_results.get(pk= self.meal_index)

    '''
    splits user input, checks if any of the split words are included in the meal name
    points are rewarded for every matching word
    split words are also kept track of, preventing input like "bacon bacon" giving out 2 points for "Bacon Eggs"
    returns true if points were awarded
    '''
    def Validate_Name_Input(self, name_input):
        
        self.chances -= 1
        
        # Lists
        input_vals = name_input.lower().split()
        meal_name = str(Meal.objects.get(pk= self.meal_index).cleaned_name)
        used_tokens = []
        
        p = 0
        
        # Loop
        for token in input_vals:
            if token in meal_name and token not in used_tokens:
                p += 1
            used_tokens.append(token)
        
        # Points are temporaily "potential" so user has multiple chances of improving their guess  
        self.potential_points = p  
            
        return p != 0
    #end method

    '''
    Fetches 10 unique random meals from TheMealDB API
    '''
    def Load_Meals(self):
        
        i = 0
        rec_meals = []
        
        # don't add more than 10 meals to database
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
            meal_name_clean = re.sub('\(|\)|\,', '', meal_name) #deletes '(' and ')' and ','
            meal_name_clean = re.sub('\-', ' ', meal_name_clean) #replaces '-' with ' '
            meal_name_clean = meal_name_clean.lower()
            
            num_of_meal_tokens = len(meal_name_clean.split(' '))
            
            self.max_point_per_meal.append(num_of_meal_tokens)
            
            if meal_name in rec_meals:
                continue
            
            # Adding to SQLite database
            Meal.objects.create(meal_id= i, Name= meal_name, Source= meal_img, cleaned_name= meal_name_clean)
            rec_meals.append(meal_name)
            i += 1
    #end method         
 