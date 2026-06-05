from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    """
    Adds a book safely to the session-based shopping cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Pass product.id explicitly as an integer number to the cart instance method
    cart.add(product_id=product.id, quantity=1, override_quantity=False)
    
    return redirect(request.META.get('HTTP_REFERER', 'store:home'))


def cart_detail(request):
    """
    Renders the active session shopping cart overview page.
    """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})