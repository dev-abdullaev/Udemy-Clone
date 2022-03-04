from django.urls import path

from . import views


urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<slug:slug>/', views.cart_add, name='cart_add'),
    path('remove/<slug:slug>', views.cart_remove, name='cart_remove'),
    path('checkout', views.cart_checkout, name='cart_checkout'),
    path('payment/', views.payment, name='payment'),
]