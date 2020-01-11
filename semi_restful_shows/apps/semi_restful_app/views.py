from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# MAIN PAGES


def index(request):
    content = {
        "showList": Show.objects.all(),
    }
    return render(request, "semi_restful_app/shows.html", content)


def new(request):
    return render(request, "semi_restful_app/new.html")


def profile(request, show_id):
    content = {
        "thisShow": Show.objects.get(id=show_id),
    }
    return render(request, "semi_restful_app/profile.html", content)


def edit(request, show_id):
    content = {
        "thisShow": Show.objects.get(id=show_id),
    }
    return render(request, "semi_restful_app/edit.html", content)

# FORM SUBMISSIONS


def create(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/shows/new")
    else:
        if request.method == "POST":
            newShow = Show.objects.create(
                title=request.POST["title"],
                network=request.POST["network"],
                release_date=request.POST["release_date"],
                description=request.POST["description"]
            )
            return redirect(f"/shows/{newShow.id}")


def update(request, show_id):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/shows/{show_id}/edit")
    else:
        if request.method == "POST":
            thisShow = Show.objects.get(id=show_id)
            if thisShow.title != request.POST["title"] and request.POST["title"] != "":
                thisShow.title = request.POST["title"]
            if thisShow.network != request.POST["network"] and request.POST["network"] != "":
                thisShow.network = request.POST["network"]
            if thisShow.release_date != request.POST["release_date"] and request.POST["release_date"] != "":
                thisShow.release_date = request.POST["release_date"]
            if thisShow.description != request.POST["description"] and request.POST["description"] != "":
                thisShow.description = request.POST["description"]
            thisShow.save()
            messages.success(request, "This show is updated")
            return redirect(f"/shows/{thisShow.id}")


def destroy(request, show_id):
    thisShow = Show.objects.get(id=show_id)
    thisShow.delete()
    return redirect("/shows")

# REDIRECT


def redirectToShows(request):
    return redirect("/shows")
