from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from store.models import Product

def order_create(request):
    cart = Cart(request)
    
    # Block empty submissions
    if len(cart) == 0:
        return redirect('store:home')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Build the order record but hold database insertion briefly
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            # Record global totals
            order.total_paid = cart.get_total_price()
            order.save()

            # Transfer each item from the session cart into database line items
            for product_id, item in cart.cart.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=item['quantity']
                    )
                except Product.DoesNotExist:
                    continue

            # Empty the user's session cart
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        # Pre-fill form details automatically if the user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'email': request.user.email,
                'phone_number': getattr(request.user, 'phone_number', ''),
                'shipping_address': getattr(request.user, 'shipping_address', '')
            }
        form = OrderCreateForm(initial=initial_data)
        
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})