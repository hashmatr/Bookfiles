from decimal import Decimal

class Cart:
    def __init__(self, request):
        """
        Initialize the cart using Django's session framework.
        """
        self.session = request.session
        # Get the cart from the session, or create an empty dict if it doesn't exist
        cart = self.session.get('session_cart')
        if not cart:
            cart = self.session['session_cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product_id) # Session keys must be strings
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
            
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        self.save()

    def remove(self, product_id):
        """
        Remove a product from the shopping cart.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # Mark the session as modified to make sure Django updates the cookie
        self.session.modified = True

    def clear(self):
        # Remove cart entirely from session
        del self.session['session_cart']
        self.save()

    def __len__(self):
        """
        Count all individual items currently sitting in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())