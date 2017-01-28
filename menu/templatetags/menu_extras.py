from django import template
import re

from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def selection_price(item, quanity):
    return item.final_price() * quanity

@register.filter
def display(items, columns):

    html = '<div class="row">'
    for idx, item in enumerate(items):
        html += '<div class="col-sm-{} item">'\
            .format(int(12 / columns))
        html += '<img alt="{}" src="media/{}" class="img-responsive item-img"/>'\
            .format(item.name, item.picture)

        if item.discount > 0:
            price_label = '<span class="label label-danger"><s>{}$</s> {}$ {}% off</span>'\
                .format(item.price, item.final_price(), item.discount)
        else:
            price_label = '<span class="label label-default">{}$</span>'\
                .format(item.price)

        html += '<div class="caption">' \
                '<h3>{} <small>{}</small></h3>' \
                '<p>{}</p>' \
                '<div data-id="{}" class="add-basket btn btn-primary">' \
                'Add to basket <i class="fa fa-shopping-basket" aria-hidden="true"></i>' \
                '</div>' \
            .format(item.name, price_label, item.description, item.id)

        html += '</div></div>'

        if idx != 0 and (idx + 1) % columns == 0:
            print(idx)
            html += '</div><div class="row">'

    html += '</div>'
    return mark_safe(html)

'''
<div class="col-sm-6 col-md-4">
    <div class="thumbnail">
      <img src="..." alt="...">
      <div class="caption">
        <h3>Thumbnail label</h3>
        <p>...</p>
        <p><a href="#" class="btn btn-primary" role="button">Button</a> <a href="#" class="btn btn-default" role="button">Button</a></p>
      </div>
    </div>
  </div>
'''