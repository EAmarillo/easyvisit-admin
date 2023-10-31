from django.db import models


# Create your models here.
class Place(models.Model):
    description = models.TextField(null=True)
    street = models.CharField(max_length=48)
    number = models.CharField(max_length=8)
    neighborhood = models.CharField(max_length=32)
    city = models.CharField(max_length=16)
    state = models.CharField(max_length=16)
    country = models.CharField(max_length=16)
    zip_code = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    urbanization = models.ForeignKey(
        'urbanizations.Urbanization',
        on_delete=models.CASCADE,
        related_name='place'
    )

    def __str__(self):
        return f'{self.street} No. {self.number}'
