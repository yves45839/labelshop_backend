import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()


@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if not username or not password or not role:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if role not in dict(User.ROLE_CHOICES):
        return JsonResponse({'error': 'Invalid role'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    user.save()

    return JsonResponse({'id': user.id, 'username': user.username, 'role': user.role})
