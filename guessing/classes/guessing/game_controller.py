class game_controller:
    lives = 3
    points = 0
    meal_index = 0

    def add_point(self):
        self.points += 1
        
    def next_meal(self):
        self.meal_index += 1
    
    def reset(self):
        self.lives = 0
        self.points = 0
        self.meal_index = 0