from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'), # <-- Added this link route!
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
]