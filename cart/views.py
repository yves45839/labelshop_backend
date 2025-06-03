import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

User = get_user_model()


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    user = request.user
    cart = get_user_cart(user)
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid quantity'}, status=400)
    if quantity <= 0:
        return JsonResponse({'error': 'Invalid quantity'}, status=400)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity},
    )
    if not created:
        item.quantity += quantity
        item.save()

    return JsonResponse({'message': 'Product added to cart'})


@csrf_exempt
@login_required
def update_cart_item(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or quantity is None:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    user = request.user

    cart = get_user_cart(user)
    try:
        item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not in cart'}, status=404)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid quantity'}, status=400)
    if quantity <= 0:
        return JsonResponse({'error': 'Invalid quantity'}, status=400)

    item.quantity = quantity
    item.save()

    return JsonResponse({'message': 'Cart updated'})


@csrf_exempt
@login_required
def remove_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')

    if not product_id:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    user = request.user

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
@login_required
def view_cart(request):
    user = request.user
    cart = get_user_cart(user)
    return JsonResponse(serialize_cart(cart))
