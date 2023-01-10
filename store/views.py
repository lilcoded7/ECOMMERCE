from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse 
import json 
import datetime 

from django.contrib import messages  
from django.conf import settings 
from .utils import cookieCart, Util, cartData
from django.conf import settings 
from django.core.mail import EmailMessage
from .forms import registerForm, loginForm
from django.contrib.auth import authenticate, login 




# Create your views here.


def verifyAcount(request):
    return JsonResponse(request, 'Account Verified ', safe=False)





def register(request):
    form = registerForm()

    if request.method == 'POST':
        form = registerForm(request.POST)
        print('passed =================================')

        if form.is_valid():
            password         = form.cleaned_data['password']
            email            = form.cleaned_data['email']
            confirm_password = form.cleaned_data['confirm_password']
            message = 'Dear Customer, Congratulation Your Account Has Been Created Successfuly'
            print(confirm_password)
            

            if password == confirm_password:
                pass 
            else:
                messages.info(request, 'Password Is Not The Same')
                print('saving form ==============================') 
            form.save() 
                
            sendEmail = EmailMessage(
                'Owusuwa Collection',
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            sendEmail.fail_silently = True
            sendEmail.send()

            return redirect('login')
        else:
            
            messages.info(request, 'Get Request')

    else:
        print('Get request 6')
        form = registerForm()
        
     
    return render(request, 'store/register.html', {'form': form})


def login(request):
    form = loginForm()

    if request.method == 'POST':
        form = loginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            print(username, '=============================')

            user = authenticate(request, name=username, password=password)

            print('Authentications Correct')
            user = Customer.objects.get(name=username)
            if password == user.password or username == user.email:
                return redirect('home')   
            else:
                messages.info(request, 'Invalide Credentials') 
                return redirect('login')  
    else:
        form = loginForm() 

    return render(request, 'store/login.html', {'form':form})


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items    = order.orderitem_set.all()
        cartItems = order.get_cart_items    
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        

       
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items    = order.orderitem_set.all()
        cartItems = order.get_cart_items    
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order  = cookieData['order']
        items  = cookieData['items']
        
    context = {'cartItems':cartItems, 'order':order, 'items':items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items    = order.orderitem_set.all()
        cartItems = order.get_cart_items    
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order  = cookieData['order']
        items  = cookieData['items']   
 
    context = {'cartItems':cartItems, 'order':order, 'items':items}

    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data      = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId', productId)
    print('Action:',action)


    customer  = request.user.customer
    print(customer, 'customer ====================')
    product   = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
         orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()  


    return JsonResponse('Item was added', safe=False)

      

# from django.views.decorators.csrf import csrf_exempt 

# @csrf_exempt
def processOrder(request):
    
    print('Data:', request.body, '=====================')

    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data  = json.loads(request.body)
    print(data, 'data000000000000000000000000000000000')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
        
    total   = float(data['form']['total'])
    print(total, '===============================')
    print(transaction_id, 'transaction Id')
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True 
    order.save()
    print('Data Saved==========================')
    print('hello ======================================================================')

    if order.shipping == False:
        shiping_details = ShippingAddress.objects.create(
            customer = customer,
            order    = order,
            address  = data['shipping']['address'],
            city  = data['shipping']['city'],
            state  = data['shipping']['state'],
            zipcode  = data['shipping']['zipcode'],
            
        )
        print('===DETAILS SAVED========')
    else:
        print('-------------------Invalide credentials--------------------------')

    
    email = request.user.email
    request.session['customer_email'] = email
    email_notifications(request)

    return JsonResponse('payment complete !', safe=False)

def email_notifications(request):
    email = request.session['customer_email']
    message = 'Dear Customer , Your order has been placed successfully'

    sendEmail = EmailMessage(
        'Owusuwa Collection',
        message,
        settings.EMAIL_HOST_USER,
        [email]
    )
    sendEmail.fail_silently = True
    sendEmail.send()

    return render(request, 'store/checkout.html')









    