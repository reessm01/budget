# simple-budget

## Installation instructions
- clone repo `git clone {repo_link}`
- `pipenv install`
- `pipenv shell`
- `python manage.py bootstrap_account_type`
- `python manage.py bootstrap_frequency`
- `python manage.py makemigrations` 
- `python manage.py migrate`

## Commands
### bootstrap_model
- Run `python manage.py bootstrap_model model_name_here` to initialize new model
- Creates new folder & files common for models and adds the url_patterns to baseapps urls.py folder

### bootstrap_personality
- Run `python manage.py bootstrap_account_type` to populate the AccountType table with predefined values

### 
- Run `python manage.py bootstrap_frequency` to populate the Frequency table with predefined values

## Templates
Add:<br>
{% extends 'common/base.html' %}<br>
{% load crispy_forms_tags %}<br>
{% block content %}<br>
your_content_here<br>
{% endblock %}<br>

## Sass instructions
- https://www.accordbox.com/blog/how-use-scsssass-your-django-project-npm-way/
