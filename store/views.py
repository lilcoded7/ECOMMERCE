from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse 
import json 
import datetime 

from django.contrib import messages  
from django.conf import settings 
from .utils import cookieCart, Email, cartData
from django.conf import settings 
from django.core.mail import EmailMessage
from .forms import RegisterForm, loginForm, VerifyForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def search(request):

    if request.method == 'POST':
        searchitem = request.POST['search']
        
        search_product = Product.objects.filter(name=searchitem)
        
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']

        context = {'searach_product': searach_product, 'cartItems':cartItems}
        return render(request, 'store/search.html', context)

    cookieData = cookieCart(request)
    cartItems  = cookieData['cartItems']

    context = {'cartItems':cartItems}
    
    return render(request, 'store/search.html', context)


def store(request):

    if request.method == 'POST':
        searchitem = request.POST['search']
        
        searach_product = Product.objects.filter(name=searchitem)
        context = {'searach_product': searach_product}

        return render(request, 'store/search.html', context)


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
    return render(request, 'store/index.html', context)


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
    return render(request, 'store/order-details.html', context)

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
    print(data,'000000000000000000000000000000000')
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
        print('COOKIES:', request.COOKIES)
        name  = data['form']['name']
        email  = data['form']['email']

        cookieData = cookieCart(request)
        items      = cookieData['items']

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(customer=customer,complete=False)

        for item in items:
                
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
        
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

    # data = {
    #     'email_subject': 'JOETOP',
    #     'email_body'   : 'Dear Customer Your Order has been placed successfully',
    #     'to_email'     : email,
    # } 
    # Email.send_email(data)
    return JsonResponse('payment complete !', safe=False)











    