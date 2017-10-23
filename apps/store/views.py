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

def addItem(request,number):
    print request.POST['quantity']
    quantity = request.POST['quantity']
    the_item = Item.objects.get(id = number)
    a = User.objects.get(id = request.session['id'])
    Cart.objects.create(quantity = quantity, item = the_item, user = a)
    b = Cart.objects.filter( user = a)
    print b
    return redirect('/items')

def logout(request):
    request.session['id'] = ""
    return redirect('/')

def checkout(request):
    a = User.objects.filter(id = request.session['id'])
    b = Cart.objects.filter(user__id = request.session['id'])
    print b
    return render(request, 'store/checkout.html')

