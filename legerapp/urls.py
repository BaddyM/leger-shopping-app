from django.urls import path
from .views import *

urlpatterns = [
    path('',index_page,name='home'),
    path('categories/',categories,name='categories'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('cart/',cart_index,name='cart'),
    path('index_admin/',index_admin,name='adminindex'),
    path('about_admin/',about_admin,name='adminabout'),
    path('categories_admin/',categories_admin,name='admincategories'),
    path('contact_list/',contact_list,name='contactlist'),
    path('products/',product_admin,name='products')
]
