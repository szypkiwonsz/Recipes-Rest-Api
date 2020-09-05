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
            "steps": [
                {
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        self.recipes_created = [{
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }]
        self.recipe_created = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
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
            "steps": [
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
            "description": [
                "This field is required."
            ]
        }
        response = self.client.post(self.list_url, format='json', data=recipe_no_data)
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
            "steps": [
                {
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
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

    def test_recipe_detail_get_authenticated(self):
        self.post_recipe()
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), self.recipe_created)

    def test_recipe_detail_get_un_authenticated(self):
        self.post_recipe()
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), self.recipe_created)

    def test_recipe_detail_patch_authenticated_no_data(self):
        self.post_recipe()
        recipe_no_data = {}
        response = self.client.patch(self.detail_url, format='json', data=recipe_no_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), self.recipe_created)

    def test_recipe_detail_patch_authenticated_name(self):
        self.post_recipe()
        recipe_one_field = {
            "name": "New Salad"
        }
        recipe_new_name = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "New Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        response = self.client.patch(self.detail_url, format='json', data=recipe_one_field)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), recipe_new_name)

    def test_recipe_detail_patch_authenticated_ingredient(self):
        self.post_recipe()
        ingredient_new_name = {
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Strawberry",
                        "recipe": None
                    },
                    "unit": "GRAM",
                    "amount": 1
                }
            ],
        }
        new_recipe = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Strawberry",
                        "recipe": None
                    },
                    "unit": "GRAM",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        response = self.client.patch(self.detail_url, format='json', data=ingredient_new_name)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), new_recipe)

    def test_recipe_detail_patch_authenticated_new_ingredient(self):
        self.post_recipe()
        ingredient_new = {
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Strawberry",
                        "recipe": None
                    },
                    "unit": "GRAM",
                    "amount": 1
                },
                {
                    "food": {
                        "name": "Salad",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 2
                }
            ],
        }
        new_recipe = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Strawberry",
                        "recipe": None
                    },
                    "unit": "GRAM",
                    "amount": 1
                },
                {
                    "id": 2,
                    "food": {
                        "id": 2,
                        "name": "Salad",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 2

                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        response = self.client.patch(self.detail_url, format='json', data=ingredient_new)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), new_recipe)

    def test_recipe_detail_patch_authenticated_food(self):
        self.post_recipe()
        recipe_one_field = {
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
        }
        ingredient_new_name = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the tomato.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        response = self.client.patch(self.detail_url, format='json', data=recipe_one_field)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), ingredient_new_name)

    def test_recipe_detail_patch_authenticated_steps(self):
        self.post_recipe()
        step_new_name = {
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the strawberry.",
                    "order": 1
                }
            ],
        }
        new_recipe = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the strawberry.",
                    "order": 1
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        response = self.client.patch(self.detail_url, format='json', data=step_new_name)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), new_recipe)

    def test_recipe_detail_patch_authenticated_new_step(self):
        self.post_recipe()
        step_new = {
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the strawberry.",
                    "order": 1
                },
                {
                    "instruction": "Dice the tomato.",
                    "order": 2
                }
            ],
        }
        new_recipe = {
            "id": 1,
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
            "steps": [
                {
                    "id": 1,
                    "instruction": "Dice the strawberry.",
                    "order": 1
                },
                {
                    "id": 2,
                    "instruction": "Dice the tomato.",
                    "order": 2
                }
            ],
            "name": "Salad",
            "portions": 1,
            "preparation_time": 1,
            "difficulty": "EASY",
            "rating": "",
            "description": "Nice recipe."
        }
        response = self.client.patch(self.detail_url, format='json', data=step_new)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), new_recipe)

    def test_recipe_detail_patch_un_authenticated(self):
        self.post_recipe()
        self.client.force_authenticate(user=None)
        recipe_one_field = {
            "ingredients": [
                {
                    "id": 1,
                    "food": {
                        "id": 1,
                        "name": "Tomato",
                        "recipe": None
                    },
                    "unit": "PIECE",
                    "amount": 1
                }
            ],
        }
        response_message = {
            'detail': 'Authentication credentials were not provided.'
        }
        response = self.client.patch(self.detail_url, format='json', data=recipe_one_field)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(response.content), response_message)

    def test_recipe_detail_delete_authenticated(self):
        response_message = {
            'detail': 'Not found.'
        }
        response = self.client.delete(self.detail_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(json.loads(response.content), response_message)

    def test_recipe_detail_delete_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response_message = {
            'detail': 'Authentication credentials were not provided.'
        }
        response = self.client.delete(self.detail_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(response.content), response_message)
