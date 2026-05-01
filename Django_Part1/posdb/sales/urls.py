from django.urls import path
from . import views

urlpatterns = [
    path('products/',              views.product_list,   name='product_list'),
    path('products/<int:pk>/',     views.product_detail, name='product_detail'),
    path('orders/',                views.order_list,     name='order_list'),
    path('orders/new/',            views.create_order,   name='create_order'),
    path('orders/<int:pk>/items/', views.add_item,       name='add_item'),
    path('orders/mine/', views.my_orders, name='my_orders'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
]
