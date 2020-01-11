from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import date, datetime, timedelta, timezone

from .models import Message, Comment
from apps.login_reg_app.models import User, UserManager


def wall(request):
    if "currentUser" not in request.session:
        return redirect("/")
    else:
        for message in Message.objects.all():
            if message.created_at < datetime.now(timezone.utc) - timedelta(minutes = 30):
                message.can_edit = False
                message.save()
        for comment in Comment.objects.all():
            if comment.created_at < datetime.now(timezone.utc) - timedelta(minutes = 30):
                comment.can_edit = False
                comment.save()
        context = {
            "user": User.objects.filter(id=request.session['currentUser']).first(),
            "messageList": Message.objects.all().order_by("-created_at"),
        }
        return render(request, "wall_app/wall.html", context)


def postMessage(request):
    if request.method == "POST":
        if request.POST["content"] != "":
            poster = User.objects.filter(id=request.session['currentUser']).first()
            Message.objects.create(
                content=request.POST["content"],
                poster=poster,
                can_edit=True
            )
    return redirect("/wall")


def postComment(request):
    if request.method == "POST":
        if request.POST["content"] != "":
            commenter = User.objects.filter(id=request.session['currentUser']).first()
            post = Message.objects.filter(id=request.POST["post"]).first()
            Comment.objects.create(
                content = request.POST["content"],
                post = post,
                commenter = commenter,
                can_edit=True
            )
    return redirect ("/wall")

def deleteMessage(request):
    if request.method == "POST":
        message = Message.objects.filter(id=request.POST["message"]).first()
        message.delete()
    return redirect ("/wall")

def deleteComment(request):
    if request.method == "POST":
        comment = Comment.objects.filter(id=request.POST["comment"]).first()
        comment.delete()
    return redirect ("/wall")    


#TO FIX:
# going into HTML via Chrome and changing which comment gets deleted
# name as numbers