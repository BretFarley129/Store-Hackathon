# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    if not 'id' in request.session:
        request.session['id'] = ""
    return render(request, 'store/index.html')

def dummy(request):
    return render(request, 'store/dummy.html')

def register(request):
    context ={}
    context['stuff'] = User.objects.all()
    return render(request, 'store/register.html',context)

def processreg(request):
    postData = {
        'username': request.POST['username'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm_password': request.POST['confirm_password'],
    }
    errors = User.objects.validate_reg(postData)
    if len(errors) == 0:
        if not 'cart' in request.session:
            request.session['cart'] = []
        x = len(Item.objects.all())
        for i in range(0, x):
            request.session['cart'].append(0)
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        

        return redirect('/')
    else:
        for error in errors:
            messages.info(request, error)
        return redirect('/register')

def login(request):
    return render(request, 'store/login.html')

def processlog(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    errors = User.objects.validate_log(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['username'] = User.objects.filter(email=postData['email'])[0].username
        if not 'cart' in request.session:
            request.session['cart'] = []
        x = len(Item.objects.all())
        for i in range(0, x):
            request.session['cart'].append(0)
        return redirect('/')
    for error in errors:
        messages.info(request, error)
    return redirect('/login')

def product(request, number):
    context = {}
    context['stuff'] = Item.objects.filter(id = number)
    return render(request, 'store/product.html', context)

def items(request):
    context = {}
    context['stuff'] = Item.objects.all()
    return render(request, 'store/items.html', context)
def confirmation(request):
    return render(request, 'store/confirmation.html')

def addItem(request,number):
    quantity = request.POST['quantity']
    print quantity
    cart_index = int(number) - 1
    print cart_index
    temp = request.session['cart']
    temp[cart_index] += int(quantity)
    request.session['cart'] = temp
    print request.session['cart']
    
    return redirect('/items')

def logout(request):
    request.session['id'] = ""
    request.session['cart'] = []
    return redirect('/')

def remove(request, number):
    cart_index = int(number) - 1
    temp = request.session['cart']
    temp[cart_index] = 0
    request.session['cart'] = temp
    
    return redirect('/checkout')

def checkout(request):
    context = {'item': [], 'quant': [], 'count': 0, 'total': 0}
    a = Item.objects.all()
    print len(a)
    print request.session['cart']
    for i in range(0,len(a)):
        if request.session['cart'][i] > 0:
            context['item'].append(Item.objects.get(id = (i+1)))
            context['quant'].append(request.session['cart'][i])
            context['count'] += 1
            context['total'] += Item.objects.get(id = (i+1)).price * float(request.session['cart'][i])

    return render(request, 'store/checkout.html',context)

