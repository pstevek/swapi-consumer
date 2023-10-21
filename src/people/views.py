import json

from . import consumer
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def index(request):
    res = {'success': True}
    query = request.GET.get('search')
    cache_key = "all" if query is None else f"search_{query}"
    result = cache.get(key=cache_key)

    res['data'] = result if result is not None \
        else consumer.search(q=query, cache_key=cache_key) if query is not None \
        else consumer.all()

    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@csrf_exempt
def person(request, person_id):
    res = {'success': False}
    cache_key = f"people_{person_id}"

    if request.method == 'GET':
        result = cache.get(key=cache_key)
        res['data'] = result if result is not None else consumer.people(id=person_id, cache_key=cache_key)
        res['success'] = True

        return Response(res, status=status.HTTP_200_OK)

    cache.delete(cache_key)
    vote = json.loads(request.body.decode('utf-8'))['vote']

    if not str(vote).isnumeric():
        res['message'] = 'Value must be numeric'
    elif int(vote) not in range(1, 6):
        res['message'] = 'Vote must between 1 to 5 inclusive'
    else:
        res['data'] = consumer.people(id=person_id, vote=vote, cache_key=cache_key)
        res['success'] = True

    return Response(res, status=status.HTTP_200_OK if res['success'] else status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def votes(request):
    votes = cache.get('votes', [])

    return Response({
        'success': True,
        'data': sorted(votes, key=lambda i: i['vote'], reverse=True)
    }, status=status.HTTP_200_OK)
