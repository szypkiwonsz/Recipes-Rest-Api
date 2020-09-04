import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


# Create your tests here.
class TestRecipeViewSet(APITestCase):
    list_url = reverse('recipe-list')
    detail_url = reverse('recipe-detail', args=[1])

    def setUp(self):
        self.user = User.objects.create(username='username', password='password')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.recipe = {
            "ingredients": [
                {
                    "food": {
                        "name": "Tomato"
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "preparation_description": "Dice the tomato."
        }
        self.recipes_created = [{
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato"
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "preparation_description": "Dice the tomato."
        }]
        self.recipe_created = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato"
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "preparation_description": "Dice the tomato."
        }

    def post_recipe(self):
        self.client.post(self.list_url, format='json', data=self.recipe)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='TOKEN ' + self.token.key)

    def test_recipe_list_get_authenticated(self):
        self.post_recipe()
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), self.recipes_created)

    def test_recipe_list_get_un_authenticated(self):
        self.post_recipe()
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), self.recipes_created)

    def test_recipe_list_post_authenticated(self):
        response = self.client.post(self.list_url, format='json', data=self.recipe)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(json.loads(response.content), self.recipe_created)

    def test_recipe_list_post_un_authenticated(self):
        response_message = {
            'detail': 'Authentication credentials were not provided.'
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(self.list_url, format='json', data=self.recipe)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(response.content), response_message)

    def test_recipe_list_post_authenticated_no_data(self):
        recipe_no_data = {}
        response_message = {
            "ingredients": [
                "This field is required."
            ],
            "name": [
                "This field is required."
            ],
            "portions": [
                "This field is required."
            ],
            "preparation_time": [
                "This field is required."
            ],
            "difficulty": [
                "This field is required."
            ],
            "preparation_description": [
                "This field is required."
            ]
        }
        response = self.client.post(self.list_url, format='json', data=recipe_no_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(response.content), response_message)

    def test_recipe_list_post_authenticated_no_ingredients_data(self):
        recipe_no_ingredients = {
            "ingredients": [],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "preparation_description": "Dice the tomato."
        }
        response_message = {
            "ingredients": {
                "empty_list_error": [
                    "Expected at least one item in list."
                ]
            }
        }
        response = self.client.post(self.list_url, format='json', data=recipe_no_ingredients)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(response.content), response_message)

    def test_recipe_list_post_authenticated_no_foods_data(self):
        recipe_no_foods = {
            "ingredients": [
                {
                    "food": {},
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "preparation_description": "Dice the tomato."
        }
        response_message = {
            "ingredients": [
                {
                    "food": {
                        "name": [
                            "This field is required."
                        ]
                    }
                }
            ]
        }
        response = self.client.post(self.list_url, format='json', data=recipe_no_foods)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(response.content), response_message)
