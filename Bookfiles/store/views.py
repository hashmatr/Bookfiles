from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def home(request, category_slug=None):
    """
    Renders the shop storefront. Displays either all products or filters 
    them smoothly based on a selected category slug.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/home.html', context)


def product_detail(request, slug):
    """
    Queries a single unique book detail view page based on its URL slug.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'store/detail.html', {'product': product})