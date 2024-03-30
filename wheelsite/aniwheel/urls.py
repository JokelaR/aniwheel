from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("anime/<int:anilist_id>", views.anime_page, name="anime_page")
] 
