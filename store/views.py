from django.shortcuts import render
from .models import *
from django.http import JsonResponse 
import json 
import datetime 
from . utils import cookieCart , cartDate

# Create your views here.



def store(request):

    data       = cartDate(request)
    cartItems  = data['cartItems']
       
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)




def cart(request):
    data       = cartDate(request)
    cartItems  = data['cartItems']
    order      = data['order']
    items      = data['items']
       
        
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data       = cartDate(request)
    cartItems  = data['cartItems']
    order      = data['order']
    items      = data['items']
 
    context = {'items': items, 'order': order, 'cartItems':cartItems}

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

      

    # print('====================================')
    # data       = json.loads(request.body)
    # productId = data['productId']
    # action    = data['action']
    # print(productId)



    


def processOrder(request):

    print('Data:', request.body, '=====================')

    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data  = json.loads(request.body)
    print(data, 'data000000000000000000000000000000000')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total   = float(data['form']['total'])
        print(total, '===============================')
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True 
        order.save() 

        if order.shipping == False:
            shiping_details = ShippingAddress.objects.create(
                customer = customer,
                order    = order,
                address  = data['shipping']['address'],
                city  = data['shipping']['city'],
                state  = data['shipping']['state'],
                zipcode  = data['shipping']['zipcode'],
                
            )
            shiping_details.save()
            
        else:
            print('============================Invalide Shipping Details =====================================')
    else:
        print('customer is not loged in..')

    return JsonResponse('payment complete !', safe=False)