from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages

from menu.models import Item, Order, OrderItem


def index(request):
    return render(request, 'menu/index.html', {
        'items': Item.objects.all(),
    })


def order(request):
    context = {'method': request.method}

    if request.method == 'POST':
        items = []
        total = 0

        # Check all active orders if their finished_time has passed
        for o in Order.objects.filter(active=True):
            seconds_until = timezone.now() - o.finished_time
            if seconds_until.total_seconds() > 0:
                o.active = False
                o.save()

        # Add 90 seconds for every order already placed
        time = timezone.now() + timedelta(minutes=Order.objects.filter(active=True).count() * 1.5)
        current_order = Order.objects.create(finished_time=time, total_price=-1)

        # For every item propery create an OrderItem and finally an order, while calculating a total
        for post_id in [i for i in request.POST if "item-" in i]:
            # Discard of the "item-" part at the beginning of the property
            item_id = post_id[5:]
            quantity = request.POST.get(post_id)

            try:
                if int(quantity) > 0:
                    item = Item.objects.get(id=item_id)

                    total += item.price * float(quantity)
                    o_item = OrderItem.objects.create(item=item, order=current_order, quantity=quantity)

                    items.append(o_item)
                else:
                    messages.add_message(request, messages.INFO, 'One or more products have a negative quantity')
            except Item.DoesNotExist:
                print("Invalid item item: %s" % item_id)

        current_order.total_price = total
        current_order.save()

        context['total'] = total
        context['items'] = items
        context['time'] = time

    return render(request, 'menu/order.html', context)


def recent(request):
    items = Item.objects.all().order_by('-id')[:3]
    return render(request, 'menu/recent.html', {'items': items})


def deals(request):
    items = Item.objects.filter(discount__gt=0)
    return render(request, 'menu/deals.html', {'items': items})


def add(request):
    response = ''

    if request.method == 'GET' and 'id' in request.GET:
        item_id = request.GET['id']

        try:
            item = Item.objects.get(id=item_id)

            basket = request.session.get('basket', {})

            if item in basket:
                basket[item] += 1
            else:
                basket[item] = 1

            request.session['basket'] = basket

            # TODO: Remove debug print
            print(basket)

            response = 'true'
        except Item.DoesNotExist:
            print("Invalid item item: %s" % item_id)

    if not response:
        response = 'false'

    return HttpResponse(response)


def remove(request):
    response = ''

    if request.method == 'GET' and 'id' in request.GET:
        item_id = request.GET['id']

        try:
            item = Item.objects.get(id=item_id)
            basket = request.session.get('basket', {})

            quantity = 1
            if 'q' in request.GET:
                quantity = int(request.GET['q'])

            if item in basket:
                basket[item] -= quantity

                if basket[item] <= 0:
                    del basket[item]

                request.session['basket'] = basket
                response = 'true'

            # TODO: Remove debug print
            print(basket)

        except Item.DoesNotExist:
            print("Invalid item item: %s" % item_id)

    if not response:
        response = 'false'

    return HttpResponse(response)

