from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.request import QueryDict
import bcrypt

from .models import User, Location, UserManager

def test(request):
    return render(request, "main/test.html")


def index(request):
    if "currentUser" not in request.session:
        return render(request, "main/index.html")
    return redirect("/dashboard")


def dashboard(request):
    if "currentUser" not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.filter(id=request.session['currentUser']).first(),
    }
    return render(request, "main/dashboard.html", context)


def results(request):
    if "currentUser" not in request.session:
        return redirect("/")
    results = []
    for id in request.session["results"]:
        x = Location.objects.get(id=id)
        results.append(x)
    resultsLen = len(results)
    context = {
        "user": User.objects.filter(id=request.session['currentUser']).first(),
        "results": results,
        "resultsLen": resultsLen,
    }
    return render(request, "main/results.html", context)


def profile(request, location_id):
    if "currentUser" not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.filter(id=request.session['currentUser']).first(),
        "location": Location.objects.filter(id=location_id).first(),
    }
    return render(request, "main/profile.html", context)


def favorites(request):
    if "currentUser" not in request.session:
        return redirect("/")
    thisUser = User.objects.filter(id=request.session['currentUser']).first()
    favlist = thisUser.favorites.all()
    favlistLen = len(favlist)
    context = {
        "user": thisUser,
        "favlist": favlist,
        "favlistLen" : favlistLen,
    }
    return render(request, "main/favorites.html", context)


def process(request):
    #data = QueryDict(str(request.POST))
    #request.session["data"] = data

    searchList = []
    filterList = []
    finalList = []
    locationFilters = False
    
    for location in Location.objects.all():
        searchList.append(location.id)

    if "opt1" not in request.POST and "opt2" not in request.POST and "opt3" not in request.POST and "opt4" not in request.POST and "open" not in request.POST:
        for id in searchList:
            finalList.append(id)
        request.session["results"] = finalList
        return redirect("/results")

    if "opt1" in request.POST:
        locationFilters = True
        for id in searchList:
            x = Location.objects.get(id=id)
            if x.category == 1:
                filterList.append(id)
    if "opt2" in request.POST:
        locationFilters = True
        for id in searchList:
            x = Location.objects.get(id=id)
            if x.category == 2:
                filterList.append(id)
    if "opt3" in request.POST:
        locationFilters = True
        for id in searchList:
            x = Location.objects.get(id=id)
            if x.category == 3:
                filterList.append(id)
    if "opt4" in request.POST:
        locationFilters = True
        for id in searchList:
            x = Location.objects.get(id=id)
            if x.category == 4:
                filterList.append(id)

    if locationFilters == False:
        for x in searchList:
            filterList.append(x)

    if "open" in request.POST:
        for id in filterList:
            x = Location.objects.get(id=id)
            if x.year_round == "Yes":
                finalList.append(id)
    else:
        for id in filterList:
            finalList.append(id)

    request.session["results"] = finalList
    return redirect("/results")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    if request.method == "POST":
        thisUser = User.objects.filter(email=request.POST["email"]).first()
        if thisUser:
            if bcrypt.checkpw(request.POST["password"].encode(), thisUser.password.encode()):
                if "currentUser" not in request.session:
                    request.session["currentUser"] = thisUser.id
                    return redirect("/dashboard")
            return redirect("/")
    return redirect("/")


def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    if request.method == "POST":
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        newUser = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password=pw_hash,
        )
        if "currentUser" not in request.session:
            request.session["currentUser"] = newUser.id
    return redirect("/dashboard")


def logout(request):
    if "currentUser" not in request.session:
        return redirect("/")
    request.session.clear()
    return redirect("/")


def add_fav(request, location_id):
    if "currentUser" not in request.session:
        return redirect("/")
    thisLocation = Location.objects.filter(id=location_id).first()
    thisUser = User.objects.filter(id=request.session['currentUser']).first()
    thisLocation.fav_by.add(thisUser)
    thisLocation.save()
    return redirect("/results")


def remove_fav(request, location_id):
    if "currentUser" not in request.session:
        return redirect("/")
    thisLocation = Location.objects.filter(id=location_id).first()
    thisUser = User.objects.filter(id=request.session['currentUser']).first()
    thisLocation.fav_by.remove(thisUser)
    thisLocation.save()
    return redirect("/favorites")

def clear_search(request):
    if "results" in request.session:
        del request.session["results"]
    return redirect("/dashboard")