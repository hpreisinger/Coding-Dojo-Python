from django.db import models
from datetime import datetime, date, timedelta
import re
import bcrypt

from apps.login_reg_app.models import User, UserManager


class Message(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    can_edit = models.BooleanField()

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Message, related_name="comments")
    commenter = models.ForeignKey(User, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    can_edit = models.BooleanField()
