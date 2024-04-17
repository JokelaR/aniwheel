# aniwheel

Fetch random anime from AniList by user

# Setup
Requirements
* Python 3.10 or greater
* Poetry

Installation
* Clone this repository
* (In the repository folder)
  * `poetry install` to install dependencies.
  * `poetry shell` to activate the environment
* (In the `/wheelsite` folder)
  * `python manage.py migrate` to create the django databases
  * `python manage.py createcachetable` to create the cache table
  * `python manage.py runserver` to run the development server
