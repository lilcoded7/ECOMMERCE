from django.urls import path
from . import views



urlpatterns = [
    path('home/', views.store, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    # path('', views.index, name='index'),
    path('register/', views.register)
    
    
]