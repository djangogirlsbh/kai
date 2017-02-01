from django.utils import timezone

from menu.models import Order


def clean_orders():
    orders = Order.objects.filter(active__exact=True).filter(finished_time__lt=timezone.now())
    for o in orders:
        o.active = False
        o.save()

    return len(orders)


def calculate_total(items):
    t = 0
    for item, quantity in items.items():
        t += item.final_price() * quantity

    return t