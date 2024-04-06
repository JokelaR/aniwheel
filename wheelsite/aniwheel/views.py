from django.http import JsonResponse

from .utility import get_or_create_user

from .models import Anime, AnilistUser, Session, WatchedAnimeStatus
from django.shortcuts import redirect, render
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

def add_session(request):
    session = Session()
    session.save()
    return redirect('session_history_page')
def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    session.delete()
    return redirect('session_history_page')

def add_anime_to_session(request, session_id):
    session = Session.objects.get(id=session_id)
    try:
        anime = get_anilist_anime_by_title(request.POST['title'].strip())
    except:
        return JsonResponse({'status': 'failed', 'message': 'Error getting anilist id'})

    Session.objects.all()[0].shown_anime

    status = request.POST['status']
    notes = request.POST['notes']
    owner = get_or_create_user(request.POST['owner'])
    watched_anime_status = WatchedAnimeStatus(watched_session=session, anime=anime, owner=owner, status=status, notes=notes)
    watched_anime_status.save()
    return redirect('session_history_page')

def remove_anime_from_session(request, session_id, relation_id):
    watched_anime_status = WatchedAnimeStatus.objects.get(id=relation_id)
    watched_anime_status.delete()
    return redirect('session_history_page')