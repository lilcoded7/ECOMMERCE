from django.db import models
from django.contrib.auth.models import User 
import secrets
from .paystack import Paystack

# Create your models here.
class Customer(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name    = models.CharField(max_length=200)
    email    = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Product(models.Model):
    name      = models.CharField(max_length=100)
    price     = models.DecimalField(max_digits=7, decimal_places=2)
    digital   = models.BooleanField(default=False, null=True, blank=False)
    image     = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url 

class Order(models.Model):
    customer       = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_dete     = models.DateTimeField(auto_now_add=True)
    complete       = models.BooleanField(default=True, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for i in orderitems:
            if i.product.digital == False:
                shipping == True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total      = sum([item.get_total for item in orderitems])
        return total 

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total      = sum([item.quantity for item in orderitems])
        return total 
        


class OrderItem(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order      = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity   = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity 
        return total 


class ShippingAddress(models.Model):
    customer   = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order      = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address    = models.CharField(max_length=100)
    city       = models.CharField(max_length=100)
    state      = models.CharField(max_length=100)
    zipcode    = models.CharField(max_length=100)
    date_added = date_added    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address 


class Payment(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    ref     = models.CharField(max_length=200)
    email   = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return 'payment: ', self.amount

    def save(slef, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)

            similar_ref = Payment.objects.filter(ref=ref)
            if not similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def mount_value(self):
        return float(self.amount * 100)


    def verifypayment(self):
        paystack = Paystack()

        status, result = paystack.verify_payment(self.ref, self.amount)

        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True 
            self.save()
            if self.verified:
                return True 
        return False 

    
