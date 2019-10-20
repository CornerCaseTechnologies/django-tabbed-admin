from django.db import models
from django.db.models import Q
# Create your models here.
class Ingredients(models.Model):
	name = models.CharField(max_length=100)
	category = models.CharField(max_length=100, choices=(
        ('ING', 'Ingredient'),
        ('FIN', 'Finished Good')
    ))
	def __str__(self):
		return "%s" % (self.name)

class Recipe(models.Model):
	recipe_name = models.ForeignKey(Ingredients, related_name='recipe_name', on_delete=models.CASCADE, limit_choices_to=Q(category='FIN'))
	ingredients = models.ManyToManyField(Ingredients, through='RecipeIngredients')
	recipe_contact = models.CharField(max_length=100)
	def __str__(self):
		return "%s" % (self.recipe_name)

class RecipeIngredients(models.Model):
	recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredients, related_name='ingredient', on_delete=models.SET_NULL, blank=False, null=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
	amount_category = models.CharField(max_length=100, choices=(
        ('oz', 'oz'),
        ('cups', 'Cups'),
        ('tbs','Table Spoons'),
        ('tp','Tea Spoons'),
        ('grams', 'Grams')
    ))
	def __str__(self):
		return "%s | %s" % (self.recipe, self.ingredient)
