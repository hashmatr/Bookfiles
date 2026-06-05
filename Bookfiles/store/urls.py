from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # 1. Main Store Landing Homepage
    path('', views.home, name='home'),
    
    # 2. Filtering View by Selected Category
    path('category/<slug:category_slug>/', views.home, name='category_list'),
    
    # 3. Individual Book Details View Page
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]
