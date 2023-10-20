import requests, httpx

from django.core.cache import cache
from django.conf import settings

PEOPLE_URL = f"{settings.SWAPI_URL}people/"


def all():
    cache_key = "all"

    return make_request(url=PEOPLE_URL, cache_key=cache_key)


def people(id: int, cache_key: str, vote=0):
    url = PEOPLE_URL + str(id)

    return make_request(url=url, cache_key=cache_key, vote=vote)


def search(q: str,  cache_key: str):
    url = PEOPLE_URL + f"?search={q}"

    return make_request(url=url, cache_key=cache_key)


def make_request(url: str, cache_key: str, vote=0):
    res = httpx.get(url).json()

    return save(
        people=res['results'] if 'results' in res else res,
        vote=vote,
        cache_key=cache_key
    )


def save(people: any, cache_key: str, vote=0):
    res = []

    if type(people) is dict:
        people = [people]
    for p in people:
        data = {
            'id': p['url'][29:-1],
            'name': p['name'],
            'vote': int(vote)
        }
        res.append(data)
        cache_votes = list(cache.get('votes', []))
        cache_votes[:] = [v for v in cache_votes if v['id'] not in set(data['id'])]
        cache_votes.append(data)
        save_to_cache(key='votes', value=cache_votes)

    save_to_cache(key=cache_key, value=res)

    return res


def save_to_cache(key: str, value):
    cache.set(
        key=key,
        value=value
    )


