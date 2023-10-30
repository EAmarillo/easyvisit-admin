from django.db import models


# Create your models here.
class UrbanizationManagers(models.Model):
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    phone = models.PositiveIntegerField()
    email = models.EmailField(max_length=64)
    is_active = models.BooleanField(default=True)
    urbanization = models.ForeignKey(
        'urbanizations.Urbanization',
        on_delete=models.CASCADE,
        related_name='urbanization_manager'
    )

    def __str__(self):
        return self.first_name
