from django.contrib import admin
from math import floor
from .models import Product,ProductImage,Payment,UserProduct,Category,Cart

# Register your models here.
class productimagemodel(admin.StackedInline):
    model=ProductImage
class productmodel(admin.ModelAdmin):
    inlines=[productimagemodel]
    model=Product
    list_editable=['category','discount']
    list_filter=['category','name']
    list_display=['name','thumbnail','category','discount','getprice']
    actions=['percentageup50']
    def getprice(self,product):
        a= floor(product.price -(product.price *(product.discount/100)))
        return f" Rs: {a}"

    def percentageup50(self,request,queryset):
        queryset.update(discount=50)


        
        
admin.site.register(Product,productmodel)
# admin.site.register(Payment)
# admin.site.register(UserProduct)
admin.site.register(Category)
admin.site.register(Cart)

@admin.register(Payment)
class paymentmodel(admin.ModelAdmin):
    list_display=['id','product','user','payment_id','order_id']

@admin.register(UserProduct)
class usermodel(admin.ModelAdmin):
    list_display=['user','product','payment']


    





