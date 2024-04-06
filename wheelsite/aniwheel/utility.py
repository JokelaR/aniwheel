from hmac import new
import pickle
from .models import Anime, Session, AnilistUser, User, WatchedAnimeStatus
from datetime import date, timedelta

from .anilist import *

def get_or_create_user(username: str):
    try:
        user = User.objects.get(username=username)
        return user
    except:
        user = User(username=username)
        user.save()
        return user