from django.db import models

# Create your models here.
class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    source = models.TextField()
    cleaned_name = models.CharField(max_length=50)
    value = models.SmallIntegerField()

    def __str__(self):
        return f"({self.meal_id}) {self.name}"
