from django.db import models
from .category import Category
from .customer import Customer
from .orders import Order
class Hisab(models.Model):
    
    amount= models.IntegerField(default=0)
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    order= models.ForeignKey(Order, on_delete=models.CASCADE, default=1)
    @staticmethod
    def get_hisab_by_id(ids):
        return Hisab.objects.filter(id__in =ids)

    @staticmethod
    def get_all_hisab():
        return Hisab.objects.all()

   