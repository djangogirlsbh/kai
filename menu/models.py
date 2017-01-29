import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.six import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

IMAGE_RATIO = 16.0/9


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    description = models.TextField()
    picture = models.ImageField()
    discount = models.IntegerField()

    def final_price(self):
        if self.discount > 0:
            return (100-self.discount)/100*self.price
        else:
            return self.price

    def __str__(self):
        return "{} {}".format(self.name, self.final_price())


class Order(models.Model):
    finished_time = models.DateTimeField()
    total_price = models.FloatField()
    active = models.BooleanField(default=True)


class OrderItem(models.Model):
    order = models.ForeignKey('Order')
    item = models.ForeignKey('Item')
    quantity = models.IntegerField()


@receiver(post_save, sender=Item)
def resize_image(sender, instance, *args, **kwargs):
    imagefield = instance.picture
    oldname = imagefield.name
    if not oldname:
        return

    storage = imagefield.storage

    # Create a new filename based on the primary key of the item
    newname = "{}.jpg".format(slugify(instance.pk))

    content = storage.open(oldname, "rb")
    if storage.path(newname) == storage.path(oldname):
        return

    image = Image.open(content)

    width, height = image.size
    # The image is wider than needed
    if 1.0 * width / height > IMAGE_RATIO:
        new_width = height * IMAGE_RATIO
        padding = (width - new_width) / 2

        image = image.crop((padding, 0, new_width+padding, height))
    # The image is taller than needed
    else:
        new_height = width / IMAGE_RATIO
        padding = (height - new_height) / 2

        image = image.crop((0, padding, width, new_height+padding))

    image.thumbnail((500, 500), Image.ANTIALIAS)

    # Convert the PIL Image to bytes
    output = BytesIO()
    image.save(output, format="JPEG", quality=90)

    # Close the file stream
    content.close()

    # Delete any picture for the same id
    storage.delete(newname)

    # Save the model with the new image file
    imagefield.save(newname, ContentFile(output.getvalue()), save=True)

    # Delete any file containing the image file in the unresized and unrenamed state
    storage.delete(oldname)

