from django.db import models


# Create your models here.
class UrbanizationManager(models.Model):
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    phone = models.PositiveBigIntegerField()
    email = models.EmailField(max_length=64)
    is_active = models.BooleanField(default=True)
    urbanization = models.ForeignKey(
        'urbanizations.Urbanization',
        on_delete=models.CASCADE,
        related_name='urbanizationmanager'
    )

    def __str__(self):
        return self.first_name

