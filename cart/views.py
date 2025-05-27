import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from products.models import Product
from .models import Cart, CartItem

User = get_user_model()


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@csrf_exempt
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not user_id or not product_id:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return JsonResponse({'error': 'User or product not found'}, status=404)

    cart = get_user_cart(user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        item.save()

    return JsonResponse({'message': 'Product added to cart'})


@csrf_exempt
def update_cart_item(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not user_id or not product_id or quantity is None:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return JsonResponse({'error': 'User or product not found'}, status=404)

    cart = get_user_cart(user)
    try:
        item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not in cart'}, status=404)

    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    return JsonResponse({'message': 'Cart updated'})


@csrf_exempt
def remove_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not user_id or not product_id:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return JsonResponse({'error': 'User or product not found'}, status=404)

    cart = get_user_cart(user)
    CartItem.objects.filter(cart=cart, product=product).delete()

    return JsonResponse({'message': 'Item removed'})


def serialize_cart(cart):
    return {
        'id': cart.id,
        'items': [
            {
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.product.list_price,
            }
            for item in cart.items.select_related('product')
        ],
    }


@csrf_exempt
def view_cart(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    cart = get_user_cart(user)
    return JsonResponse(serialize_cart(cart))
