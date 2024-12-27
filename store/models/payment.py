from django.db import models
from .category import Category
from .customer import Customer
from .orders import Order
class Payment(models.Model):
    
    amount= models.IntegerField(default=0)
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)

    @staticmethod
    def get_payment_by_id(ids):
        return Payment.objects.filter(id__in =ids)

    @staticmethod
    def get_all_payment():
        return Payment.objects.all()

   