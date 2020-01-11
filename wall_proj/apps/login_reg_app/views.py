from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt

from .models import *


def index(request):
    if "currentUser" not in request.session:
        return render(request, "login_reg_app/index.html")
    else:
        return redirect("/wall")


def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":
            password = request.POST["password"]
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            newUser = User.objects.create(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                password=pw_hash,
                birthday=request.POST["birthday"]
            )
            if "currentUser" not in request.session:
                request.session["currentUser"] = newUser.id
            return redirect("/wall")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":
            thisUser = User.objects.filter(email=request.POST["email"]).first()
            if thisUser:
                if bcrypt.checkpw(request.POST["password"].encode(), thisUser.password.encode()):
                    if "currentUser" not in request.session:
                        request.session["currentUser"] = thisUser.id
                        return redirect("/wall")
                return redirect("/")
            return redirect("/")


def logout(request):
    if "currentUser" not in request.session:
        return redirect("/")
    else:
        request.session.clear()
        return redirect("/")
