from django.contrib import admin
from .models import Meal

class MealAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )

# Register your models here.
admin.site.register(Meal, MealAdmin)