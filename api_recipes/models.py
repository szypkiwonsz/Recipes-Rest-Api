from django.db import models
from PIL import Image


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
    order = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.instruction}'


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
    name = models.CharField(max_length=50)
    image = models.ImageField(default='default.png', upload_to='recipes_images')
    description = models.TextField(max_length=500)
    ingredients = models.ManyToManyField(Ingredient)
    portions = models.PositiveIntegerField()
    preparation_time = models.PositiveIntegerField(help_text='Time in minutes.')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, blank=True, default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    steps = models.ManyToManyField(Step)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
