from django.urls import path
from .views import *

app_name="store"

urlpatterns=[
    path('',homepage,name='home'),
    path('products/',products,name='products'),
    path('detail/<slug>/',product_detail,name='product_detail'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('search/',search,name='search'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('register/',register,name='register'),

]