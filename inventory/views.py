import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Site, ProductStock
from .utils import transfer_stock as transfer_stock_util


@csrf_exempt
@login_required
def manage_sites(request):
    if request.method == 'GET':
        sites = list(Site.objects.values('id', 'name'))
        return JsonResponse(sites, safe=False)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        name = data.get('name')
        if not name:
            return JsonResponse({'error': 'Missing name'}, status=400)
        site, created = Site.objects.get_or_create(name=name)
        if not created:
            return JsonResponse({'error': 'Site already exists'}, status=400)
        return JsonResponse({'id': site.id, 'name': site.name})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def list_product_stock(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    stocks = [
        {
            'site_id': stock.site.id,
            'site_name': stock.site.name,
            'quantity': stock.quantity,
        }
        for stock in ProductStock.objects.filter(product=product).select_related('site')
    ]
    return JsonResponse(stocks, safe=False)


@csrf_exempt
@login_required
def update_product_stock(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    site_id = data.get('site_id')
    quantity = data.get('quantity')

    if product_id is None or site_id is None or quantity is None:
        return JsonResponse({'error': 'Missing fields'}, status=400)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    try:
        site = Site.objects.get(id=site_id)
    except Site.DoesNotExist:
        return JsonResponse({'error': 'Site not found'}, status=404)
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid quantity'}, status=400)
    if quantity < 0:
        return JsonResponse({'error': 'Invalid quantity'}, status=400)

    stock, _ = ProductStock.objects.get_or_create(product=product, site=site, defaults={'quantity': 0})
    stock.quantity = quantity
    stock.save(update_fields=['quantity'])

    return JsonResponse({'message': 'Stock updated', 'quantity': stock.quantity})


@csrf_exempt
@login_required
def transfer_product_stock(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    from_site_id = data.get('from_site_id')
    to_site_id = data.get('to_site_id')
    quantity = data.get('quantity')

    if None in (product_id, from_site_id, to_site_id, quantity):
        return JsonResponse({'error': 'Missing fields'}, status=400)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    try:
        from_site = Site.objects.get(id=from_site_id)
        to_site = Site.objects.get(id=to_site_id)
    except Site.DoesNotExist:
        return JsonResponse({'error': 'Site not found'}, status=404)
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid quantity'}, status=400)
    if quantity <= 0:
        return JsonResponse({'error': 'Invalid quantity'}, status=400)

    try:
        origin, dest = transfer_stock_util(product, from_site, to_site, quantity)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({
        'message': 'Transfer successful',
        'from_site_id': origin.site.id,
        'to_site_id': dest.site.id,
        'origin_quantity': origin.quantity,
        'dest_quantity': dest.quantity,
    })
