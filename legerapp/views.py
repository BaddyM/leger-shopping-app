from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import *
import datetime
import os
from django.conf import settings
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_page(request):
    page = 'Home'
    
    #Fetch Carousel Data
    carousel = Carousel.objects.values()
    context = {
        'page':page,
        'carousel':carousel
    }
    
    return render(request,'home.html',context)

def categories(request):
    page = 'Categories'
    context = {
        'page':page,
    }
    return render(request,'categories.html',context)

def contact(request):
    page = 'Contact'
    context = {
        'page':page,
    }
    
    if request.method == 'POST':
        #Get the data to the variables
        full_name = request.POST['full_name']
        email = request.POST['full_email']
        message = request.POST['message']
        status = 'unread'
        created_at = datetime.datetime.now()
        
        #Save the data to the model
        new_contact = Contact(full_name = full_name, email = email, message = message, status=status, created_at = created_at)
        new_contact.save()
        
    return render(request,'contact.html',context)

def about(request):
    page = 'About'
    context = {
        'page':page,
    }
    return render(request,'about.html',context)

def cart_index(request):
    page = 'Cart'
    context = {
        'page':page
    }
    return render(request, 'cart_index.html',context)

''' ***************************** Admin Views ***************************** '''

@login_required
def index_admin(request):
    page = 'Admin-Home'
    clients = len(Contact.objects.all().values())
    products = len(Product.objects.all().values())     
        
    context = {
        'page':page,
        'clients':clients,
        'products':products,
    }  
      
    return render(request, 'admin/index_admin.html', context)

@login_required
def index_ajax_response(request):
    if request.method == 'POST':
        #Messages
        try:
            msg_read = len(Contact.objects.filter(status='read').values())
            msg_unread = len(Contact.objects.filter(status='unread').values())
        except:
            msg_read = 0
            msg_unread = 0
            
        #Users
        try:
            users = len(Contact.objects.all())
        except:
            users = 0
            
        ajax_data = {
            'msg_read':msg_read,
            'msg_unread':msg_unread,
            'users':users
        }

        return JsonResponse(ajax_data)

@login_required
def categories_admin(request):
    page = 'Admin-Categories'
        
    if request.method == 'POST':
        process = request.POST['process']
        print("Process = "+process)
        if process == 'add_category':
            category_name = request.POST['category_name']
            save_category = Category(category_name=category_name)
            save_category.save()
        elif process == 'delete_category':
            id = request.POST['category_id']
            data = Category.objects.get(id=id)
            data.delete()
            return HttpResponse("Successfully Deleted Category.")
    
    #Fetch the data from the DB
    data = Category.objects.all().order_by('-id').values()  
    
    context = {
        'page':page,
        'data':data
    }
    
    return render(request, 'admin/categories_admin.html',context)

@login_required
def about_admin(request):
    page = 'Admin-About'
    
    if request.method == 'POST':
        process = request.POST['process']
        if process == 'add_about_text':
            text = request.POST['about_text']
            
            try:
                get_data = About.objects.get(id=1)
                get_data.about = text
                get_data.save()
                
                return HttpResponse("Data Updated!")
            except:
                #If empty, insert new
                about_text = About(about=text)
                about_text.save()
                return HttpResponse("New Data Inserted!")
    
    data = About.objects.get(id=1)
    context = {
        'page':page,
        'data':data
    }    
    return render(request, 'admin/about_admin.html', context)

@login_required
def product_admin(request):
    page = 'Admin-Product'
    categories = Category.objects.all().order_by('-id').values()
    
    context = {
        'page':page,
        'categories':categories
    }
    
    data = Product.objects.all().order_by('-id').values()
    
    if request.method == 'POST':
        task = request.POST['task']
        
        if task == 'add_product':
            product_name = request.POST['product_name']
            category = request.POST['product_category']
            price = request.POST['product_price']
            size = request.POST['product_size']
            qty = request.POST['product_qty']
            desc = request.POST['description']
            image = request.FILES['product_img']
            
            #Save into the DB
            save_data = Product(product_name = product_name, product_category = category, product_price = price, description = desc, size = size, items_available = qty, product_image = image)
            
            save_data.save()
        elif task == 'delete_product':
            id = request.POST['delete_id']
            x = Product.objects.get(id=id)
            image_file = str(x.product_image)
            #delete the product Image
            media_path = settings.BASE_DIR
            os.remove(os.path.join(media_path,'media',image_file))
            #Delete the product data
            x.delete()
        elif task == 'edit_product':
            id = request.POST['edit_id']
            #Fetch the data as Iterable
            modal_data = Product.objects.filter(id=id)
            #Serialize the data
            serialized = serializers.serialize('json',modal_data)
            if modal_data:
                return JsonResponse({'data':serialized},status=200)
        elif task == 'update_product':
            id = request.POST['product_id']
            prod_name = request.POST['product_name_edit']
            category = request.POST['product_category_edit']
            price = request.POST['product_price_edit']
            size = request.POST['product_size_edit']
            description = request.POST['description_edit']
            qty = request.POST['product_qty_edit']
            
            #Get data from DB 
            fetch_data = Product.objects.get(id=id)
            
            #Update the records
            try:
                #If image is not null
                image = request.FILES['product_img_edit']
                
                #Delete Old Image
                image_file = str(fetch_data.product_image)
                media_path = settings.BASE_DIR
                os.remove(os.path.join(media_path,'media',image_file))
                
                #Update the DB
                fetch_data.product_name = prod_name
                fetch_data.product_category = category
                fetch_data.product_price = price
                fetch_data.size = size
                fetch_data.description = description
                fetch_data.items_available = qty
                fetch_data.product_image = image
                
                #Save
                fetch_data.save()
            except:
                #IF IMAGE IS NULL
                #Update the DB
                fetch_data.product_name = prod_name
                fetch_data.product_category = category
                fetch_data.product_price = price
                fetch_data.size = size
                fetch_data.description = description
                fetch_data.items_available = qty
                
                #Save
                fetch_data.save()
                
    if data:
        context = {
            'page':page,
            'categories':categories,
            'data' : data
        }
    
    return render(request, 'admin/product_admin.html',context)

@login_required
def contact_list(request):
    page = 'Admin-Contact'
    
    #Orderby in descending order of the id
    data = Contact.objects.all().order_by('-id').values()
    
    context = {
        'page':page,
        'data':data
    }
    
    #Deal with the Contact Statuses
    if request.method == 'POST':
        #Get the id of the selected item
        id = int(request.POST['status_id'])
        #Get the status
        status = request.POST['status']    
        #fetch the data, using index
        x = Contact.objects.get(id=id)
          
        if status == 'delete':            
            x.delete()
        else:      
            #update the value
            x.status = 'read'
            x.updated_at = datetime.datetime.now()
            #Update the table
            x.save()

    return render(request, 'admin/contacts_list.html',context)

def login_user(request):
    page = 'Login'
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['userpassword']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("Logged in")
            return redirect('adminindex')
        else:
            print("Log in Failed")
            messages.success(request,"Failed: Invalid Credentials")
            return redirect('login_user')
     
    context = {
         'page':page
     }       
    return render(request,'admin/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('login_user')
