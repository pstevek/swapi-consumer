from django.http import JsonResponse

res = {
    'success': True,
    'message': "PostPay Assessment"
}


def index(request):
    return JsonResponse(res)