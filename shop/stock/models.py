from email.policy import default
from django.db import models
from django.contrib.auth.models import User


PRODUCT_CHOICE = (
    (1, "nouriture"),
    (2, "éléctronique"),
    (3, "épicerie"),
    (4, "hygiéne"))


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200, default="")
    categorie = models.CharField(
       max_length=32,
       choices=PRODUCT_CHOICE,
    )
    price = models.IntegerField()
    product_number = models.IntegerField()
    product_number_max = models.IntegerField()
    discount = models.IntegerField(default=0)
    special_discount = models.IntegerField(default=1)
    special_discount_gift = models.IntegerField(default=1)


class Cart(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    validation = models.BooleanField(default=False)
