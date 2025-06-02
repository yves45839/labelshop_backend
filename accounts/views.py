import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout

from .utils import generate_and_send_otp, verify_otp

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

    if email:
        generate_and_send_otp(email)

    return JsonResponse({'id': user.id, 'username': user.username, 'role': user.role})


@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Missing credentials'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    login(request, user)

    return JsonResponse({'message': 'Logged in', 'id': user.id, 'username': user.username, 'role': user.role})


@csrf_exempt
def logout_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if request.user.is_authenticated:
        logout(request)

    return JsonResponse({'message': 'Logged out'})


@csrf_exempt
def cancel_account(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    user = request.user
    user.delete()
    logout(request)

    return JsonResponse({'message': 'Account deleted'})

@csrf_exempt
def verify_otp_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    email = data.get('email')
    code = data.get('code')
    if not email or not code:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    if verify_otp(email, code):
        return JsonResponse({'message': 'OTP verified'})
    return JsonResponse({'error': 'Invalid or expired OTP'}, status=400)
