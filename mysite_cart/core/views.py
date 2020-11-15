from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views import generic
from core.models import *

def home(request):
    return redirect('products')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return redirect('products')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('products')
    else:
        form = AuthenticationForm()
    return render(request, 'core/signin.html', {'form': form})

@login_required(login_url = signin)
def logout_view(request):
    logout(request)
    return redirect(home)


@login_required(login_url = signin)
def add_to_cart(request, product_id):
    Cart.objects.get_or_create(user=request.user)
    my_cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(id = product_id)
    Entry.objects.get_or_create(cart= my_cart, product=product)
    my_entry = Entry.objects.get(cart= my_cart, product=product)
    my_entry.quantity +=1
    my_cart.total += product.price
    my_entry.save()
    my_cart.save()
    return redirect('products')



@login_required(login_url = signin)
def remove_from_cart(request, product_id):
    Cart.objects.get_or_create(user=request.user)
    my_cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(id=product_id)
    Entry.objects.get_or_create(cart=my_cart, product=product)
    my_entry = Entry.objects.get(cart=my_cart, product=product)
    if my_entry.quantity >= 1:
        my_entry.quantity -=1
        my_cart.total -= product.price
        my_entry.save()
        my_cart.save()
    if my_entry.quantity == 0:
        my_entry.delete()
    return redirect('cart')

@login_required(login_url = signin)
def cart_view(request):
    Cart.objects.get_or_create(user=request.user)
    my_cart = Cart.objects.get(user=request.user)
    total = my_cart.total
    list_of_entries = Entry.objects.filter(cart=my_cart)
    return render(request, 'core/cart.html', {'list_of_entries': list_of_entries, 'total': total})

class ProductList(generic.ListView):
    model = Product