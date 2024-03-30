from hmac import new
import pickle
from .models import Anime, Session, AnilistUser, User, WatchedAnimeStatus
from datetime import date, timedelta

from .anilist import *

#2023, 4, 8
def importExistingSessions(filePath, year, month, day):
    data = pickle.load(open(filePath, 'rb'))

    sessionDate = date(year, month, day)
    increment = timedelta(days=7)

    Session.objects.all().delete()

    for session in data:
        sessionData = data[session]        
        print('Importing session', session, 'on', sessionDate)

        newSession = Session(date=sessionDate)
        newSession.save()
        sessionDate = sessionDate + increment
        for anime in sessionData:
            animeObject = get_anilist_anime_by_title(anime['name'])
            try:
                ownerObject = User.objects.get(username=anime['owner'])
                print('For existing user', ownerObject.username)
            except:
                username = anime['owner']
                print('Creating shallow user', username)
                ownerObject = User(username=username)
                ownerObject.save()
            status = WatchedAnimeStatus(
                watched_session=newSession,
                anime=animeObject,
                status=anime['status'],
                notes=anime['notes'],
                owner=ownerObject
            )
            status.save()
        newSession.save()
