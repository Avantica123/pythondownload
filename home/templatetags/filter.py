from django import template
from math import floor

register=template.Library()

@register.simple_tag
def pppp(price,discount):
   return floor(price-(price * (discount/100)))

@register.simple_tag
def lain(cart):
   return len(cart)

@register.simple_tag
def is_in_cart(cart,product):  
   keys=cart.keys()
   for id in keys:
      if int(id)==product:
         return True
   return False  



@register.simple_tag
def quantity(cart,product):
   keys=cart.keys()
   for key in keys:
      if int(key)==product:
         return cart.get(key)
   return 0
   
      
@register.simple_tag
def rate(product_price,product_discount,cart,product):
   test=product_price-(product_price*product_discount/100)
   return floor(test*quantity(cart,product))
         
    

   
         
