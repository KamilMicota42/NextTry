from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from .utils import cartData
import json
import datetime

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def store_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


@login_required
def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


@login_required
def favorites_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        favorites, created = Favorites.objects.get_or_create(customer=customer)
        items = favorites.favoritesitem_set.all()
    else:
        items = []
        favorites = []
    context = {'items': items, 'favorites': favorites}
    return render(request, 'store/favorites.html', context)


@login_required
def checkout_view(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def details_view(request, pk=None, *args, **kwargs):
    product_obj = Product.objects.get(id=pk)
    if pk is not None:
        product_obj = Product.objects.get(id=pk)
    context = {
        "object": product_obj,
    }
    return render(request, 'store/details.html', context=context)


def search_view(request):
    q = request.GET['q']
    products = Product.objects.filter(name__contains=q).order_by('-id')
    # in order to add genres to searchbar: Product.objects.filter(genre__contains=q).order_by('-id')
    return render(request, 'store/search.html', {'products': products})


def category_view(request, cats):
    products = Product.objects.filter(genre__exact=cats).order_by('-id')
    return render(request, 'store/category.html', {'cats': cats, 'products': products})


@login_required
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    orderItem.save()

    if action == 'remove':
        orderItem.delete()
        return JsonResponse('Item was deleted from cart', safe=False)

    orderItem.save()

    return JsonResponse('Item was added to cart', safe=False)


@login_required
def update_item_favorites(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    favorites, created = Favorites.objects.get_or_create(customer=customer)

    favoritesItem, created = FavoritesItem.objects.get_or_create(favorites=favorites, product=product)

    favoritesItem.save()

    if action == 'remove':
        favoritesItem.delete()
        return JsonResponse('Item was deleted from favorites', safe=False)

    favoritesItem.save()

    return JsonResponse('Item was added to favorites', safe=False)











@login_required
@csrf_exempt
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )

    products = Product.objects.all()
    lista = order.get_cart_items_ids
    for product in products:
        if (product.id in lista):
            product.delete()

    return JsonResponse('Payment submitted...', safe=False)
