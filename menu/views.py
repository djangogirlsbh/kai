from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

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
            except Item.DoesNotExist:
                print("Invalid item item: %s" % item_id)

        current_order.total_price = total
        current_order.save()

        context['total'] = total
        context['items'] = items
        context['time'] = time

    return render(request, 'menu/order.html', context)
