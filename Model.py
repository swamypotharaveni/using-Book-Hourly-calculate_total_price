from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.TextField()
    total_charge = models.DecimalField(max_digits=6, blank=True, decimal_places=2, null=True)
    taken_date = models.DateTimeField(blank=True, null=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    book_hourly_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    book_created_date = models.DateTimeField(auto_now_add=True)
    book_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Book)
def calculate_total_price(sender, instance, **kwargs):
    if instance.taken_date and instance.submitted_date:
        duration = instance.submitted_date - instance.taken_date
        total_hours = duration.total_seconds() / 3600
        total_hours_decimal = Decimal(str(total_hours))
        instance.total_charge = instance.book_hourly_price * total_hours_decimal
    else:
        instance.total_charge = None



