# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import md5
import os, binascii

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_reg(self, postData):
        print '~~~~~~~~~~~'
        errors = []
        print postData
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        #validation block
        if len(postData['username']) < 2:
            errors.append("Username name must be at least 2 characters")
        if len(postData['password']) < 8:
            errors.append('Password needs to be at least 8 characters')
        if not my_re.match(postData['email']):
            errors.append("Please enter a valid email format")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append('email already in use')
        if postData['password'] != postData['confirm_password']:
            errors.append('Passwords do not match')
        
        #success block
        if len(errors) == 0:
            salt = binascii.b2a_hex(os.urandom(15))
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            User.objects.create(username=postData['username'], email=postData['email'], salt=salt, password=hashed_pw)

        return errors
    
    def validate_log(self, postData):
        errors = []
        if User.objects.filter(email=postData['email']):
            salt = User.objects.get(email=postData['email']).salt
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            if User.objects.get(email=postData['email']).password != hashed_pw:
                errors.append('Incorrect password')
        else:
            errors.append('Email has not been registered')
        return errors

class User(models.Model):
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()

    salt = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.username, self.email, self.password)

class Cart(models.Model):
    quantity = models.IntegerField()
    user = models.ForeignKey(User, related_name = "cart")
    def __str__(self):
        return "Item: \n{}\n{}\n".format(self.quantity, self.user)
    def __repr__(self):
        return "Item: \n{}\n{}\n".format(self.quantity, self.user)

class Item(models.Model):
    name = models.CharField(max_length = 255)
    desc = models.TextField()
    price = models.FloatField()
    image = models.CharField(max_length = 255)
    

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "Item: \n{}\n{}\n{}\n{}\n".format(self.id, self.name, self.price, self.desc)
    def __str__(self):
        return "Item: \n{}\n{}\n{}\n{}\n".format(self.id, self.name, self.price, self.desc)
    

class Store(models.Model):
    quantity = models.IntegerField()
    items = models.ForeignKey(Item, related_name="store")