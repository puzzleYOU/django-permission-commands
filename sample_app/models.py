from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=32)
    postcode = models.CharField(max_length=32)
    city = models.CharField(max_length=32)


class Employee(models.Model):
    prename = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
