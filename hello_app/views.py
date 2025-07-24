# hello_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def greet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', 'Guest')
            return JsonResponse({'greeting': f'Hello, {name}!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def home(request):
    return JsonResponse({
        'message': 'Welcome to the homepage!',
        'available_endpoints': {
            'POST /greet/': 'Send a JSON with "name" to get a greeting'
        }
    })