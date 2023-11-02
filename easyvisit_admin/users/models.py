from django.db import models


# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.pk} | {self.role}'


class APIUser(models.Model):
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    email = models.EmailField(max_length=64)
    is_active = models.BooleanField(default=True)
    place = models.ForeignKey(
        'places.Place',
        on_delete=models.CASCADE,
        related_name='apiuser'
    )
    role = models.ForeignKey(
        'users.Role',
        on_delete=models.CASCADE,
        related_name='apiuser'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
