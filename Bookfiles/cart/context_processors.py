from .cart import Cart

def cart(request):
    """
    Returns the initialized Cart instance globally to all HTML templates.
    """
    return {'cart': Cart(request)}