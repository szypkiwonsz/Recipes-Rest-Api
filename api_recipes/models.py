from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
from easy_thumbnails.fields import ThumbnailerImageField


class User(AbstractUser):
    email = models.EmailField(unique=True, error_messages={
        'unique': _('A user with that email already exists.')
    })


class Food(models.Model):
    name = models.CharField(max_length=20)
    recipe = models.ForeignKey('Recipe', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('PIECE', 'PIECE'),
        ('GRAM', 'GRAM'),
        ('LITER', 'LITER'),
        ('SPOON', 'SPOON'),
        ('TEASPOON', 'TEASPOON'),
        ('MILLILITER', 'MILLILITER'),
        ('BUNCH', 'BUNCH'),
        ('PINCH', 'PINCH')
    )
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    amount = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.food.name}, {self.amount}'


class Step(models.Model):
    instruction = models.TextField(max_length=500)
    order = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.instruction}'


class Recipe(models.Model):
    CROP_SETTINGS = {'size': (300, 300), 'crop': 'smart'}
    DIFFICULTY_CHOICES = (
        ('EASY', 'EASY'),
        ('MEDIUM', 'MEDIUM'),
        ('HARD', 'HARD')
    )
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    name = models.CharField(max_length=50)
    image = ThumbnailerImageField(default='default.png', upload_to='recipe_images', resize_source=CROP_SETTINGS)
    description = models.TextField(max_length=500)
    ingredients = models.ManyToManyField(Ingredient)
    portions = models.PositiveIntegerField()
    preparation_time = models.PositiveIntegerField(help_text='Time in minutes.')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, blank=True, default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    steps = models.ManyToManyField(Step)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
