from django.db import models


PRODUCT_CHOICE = (
    (1, "nouriture"), 
    (2, "éléctronique"),
    (3, "épicerie"),
    (4, "hygiéne"))


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    categorie = models.CharField(
       max_length=32,
       choices=PRODUCT_CHOICE,
    )
    price = models.IntegerField()
    product_number = models.IntegerField()
    discount = models.IntegerField(default=0)
    special_discount = models.IntegerField(default=1)
    special_discount_gift = models.IntegerField(default=1)
