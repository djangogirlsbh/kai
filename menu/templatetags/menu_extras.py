from django import template
import re

from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def display(items, columns):

    html = '<div class="row">'
    for idx, item in enumerate(items):
        html += '<div class="col-sm-{} item">'\
            .format(int(12 / columns))
        html += '<img src="media/{}" class="img-responsive item-img"/><br>'\
            .format(item.picture)

        html += '<a href="{}?id={}" class="btn btn-primary pull-right">+</a>'\
            .format(reverse('menu:add'), item.id)

        html += '<label for="input-{}">{}'\
            .format(item.id, item.name)

        if item.discount > 0:
            html += '<span class="label label-danger"><s>{}$</s> {}$ {}% off</span>'\
                .format(item.price, item.final_price(), item.discount)
        else:
            html += '<span class="label label-default">{}$</span>'\
                .format(item.price)

        html += '</label><br>'
        html += '<p>{}</p></div>'\
            .format(item.description)

        if idx != 0 and (idx + 1) % columns == 0:
            print(idx)
            html += '</div><div class="row">'

    html += '</div>'
    return mark_safe(html)
