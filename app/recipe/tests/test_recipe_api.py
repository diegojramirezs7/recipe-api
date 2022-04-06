from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Ingredient, Tag

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe(user, **kwargs):
    """create and return a sample recipe"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00,
    }

    defaults.update(kwargs)
    return Recipe.objects.create(user=user, **defaults)


def sample_tag(user, name='Main Course'):
    """create and return a Tag object"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name = 'Cinammon'):
    """create and return an Ingredient object"""
    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """test that authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """test authenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = 'diego@oxd.com',
            password = 'MyPassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe(self.user)
        sample_recipe(self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user('test@oxd.com', 'MyPassword123')
        sample_recipe(user = self.user)
        sample_recipe(user = user2)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
    
    def test_view_recipe_detail(self):
        """test viewing a recipe detail"""
        recipe = sample_recipe(user = self.user)
        recipe.tags.add(sample_tag(user = self.user))
        recipe.ingredients.add(sample_ingredient(user = self.user))

        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
        


