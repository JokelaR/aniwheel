from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("anime/<int:anilist_id>", views.anime_page, name="anime_page"),
    
    path("anime/random", views.get_random_anime, name="get_random_anime"),
    path("anime/more_random", views.get_more_anime, name="get_more_anime"),
    path("anime/set_seen", views.add_anime_to_seen, name="add_anime_to_seen"),

    #override allauth non-login urls
    re_path(r'^accounts\/(password|confirm-email|email).*', views.redirect_home, name="index_redirect"),
    path("accounts/signup/", views.redirect_login, name="login_redirect"),
    path("accounts/login/", views.redirect_login, name="login_redirect"),
] 
