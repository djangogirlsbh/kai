from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages

from api.utils import clean_orders
from menu.models import Item, Order, OrderItem


def index(request):
    return render(request, 'menu/index.html', {
        'items': Item.objects.all(),
    })


def order(request):
    context = {'method': request.method}

    if request.method == 'POST' and 'proceed' in request.POST:
        total = 0

        clean_orders()

        # Add 90 seconds for every order already placed
        time = timezone.now() + timedelta(minutes=Order.objects.filter(active=True).count() * 1.5)
        current_order = Order.objects.create(finished_time=time, total_price=-1)

        # For every item propery create an OrderItem and finally an order, while calculating a total
        for item, quantity in request.session.get('basket', {}).items():
            total += item.price * float(quantity)
            OrderItem.objects.create(item=item, order=current_order, quantity=quantity)

        current_order.total_price = total
        current_order.save()

        context['total'] = total
        context['id'] = current_order.id
        context['time'] = time
        context['processed'] = True

        request.session['basket'] = {}

    return render(request, 'menu/order.html', context)


def recent(request):
    return render(request, 'menu/recent.html', {
        'items': Item.objects.all().order_by('-id')[:3],
    })


def deals(request):
    return render(request, 'menu/deals.html', {
            'items': Item.objects.filter(discount__gt=0),
    })


def basket(request):
    items = request.session.get('basket', {})

    total = 0
    for item, quantity in items.items():
        total += item.price * quantity

    return render(request, 'menu/basket.html', {
        'items': items,
        'total': total,
    })




