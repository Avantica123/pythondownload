"""NewProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import settings
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("" ,views.index,name="home"),
    path('login/',views.userlogin,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.userlogout,name="logout"),
    path("aboutproduct/<int:id>/",views.aboutproduct,name="aboutproduct"),
    path("checkout/<int:id>/",views.checkout,name="checkout"),
    path("payment/<int:id>/",views.payment,name="payment"),
    path("payment_verify/",views.payment_verify,name="payment_verify"),
    path("myorder/",views.myorder,name="myorder"),
    path("download/<int:id>",views.downloaded,name="download"),
    path("addtocart/",views.addtocart,name="addtocart"),
    path("cart/",views.cart,name="cart"),
    path("removecart/",views.removecart,name="removecart")









]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

