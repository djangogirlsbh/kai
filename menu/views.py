from datetime import timedelta
from functools import reduce

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages

from api.utils import clean_orders, calculate_total
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
            total += item.final_price() * float(quantity)
            OrderItem.objects.create(item=item, order=current_order, quantity=quantity)

        current_order.total_price = total
        current_order.save()

        context['total'] = total
        context['ref_id'] = current_order.ref_id
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


def finder(request):
    context = {'method': request.method}
    if request.method == 'POST':
        if 'ref_id' in request.POST:
            try:
                order_items = OrderItem.objects.filter(order__ref_id=request.POST['ref_id'])
                items = {}
                total = 0.0
                for oi in order_items:
                    items[oi.item] = oi.quantity
                    total += oi.quantity * oi.item.final_price()

                context['items'] = items
                context['total'] = total

            except Item.DoesNotExist:
                print("ERROR")

    return render(request, 'menu/finder.html', context)


def basket(request):
    items = request.session.get('basket', {})

    return render(request, 'menu/basket.html', {
        'items': items,
        'total': calculate_total(items),
    })


def item(request, item_id):
    product = get_object_or_404(Item, pk=item_id)

    return render(request, 'menu/item.html', {
        'item': product
    })


