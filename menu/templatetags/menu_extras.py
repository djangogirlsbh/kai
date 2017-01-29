from django import template
import re

from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display(items, columns):
    html = '<div class="row full-height">'
    for idx, item in enumerate(items):
        html += '<div class="col-sm-{} item">' \
            .format(int(12 / columns))
        html += '<img alt="{}" src="{}" class="img-responsive item-img"/>' \
            .format(item.name, item.image_url())

        if item.discount > 0:
            price_label = '<span class="label label-danger"><s>{}$</s> {}$ {}% off</span>' \
                .format(item.base_price, item.final_price(), item.discount)
        else:
            price_label = '<span class="label label-default">{}$</span>' \
                .format(item.base_price)

        html += '<div class="caption">' \
                '<h3>{} <small>{}</small></h3>' \
                '<div data-id="{}" class="add-basket btn btn-primary">' \
                'Add to basket <i class="fa fa-shopping-basket" aria-hidden="true"></i>' \
                '</div>' \
            .format(item.name, price_label, item.id)

        html += '</div></div>'

        if idx != 0 and (idx + 1) % columns == 0:
            print(idx)
            html += '</div><div class="row">'

    html += '</div>'
    return mark_safe(html)


@register.filter
def basketify(items, editable):
    html = '<div class="items">'

    for item, quantity in items.items():
        pieces = "{} pieces".format(quantity) if quantity > 1 else ''
        edit = '<small><a href="#">Remove one</a> | <a href="#">Remove all</a></small>' if editable else ''

        html += '<div class="row">\
                    <div class="col-sm-2">\
                        <img alt="{}" src="{}" class="img-responsive item-img"/>\
                    </div>\
                    <div class="col-sm-8">\
                        <h4>\
                            <strong>{}</strong>\
                            <span class="quantity">{}</span>\
                        </h4>\
                        <p>{}</p>\
                        {}\
                    </div>\
                    <div class="col-sm-2 col-price">\
                        <strong>{}$</strong>\
                    </div>\
                </div>'.format(item.name, item.image_url(),
                               item.name,
                               pieces,
                               item.description,
                               edit,
                               item.final_price() * quantity)

    html += '</div>'
    return mark_safe(html)
