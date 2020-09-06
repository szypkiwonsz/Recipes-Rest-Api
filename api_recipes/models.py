from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=20)
    recipe = models.ForeignKey('Recipe', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('PIECE', 'PIECE'),
        ('GRAM', 'GRAM')
    )
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES)
    amount = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.food.name}, {self.amount}'


class Step(models.Model):
    instruction = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return


class Recipe(models.Model):
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
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    portions = models.PositiveIntegerField()
    preparation_time = models.PositiveIntegerField(help_text='Time in minutes.')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, blank=True, default=0)
    steps = models.ManyToManyField(Step)

    def __str__(self):
        return self.name