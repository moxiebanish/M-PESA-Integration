from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    number = models.CharField(max_length=13)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name 
    
class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    checkout_id = models.CharField(max_length=500, unique=True)
    amount = models.CharField(max_length=6)
    ref_code = models.CharField(max_length=20)
    date_and_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_and_time.strftime('%A, %d %B %Y, %I:%M%p'))
    
    def __repr__(self):
        return self.ref_code
    

# Create your models here.
