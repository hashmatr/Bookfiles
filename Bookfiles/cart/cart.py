from decimal import Decimal
from store.models import Product

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

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # Fetch actual Product objects from the database matching our cart IDs
        products = Product.objects.filter(id__in=product_ids)
        
        cart_copy = self.cart.copy()
        for product in products:
            cart_copy[str(product.id)]['product'] = product

        for item in cart_copy.values():
            # Dynamically attach the price and calculate the total line-item cost
            if 'product' in item:
                item['price'] = Decimal(item['product'].price)
                item['total_price'] = item['price'] * item['quantity']
                yield item

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
        if 'session_cart' in self.session:
            del self.session['session_cart']
        self.save()

    def __len__(self):
        """
        Count all individual items currently sitting in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculates the total cost of all items in the cart using live product prices.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = Decimal('0.00')
        
        for product in products:
            quantity = self.cart[str(product.id)]['quantity']
            total += Decimal(product.price) * quantity
        return total