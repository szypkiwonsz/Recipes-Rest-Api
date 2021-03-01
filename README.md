# Recipes-Rest-Api

[**See Project Live Here**](https://recipes-cookbook-api.herokuapp.com/api/)

Simple API for recipes with a visible user interface, created with the Django REST Framework. It also has user 
registration and authentication using standard tokens.

## Endpoints

User registration

```
/api/users/ (POST) -> Body with username, email and password in JSON format
```

Get user token

```
/api/auth/ (POST) -> Body with username, email and password of registered user in JSON format
```

Add, show recipes

```
/api/recipes/ (GET, POST) -> To add a recipe you have to use JSON data formatted like bellow:

{"ingredients": [
    {"food": 
        {"name": "Lettuce"}, 
    "unit": "PIECE", 
    "amount": 1}
], 
"steps": [
    {"instruction": "Cut into strips."}
], 
"name": "Salad", 
"description": "Delicious salad.", 
"portions": 1, 
"preparation_time": 10, 
"difficulty": "EASY"}

and set the headers like:

KEY: Content-Type VALUE: application/json
KEY: Authorization VALUE: Token USER_TOKEN
```

Manage recipe

```
/api/recipes/1/ (GET, PATCH, DELETE) -> to edit or delete recipe you have to set up headers like bellow:

KEY: Content-Type VALUE: application/json
KEY: Authorization VALUE: Token USER_TOKEN
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Installing

Clone the repository

```
Open a terminal with the selected path where the project should be cloned
```
```
Type: git clone https://github.com/szypkiwonsz/Recipes-Rest-Api.git
```

### Prerequisites
Python Version
```
3.8+
```

Libraries and Packages

```
pip install -r requirements.txt
```
---

### Running

A step by step series of examples that tell you how to run a project

```
Download project
```
```
Install requirements
```
```
Run terminal with choosen folder "Physiotherapy_Management_System>" where manage.py file is
```
```
Type "python manage.py makemigrations", to make migrations
```
```
Type "python manage.py migrate", to create database
```
```
Set the environment variables as required in the settings.py file
```
```
Type "python manage.py runserver", to start the server
```
---
### Running tests

How to run tests
```
Open terminal with choosen folder "Physiotherapy_Management_System>" where manage.py file is
```
```
Type: "python manage.py test"
```
---

## Application Features
```
User registration
```
```
Login and authentication with a token
```
```
Possibility to get recipes and manage if you are an author
```
---
## Built With

* [Python 3.8](https://www.python.org/) - The programming language used
* [Django 3.0.4](https://www.djangoproject.com/) -  Web framework
* [Django REST Framework 0.1.0](https://www.django-rest-framework.org/) - Powerful toolkit for building Web APIs
* Unit Tests - Software testing method

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The project was made to better understand the Django REST Framework and for my other application created in Flask - 
[Cookbook-Recipes](https://github.com/szypkiwonsz/Cookbook-Recipes)