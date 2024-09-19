from django.db import models

# Create your models here.
class Meal(models.Model):
    Name = models.CharField(max_length=50)
    Source = models.TextField()