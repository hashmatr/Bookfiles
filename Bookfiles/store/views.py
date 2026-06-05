from django.shortcuts import render
from .models import Product  # We can pull our products later!

def home(request):
    """
    Renders the main homepage layout of the BookFiles store.
    """
    return render(request, 'store/home.html')