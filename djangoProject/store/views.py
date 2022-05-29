from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
import json

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


def checkout_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def details_view(request, pk=None, *args, **kwargs):
    product_obj = Product.objects.get(id=pk)
    if pk is not None:
        product_obj = Product.objects.get(id=pk)
    context = {
        "object": product_obj,
    }
    return render(request, 'store/details.html', context=context)


@login_required
def favorites_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/favorites.html', context)


def search_view(request):
    q = request.GET['q']
    products = Product.objects.filter(name__contains=q).order_by('-id')
    # in order to add genres to searchbar: Product.objects.filter(genre__contains=q).order_by('-id')
    return render(request, 'store/search.html', {'products': products})


def category_view(request, cats):
    products = Product.objects.filter(genre__exact=cats).order_by('-id')
    return render(request, 'store/category.html', {'cats': cats, 'products': products})


# def update_item(request):
#     data = json.load(request.body)
#     productId = data['productId']
#     action = data['action']
#     print('Action: ', action)
#     print('Product: ', productId)
#
#     return JsonResponse('Item was added', safe=False)


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

    return JsonResponse('Item was added to cart', safe=False)
