from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title=models.CharField( max_length=50)
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    name=models.CharField( max_length=50)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    des=models.CharField( max_length=200)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    file=models.FileField( upload_to="upload/files",null=True,blank=True)
    thumbnail=models.ImageField( upload_to="upload/thumbnail")
    link=models.CharField( max_length=50,null=True,blank=True)
    filesize=models.IntegerField()

    def __str__(self):
        return self.name
        
    
class ProductImage(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="upload/images")

class Payment(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateTimeField( auto_now_add=True)
    status_bar=(
        ("SUCCESS","SUCCESS"),
        ("FAIL","FAIL")
    )
    status=models.CharField(choices=status_bar,max_length=200)
    payment_id=models.CharField(max_length=50)
    order_id=models.CharField( max_length=50)

    def __str__(self):
        return self.product.name
class UserProduct(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE)

class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    




