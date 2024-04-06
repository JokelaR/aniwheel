from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("anime/<int:anilist_id>", views.anime_page, name="anime_page"),

    path("sessions/", views.session_history_page, name="session_history_page"),
    path("sessions/add/", views.add_session, name="add_session"),
    path("sessions/<int:session_id>/add_anime", views.add_anime_to_session, name="add_anime_to_session"),
    path("sessions/<int:session_id>/remove_anime/<int:relation_id>", views.remove_anime_from_session, name="remove_anime_from_session"),
    path("sessions/<int:session_id>/delete", views.delete_session, name="delete_session"),
] 
