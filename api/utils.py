from django.utils import timezone

from menu.models import Order


def clean_orders():
    orders = Order.objects.filter(active__exact=True).filter(finished_time__lt=timezone.now())
    for o in orders:
        o.active = False
        o.save()

    return len(orders)