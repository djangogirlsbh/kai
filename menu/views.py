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
        time = timezone.now() + timedelta(minutes=Order.objects.filter(active=True).count()*1.5)
        current_order = Order.objects.create(finished_time=time, total_price=-1)

        for post_id in [i for i in request.POST if "item-" in i]:
            item_id = post_id[5:]

            try:
                item = Item.objects.get(id=item_id)
                items.append(item)
                total += item.price
                OrderItem.objects.create(item=item, order=current_order)
            except Item.DoesNotExist:
                print("Invalid item item: %s" % item_id)

        current_order.total_price = total
        current_order.save()

        context['total'] = total
        context['items'] = items
        context['time'] = time

    return render(request, 'menu/order.html', context)
