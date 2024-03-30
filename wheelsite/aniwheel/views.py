import requests
from .models import Anime, AnilistUser
from django.shortcuts import render
from django.core.cache import cache

# Create your views here.

def index(request):
    #get_anilist_listdata('')
    return render(request, 'index.html')

def anime_page(request, anilist_id):
    anime = get_anilist_anime_details(anilist_id)
    return render(request, 'anime.html', {'anime': anime})



# Utility functions

def get_anilist_listdata(username: str):
    """
    Get user anime list via the AniList GraphQL API
    """
    query = """
    query ($username: String) {
        MediaListCollection(userName: $username, type: ANIME, status: PLANNING) {
            lists {
                entries {
                    media {
                        id
                        title {
                            english
                            romaji
                        }
                        format
                        bannerImage
                        coverImage {
                            extraLarge
                            color
                        }
                    }
                }
            }
        }
    }
    """

    variables = {
        'username': username
    }

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    if 'error' in data:
        print(data['error'])
        return None

    anime_list = data['data']['MediaListCollection']['lists'][0]['entries']

    matched_anime = Anime.objects.in_bulk([anime['media']['id'] for anime in anime_list])

    newly_added = Anime.objects.bulk_create([
        Anime(
            anilist_id = anime['media']['id'],
            title_en = anime['media']['title']['english'],
            title_romaji = anime['media']['title']['romaji'],
            format = anime['media']['format'],
            banner_image = anime['media']['bannerImage'],
            cover_image = anime['media']['coverImage']['extraLarge'],
            cover_color = anime['media']['coverImage']['color']
        )
        for anime in anime_list if anime['media']['id'] not in matched_anime
    ])

    print('Added', len(newly_added), 'new anime to the database')

    pass

def get_anilist_userdata(username: str):
    """
    Get user data via the AniList GraphQL API
    """
    query = """
    query ($username: String) {
        User(name: $username) {
            id
            name
            avatar {
                large
            }
        }
    }
    """

    variables = {
        'username': username
    }

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    print(data)
    if 'error' in data:
        print(data['error'])
        return None
    
    user = data['data']['User']

    try:
        user = AnilistUser.objects.get(anilist_userid = user['id'])
        return user
    except:
        newuser = AnilistUser.objects.create(anilist_userid = user['id'], username = user['name'], avatar = user['avatar']['large'])
        return newuser
    
def get_anilist_anime_details(anilist_id: int):
    media = cache.get(f'anilist_anime_{anilist_id}')
    if (media is not None): 
        print(f'Got {anilist_id} from cache')
    if (media is None):
        print(f'Getting {anilist_id} from AniList API')
        """
        Get anime data via the AniList GraphQL API
        """
        query = """
        query ($id: Int) {
            Media(id: $id) {
                title {
                    english
                    romaji
                    native
                }
                format
                status
                episodes
                duration
                source (version: 3)
                description
                genres
                averageScore
                meanScore
                tags {
                    name
                    isGeneralSpoiler
                    isMediaSpoiler
                }
                isAdult
                bannerImage
                coverImage {
                    extraLarge
                    color
                }
            }
        }
        """

        variables = {
            'id': anilist_id
        }

        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()

        if 'errors' in data or 'error' in data:
            print(f'Anilist API returned an error', data)
            return None
        
        cache.set(f'anilist_anime_{anilist_id}', data['data']['Media'], 3600)
        media = data['data']['Media']

    print(media['isAdult'])
    return media