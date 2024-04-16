from time import sleep
import requests
from django.core.cache import cache
    
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
                id
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

    return media

def get_user_anime_list(username: str):
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
                    }
                }
            }
        }
    }
    """

    variables = { 'username': username }

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    if response.status_code == 404:
        return '404'

    if 'error' in data:
        print(data['error'])
        return None
    
    else:
        return data['data']['MediaListCollection']['lists'][0]['entries']