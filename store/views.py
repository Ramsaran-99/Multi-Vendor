from django.shortcuts import render,redirect
from store.models import *
from django.http import JsonResponse,HttpRequest
from decimal import *
from django.db.models import Q, Avg, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout as authlogout
from django.contrib.auth.models import User
from userauth import models as user_models

def homepage(request):
    return render(request,'store/index.html')

def products(request):
    products=Product.objects.filter(status="Published")

    return render(request,'store/products.html',
                  {
                      "products":products,
                  })

def product_detail(request,slug):
    product = Product.objects.get(status="Published",slug=slug)
    related_product = Product.objects.filter(category=product.category, status="Published").exclude()
    stock_range = range(1,product.stock + 1)
    return render(request,'store/product-detail.html',
                  {
                      "products":product,
                      "related":related_product,
                      "stock":stock_range,
                  })


def add_to_cart(request):
    
    id = request.GET.get("id")
    qty = request.GET.get("qty")
    color = request.GET.get("color")
    size = request.GET.get("size")
    cart_id = request.GET.get("cart_id")

    request.session['cart_id'] = cart_id
    if not id or not qty or not cart_id:
        return JsonResponse({"error": "No id, qty or cart_id"}, status=400)
    try:
        product= Product.objects.get(status="Published", id=id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not foud"}, status=404)
    
    if not id or not qty or not cart_id:
        return JsonResponse({"error": "No id, qty or cart_id"}, status=400)

    try:
        product = Product.objects.get(status="Published", id=id)

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not foud"}, status=404)

    existing_cart_items = Cart.objects.filter(cart_id=cart_id, product=product).first()
    if int(qty) > product.stock:
        return JsonResponse({"error": "Qty exceed current stock amount"}, status=404)

    if not existing_cart_items:
        cart = Cart.objects.create()
        cart.qty = qty
        cart.product = product.price
        cart.color = color
        cart.sub_total = Decimal(product.price) * Decimal(qty)
        cart.shipping = Decimal(product.shipping) * Decimal(qty)
        cart.total = cart.sub_total + cart.shipping
        cart.user = request.user if request.user_is_authenticated else None
        cart.cart_id = cart_id

        cart.save()

        message = "Item added to cart"       

    else:
        existing_cart_items.product = product
        existing_cart_items.qty = qty
        existing_cart_items.product = product.price
        existing_cart_items.color = color
        existing_cart_items.sub_total = Decimal(product.price) * Decimal(qty)
        existing_cart_items.shipping = Decimal(product.shipping) * Decimal(qty)
        existing_cart_items.total = existing_cart_items.sub_total + existing_cart_items.shipping
        existing_cart_items.user = request.user if request.user_is_authenticated else None
        existing_cart_items.cart_id = cart_id 

        existing_cart_items.save()

        message = "Cart updated"

    total_cart_items = Cart.objects.filter(Q(cart_id=cart_id) | Q(cart_id=cart_id))
    cart_sub_total = cart.objects.filter(Q(cart_id=cart_id) | Q(cart_id=cart_id)).aggregate(sub_total=Sum("sub_total")['sub_total'])
    return JsonResponse(
        {
            "message":message,
            "total_cart_items":total_cart_items.count(),
            "cart_sub_total": "{:,.2f}".format(cart_sub_total),
            "cart_sub_total": "{:,.2f}".format(existing_cart_items.sub_total) if existing_cart_items else "{:,.2f}".format(cart.cart_sub_total)
        }
    )        


def search(request):
    query=request.GET.get('s')
    products=Product.objects.filter(name__icontains=query).order_by("-date")
    return render(request,'store/search.html',
                  {
                      "products":products,
                      "query":query,
                  })

def login(request):
    message=""
    if request.method=="POST":
        username=request.POST.get('usermail')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)    
        if user is not None:
            authlogin(request,user)
            return redirect("store:home")
        else:
            message="Incorrect username or password!"
            
    return render(request,'authenticate/login.html',
                  {
                    "message":message,
                  })


#logout
@login_required(login_url="login")
def logout(request):
    authlogout(request)
    return redirect("store:home")

# register
def register(request):
    message=""
    if request.method=="POST":
        username1=request.POST.get('username')
        email1=request.POST.get('email')
        password=request.POST.get('password')
        password1=request.POST.get('password1')

        if password==password1:
            if user_models.User.objects.filter(email=email1).exists():
                message="email already exists"
                return redirect('register')
            elif user_models.User.objects.filter(username=username1).exists():
                message="username already exists"
                return redirect('login')
            else:
                user=user_models.User.objects.create_user(username=username1,email=email1,password=password)
                user.save()
        else:
                message="Passwords are not same"
        
    return render(request,'authenticate/register.html',
                  {
                    "message":message,
                    })



"""
TODO                                    STATUS

add_to_cart                             none
payment_integration                     none
proper login & logout functionality     none
changing_password                       none
sorting                                 none
notification                            none
review_management                       none
coupen & order management               none


"""