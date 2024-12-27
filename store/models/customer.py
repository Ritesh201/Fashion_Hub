from django.db import  models
from django.core.validators import MinLengthValidator

class Customer(models.Model):
    
    user_name = models.CharField(max_length=50)
    phone = models.IntegerField(default='8928')
    email = models.EmailField()
    password = models.CharField(max_length=500)
    re_enter_password=models.CharField(max_length=500,default='****')
    address=models.CharField(max_length=500,default='model town,ratia')
    pincode=models.IntegerField(default='125051')
    
    def register(self):
        self.save()
        

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False

 

