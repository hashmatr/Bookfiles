from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm

# 1. Registration View
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Automatically log in the user after a successful signup
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect('store:home') # We'll create this home view shortly!

# 2. Login View (Extending Django's built-in secure LoginView)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # If already logged in, redirect away from login page