from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    description = models.TextField()
    picture = models.FileField()
    discount = models.IntegerField()


class Order(models.Model):
    finished_time = models.DateTimeField()
    total_price = models.FloatField()
    active = models.BooleanField(default=True)


class OrderItem(models.Model):
    order = models.ForeignKey('Order')
    item = models.ForeignKey('Item')
    quantity = models.IntegerField()
