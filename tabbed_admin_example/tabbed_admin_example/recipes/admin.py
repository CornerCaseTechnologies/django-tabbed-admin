from django.contrib import admin
from tabbed_admin import TabbedModelAdmin
from .models import Recipe, Ingredients, RecipeIngredients
# Register your models here.

class IngredientsAdmin(admin.ModelAdmin):
	model = Ingredients
	search_fields = ['name']
	list_filter = ['category']

class RecipeIngredientsInline(admin.TabularInline):
	model = RecipeIngredients
	autocomplete_fields = ['ingredient']
	extra = 0

class RecipesAdmin(TabbedModelAdmin):
	model = Recipe
	search_fields = ['recipe_name']

	fieldsets = [(None, {'fields': ('recipe_name', 'recipe_contact')})]

	ingredient_inline = (RecipeIngredientsInline,)
	
	tabs = [
		('Recipe Info', fieldsets),
		('Ingredients', ingredient_inline)
	]

admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredients, IngredientsAdmin)	