from django import template

from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def display(items, columns):
    html = '<div class="row full-height">'
    for idx, item in enumerate(items):
        html += '<div class="col-sm-{} item">' \
            .format(int(12 / columns))
        html += '<a href="{}"><img alt="{}" src="{}"/></a>' \
            .format(reverse("menu:item", kwargs={"item_id": item.pk}), item.name, item.image_url())

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
        edit = ''
        if editable:
            edit = '<small><div class="btn btn-default btn-xs remove-item" ' \
                   'data-id="{}" data-quantity="1">Remove one</div>'.format(item.id)
            if quantity > 1:
                edit += '<div class="btn btn-default btn-xs remove-item" ' \
                        'data-id="{}" data-quantity="{}">Remove all</div>'.format(item.id, quantity)
            edit += '</small>'

        html += '<div class="row">\
                    <div class="col-sm-2">\
                        <img alt="{}" src="{}"/>\
                    </div>\
                    <div class="col-sm-8">\
                        <h4>\
                            <strong><a href="{}">{}</a></strong>\
                            <span class="quantity" data-id="{}">{}</span>\
                        </h4>\
                        {}\
                    </div>\
                    <div class="col-sm-2 col-price">\
                        <strong class="subtotal" data-id="{}">{}$</strong>\
                    </div>\
                </div>'.format(item.name, item.image_url(),
                               reverse("menu:item", kwargs={"item_id": item.pk}), item.name,
                               item.id, pieces,
                               edit,
                               item.id, item.final_price() * quantity)

    html += '</div>'
    return mark_safe(html)
