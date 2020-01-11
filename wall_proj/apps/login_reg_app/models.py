from django.db import models
from datetime import datetime, date, timedelta
import re
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        nums = set('01234567890')
        if len(postData['first_name']) == 0 and len(postData['last_name']) == 0 and len(postData['email']) == 0 and len(postData['birthday']) == 0 and len(postData['password']) == 0 and len(postData["password_confirm"]) == 0:
            errors["george_protocol"] = "All fields are required."
            return errors
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        if any((c in nums) for c in postData['first_name']):
            errors["first_name_nums"] = "Please don't use numbers in your first name."
        if any((c in nums) for c in postData['last_name']):
            errors["first_name_nums"] = "Please don't use numbers in your last name."
        if len(postData["email"]) == 0:
            errors["blank_email"] = "Please enter your email."
        if len(postData["email"]) != 0:
            if not email_regex.match(postData['email']):
                errors["bad_email"] = "Please use a valid email address."
            if len(User.objects.filter(email=postData['email'])) != 0:
                errors["taken_email"] = "This email is already associated with an account." 
        if len(postData["birthday"]) == 0:
            errors["blank_birthday"] = "Please enter your birthday."
        if len(postData["birthday"]) != 0:   
            if datetime.strptime(postData['birthday'], '%Y-%d-%j') > datetime.today():
                errors["bad_birthday"] = "Your birthday needs to be in the past."
            if datetime.strptime(postData['birthday'], '%Y-%d-%j') > datetime.today() - timedelta(days = 4745):
                errors["young_birthday"] = "You must be at least 13 years of age to register."
            if datetime.strptime(postData['birthday'], '%Y-%d-%j') < datetime.today() - timedelta(days = 43800):
                errors["old_birthday"] = "Are you sure you entered your birthday correctly?"
        if len(postData['password']) < 8:
            errors["short_password"] = "Password should be at least 8 characters."
        if postData['password'] != postData["password_confirm"]:
            errors["mismatch_password"] = "Your two passwords don't match! Try again."
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(postData["email"]) == 0 or len(postData["password"]) == 0:
            errors["blank"] = "Please enter your email address and password to log in."
            return errors
        user = User.objects.filter(email=postData["email"]).first()
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):
            errors["email"] = "Please use a valid email address."
        if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
            errors["password"] = "Incorrect password - please try again."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    objects = UserManager()
