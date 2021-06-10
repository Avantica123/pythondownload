from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import Signupform,loginform,checkoutform
from .models import Product,Category,ProductImage,Payment,UserProduct,Cart
import razorpay
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from math import floor
from django.contrib.auth.decorators import login_required
client = razorpay.Client(auth=("rzp_test_F8OWHQZtMIZnYA", "y48w4uBmBNhzzbuV1TgHeJjN"))


# Create your views here.
def cart(request):
    cart=request.session.get("cart").keys()
    
    
    product=Product.objects.filter(id__in=cart)
    print(product)

    return render(request,"cart.html",{"product":product})
def removecart(request):
    removecart=request.GET.get('removecart')
    print(removecart)
    cart=request.session.get('cart')
    print(cart)
    cart.pop(removecart)
    request.session['cart']=cart
    return redirect('cart')
def index(request):
    category=Category.objects.all()
    cart=request.session.get('cart')
    if cart is None:
        cart={}
    for i in cart:
        print(i)
    
                    
    
    
   
    
    
    # print(type(request.GET.Category))
    categori=request.GET.get('category')
    activate=None
    # activate=int(categori)
    if categori:
        products=Product.objects.filter(category=categori)
        activate=int(categori)
    else:
        products=Product.objects.all()

    return render(request,"index.html",{"products":products,'category':category,'activate':activate})



   
    



@csrf_exempt
def payment_verify(request):
    if request.method == "POST":
        print(request.POST)
        razorpay_payment_id =request.POST.get('razorpay_payment_id')
        razorpay_order_id =request.POST.get('razorpay_order_id')
        razorpay_signature =request.POST.get('razorpay_signature')
        payment=Payment.objects.get(order_id=razorpay_order_id)
        payment.status="SUCCESS"
        payment.payment_id=razorpay_payment_id
        payment.save()
        userproduct=UserProduct(user=payment.user,product=payment.product,payment=payment)
        userproduct.save()
        return render(request,"order.html")



        
def aboutproduct(request,id):
    product=Product.objects.get(pk=id)
    cart=request.session.get('cart')
    if cart:
        pass
    else:
        cart={}
    request.session['cart']=cart
    print(cart)
    
   

    
    return render(request,"aboutproduct.html",{'product':product})

def addtocart(request):
    # product=Product.objects.get(pk=id)
    product_id=request.POST.get('product')
    remove=request.POST.get('remove')

    
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(product_id)
        if quantity:
            if remove:
                cart[product_id]=quantity-1
            else:
                cart[product_id]=quantity+1

        else:
            cart[product_id]=1
    
    else:
        cart={}
        cart[product_id]=1
    request.session['cart']=cart
    
    
    print(cart)
    print(len(cart))
    

    return redirect(f"/aboutproduct/{product_id}")

def checkout(request,id):
    product=Product.objects.get(pk=id)
    user=None
    if request.user.is_authenticated:
        user=request.user
    else:
        return redirect("login")
    form=checkoutform(initial={'email':user.email})
    
    return render(request,"checkout.html",{'product':product,'form':form})   
def payment(request,id):
    product=Product.objects.get(pk=id)
    form=checkoutform(request.POST)
    user=None
    if request.user.is_authenticated:
        user=request.user
    else:
        return redirect('login')
    if form.is_valid:
        actualprice=floor(product.price-(product.price * (product.discount/100)))

        order_amount = actualprice * 100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        
        data ={
            "amount":order_amount,
            'currency':order_currency,
            'receipt':order_receipt
            
        }
        
        order=client.order.create(data=data)
        payment=Payment(product=product,user=user,status='FAIL',order_id=order.get('id'))
        payment.save()
        
        return render(request,'checkout.html',{'product':product,'user':user,'order':order,"dialog":True,"form":form})
        


    
    return render(request,"checkout.html",{'product':product,'form':form})  

def myorder(request):
    user=None
    if request.user.is_authenticated:
        user=request.user
        userproduct=UserProduct.objects.filter(user=user)
     
            
        return render(request,"myorder.html",{"userproduct":userproduct})

@login_required(login_url="/login/")
def downloaded(request,id):
    

    try:
       product=Product.objects.get(pk=id)
       userproduct=UserProduct.objects.get(product=product,user=request.user)
       return FileResponse(open(product.file.path,'rb'))
    except:
        return redirect('login')
   
    

def userlogin(request):
    # if not request.user.is_authenticated:
        if request.method=="POST":
            form=loginform(request=request, data=request.POST)
           
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    # cart=request.session.get('cart')
                    # product=None
                    # quantity=None
                    # if cart is None:
                    #     cart={}
                    # for i in cart:
                    #    product=Product.objects.filter(id__in=i)
                    #    quantity=cart.get(i)
                    # cart=Cart(product=product,quantity=quantity,user=user)
                    # cart.save()
                    # request.session['cart']=cart
                    
                    return redirect("/")
                    messages.success(request,"Succesfully Login")
                    # session_cart=request.session.get('cart')
                    # 
                    # for c in cart:
                    #     obje={"size":c.sizevariant.size,"tshirt":c.sizevariant.tshirt.id,"quantity":c.quantity}
                    #     session_cart.append(obje)
                    # request.session['cart']=session_cart if session_cart is None:
                    #     session_cart=[]
                    # else:
                    #     for c in session_cart:
                    #         size=c.get('size')
                    #         tshirt_id=c.get('tshirt')
                    #         quantity=c.get('quantity')
                    #         cart_obje=Cart()
                    #         cart_obje.sizevariant=Sizevariant.objects.get(size=size,tshirt=tshirt_id)
                    #         cart_obje.quantity=quantity
                    #         cart_obje.user=user
                    #         cart_obje.save()
                    # cart=Cart.objects.filter(user=user)
                    # session_cart=[]
                    # next_page=request.session.get('next_page')   
                    # if next_page is None:
                    #     next_page='home'
                    
                    # return redirect(next_page)
                
        else:
            form=loginform()
            # next_page=request.GET.get('next')
            # if next_page is not None:
            #     request.session['next_page']=next_page
        return render(request,'login.html',{"form":form})
    # else:
        # return redirect('/')

def signup(request): 
    if not request.user.is_authenticated:
        if request.method=="POST":

            form=Signupform(request.POST)
            if form.is_valid():

                form.save()
                form=Signupform()
                messages.success(request,"Congratutions!!! Welcome")
                return redirect('login')
        else:
          form=Signupform()
        return render(request,'signup.html',{"form":form})
    else:
        return redirect('/')
def userlogout(request):
    logout(request)
    return redirect('/')

