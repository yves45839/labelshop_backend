import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from .models import Order, OrderItem

User = get_user_model()


def serialize_order(order):
    return {
        'id': order.id,
        'status': order.status,
        'created_at': order.created_at,
        'items': [
            {
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price,
            }
            for item in order.items.select_related('product')
        ],
    }


@csrf_exempt
def create_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = data.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Missing user_id'}, status=400)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    cart = Cart.objects.filter(user=user).first()
    if not cart or not cart.items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    order = Order.objects.create(user=user)
    for item in cart.items.select_related('product'):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.list_price,
        )
    cart.items.all().delete()
    return JsonResponse(serialize_order(order))


def list_orders(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    orders = user.orders.prefetch_related('items__product')
    return JsonResponse([serialize_order(order) for order in orders], safe=False)
