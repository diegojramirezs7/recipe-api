from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientAPITests(TestCase):
    """test the publicly available ingredient API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access endpoints """
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """test the ingredients can be retrieved by authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'diego@oxd.com',
            'MyPassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieve list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        """test that only ingredients for authenticated user are returned"""
        user2 = get_user_model().objects.create_user('other@oxd.com', 'MyPassword123')
        Ingredient.objects.create(user=user2, name='Other')
        ingredient = Ingredient.objects.create(
            user=self.user, name='My Ingredient')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """test that user can successfully create an ingredient"""
        payload = {'name': 'Cabbage'}
        res = self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user, name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """test create invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_ingredient_assigned_to_recipes(self):
        """Test filtering ingredients by those assigned to a recipe"""
        ingredient1 = Ingredient.objects.create(user = self.user, name = 'Apple')
        ingredient2 = Ingredient.objects.create(user = self.user, name = 'Turkey')

        recipe = Recipe.objects.create(
            title = 'Apple Crumble',
            time_minutes = 5,
            price = 10,
            user = self.user
        )

        recipe.ingredients.add(ingredient1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
    

    def test_retrieve_ingredients_unique(self):
        """Filtering ingredients by assigned return unique items"""
        ingredient = Ingredient.objects.create(user = self.user, name = 'Eggs')
        Ingredient.objects.create(user = self.user, name = 'cheese')

        recipe1 = Recipe.objects.create(
            title = 'Eggs benedict', 
            time_minutes = 30, 
            price = 12.00, 
            user = self.user
        )
        recipe1.ingredients.add(ingredient)

        recipe2 = Recipe.objects.create(
            title = 'Coriander Eggs on Toast', 
            time_minutes = 30, 
            price = 12.00, 
            user = self.user
        )

        recipe2.ingredients.add(ingredient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)

