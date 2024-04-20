from django.http import Http404, HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods, require_safe


from .models import SeenAnime
from django.shortcuts import render
from django.core.cache import cache
from .anilist import *
import random, json

# Create your views here.

def index(request):
    #get_anilist_listdata('')
    return render(request, 'index.html')

def anime_page(request, anilist_id, **kwargs):
    list = None
    if kwargs.get('remaining_list'):
        list = kwargs['remaining_list']
    anime = get_anilist_anime_details(anilist_id)
    if not anime:
        return JsonResponse({'status': 'failed', 'message': 'Error getting anilist anime'})
    return render(request, 'anime.html', {'anime': anime, 'remaining_list': list})

def get_random_anime(request):
    username = request.POST.get('search_user')
    filters = request.POST.getlist('format')
    status = request.POST.get('list')
    ignore_seen = request.POST.get('ignore_seen')
    if not ignore_seen:
        watchedList = [x.id for x in SeenAnime.objects.all()]
    else:
        watchedList = []

    if not username or not filters:
        raise Http404("Can't find anything with no username or no filters")
    
    list = cache.get(f'anilist_list_{username}_{status}')
    if not list:
        list = get_user_anime_list(username, status)
        if list == '404':
            raise Http404('User not found')
        cache.set(f'anilist_list_{username}_{status}', list, 600)
    if list:
        anime_picked = False
        list = [x['media']['id'] for x in list if x['media']['format'] in filters and x['media']['id'] not in watchedList]
        while not anime_picked and list:
            random.shuffle(list)
            chosen = list.pop()
            if chosen not in watchedList:
                anime_picked = True
        if not list:
            return JsonResponse({'status': 'failed', 'message': 'No anime to show'})
        return anime_page(request, chosen, remaining_list=list)
    
    else:
        return JsonResponse({'status': 'failed', 'message': 'Error getting anilist list'})

def get_more_anime(request):
    list = None
    if request.POST.get('remaining_list') != 'None':
        list = json.loads(request.POST.get('remaining_list'))
    if not list:
        return JsonResponse({'status': 'failed', 'message': 'No anime left'})
    return anime_page(request, list.pop(0), remaining_list=list)

@require_http_methods(['POST'])
@permission_required('aniwheel.add_seenanime')
def add_anime_to_seen(request):
    id = request.POST['anilist_id']
    if not id:
        return JsonResponse({'status': 'failed', 'message': 'Error getting anilist id'})
    SeenAnime.objects.get_or_create(id=id)
    return JsonResponse({'status': 'success'})

@require_safe
def redirect_login(request):
    return HttpResponseRedirect('/accounts/discord/login')

@require_safe
def redirect_home(request, leftovers):
    return HttpResponseRedirect('/')