from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
     def user_validator(self, postData):
        valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name needs to be minimum 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name needs to be minimum 2 characters"
        if not valid_email.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email = postData['email']).exists():
            errors['email_uniqueness'] = "Account already exists with this email"
        if len(postData['password']) < 8:
            errors['password_len'] = "Password needs to be atleast 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Password does not match"
        return errors
     
     
     def edit_validator(self, postData):
        valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        error_messages = {}
        if len(postData['updated_first_name']) < 2:
            error_messages['updated_first_name'] = "First Name needs to be minimum 2 characters"
        if len(postData['updated_last_name']) < 2:
            error_messages['updated_last_name'] = "Last Name needs to be minimum 2 characters"
        if not valid_email.match(postData['updated_email']):    # test whether a field matches the pattern            
            error_messages['updated_email'] = "Invalid email address!"
        if User.objects.filter(email = postData['updated_email']).exists():
            error_messages['updated_email_uniqueness'] = "Account already exists with this email"
        return error_messages


class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        error_mess = {}
        if len(postData['author']) < 3:
            error_mess['author'] = "The author section requires more than 3 characters"
        if len(postData['quote']) < 10:
            error_mess['quote'] = "The quotes section requires more than 10 characters"
        return error_mess


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    user = models.ForeignKey(User, related_name='quotes', on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = QuoteManager()

class Like_quote(models.Model):
    like = models.CharField(max_length=5, default='Like')
    user = models.ForeignKey(User, related_name="like_quotes", on_delete= models.CASCADE)
    quote = models.ForeignKey(Quote, related_name="like_quotes", on_delete= models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)