from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date


class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters."
        if len(postData['network']) < 3:
            errors["network"] = "Network should be at least 3 characters."
        if len(postData['release_date']) == 0:
            errors["no_date"] = "Enter a release date."
        if datetime.strptime(postData['release_date'], '%Y-%d-%j') > datetime.today():
            errors["invalid_date"] = "The release date should be in the past."
        if len(postData['description']) < 10:
            errors["description"] = "Description should be at least 10 characters."
        return errors


class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=45)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()
