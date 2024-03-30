import requests

from .utility import importExistingSessions
from .models import Anime, AnilistUser, Session
from django.shortcuts import render
from django.core.cache import cache
from .anilist import *

# Create your views here.

def index(request):
    #get_anilist_listdata('')
    return render(request, 'index.html')

def anime_page(request, anilist_id):
    anime = get_anilist_anime_details(anilist_id)
    return render(request, 'anime.html', {'anime': anime})

def wheel_page(request, wheel_id):
    return render(request, 'wheel.html')

def session_history_page(request):
    sessions = Session.objects.all()
    return render(request, 'session_history.html', {'sessions': sessions})