from django.db import models


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class Urbanization(models.Model):
    name = models.CharField(max_length=48)
    street = models.CharField(max_length=48)
    number = models.CharField(max_length=8)
    neighborhood = models.CharField(max_length=32)
    city = models.CharField(max_length=16)
    state = models.CharField(max_length=16)
    country = models.CharField(max_length=16)
    zip_code = models.PositiveSmallIntegerField
    houses = models.PositiveIntegerField
    is_active = models.BooleanField()
    rfc = models.CharField(max_length=13, null=True)
    email = models.EmailField(max_length=64)
    plan = models.ForeignKey(
        'urbanizations.Plan',
        on_delete=models.CASCADE,
        related_name='urbanization'
    )

    def __str__(self):
        return self.name
