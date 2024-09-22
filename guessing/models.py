from django.db import models

# Create your models here.
class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Source = models.TextField()
    cleaned_name = models.CharField(max_length=50)
    
    def __str__(self):
        str_id = "(" + str(self.meal_id) + ") "
        return str_id + self.Name