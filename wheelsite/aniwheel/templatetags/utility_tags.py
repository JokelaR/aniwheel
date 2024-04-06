from django import template
from ..models import Anime, Session, WatchedAnimeStatus
from datetime import date as Date

register = template.Library()

@register.filter
def session_info(anime: Anime, session_id: int):
    object = WatchedAnimeStatus.objects.get(watched_session=session_id, anime=anime)
    print(object)
    return object

@register.filter
def date(date: Date):
    return date.strftime('%d %B, %Y').lstrip('0')