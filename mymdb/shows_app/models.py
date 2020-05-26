from django.db import models
from datetime import datetime
from login_app.models import User

# Create your models here.


class ShowManager(models.Manager):
    def basicValidator(self, postData):
        errors = {}

        if(len(postData['title']) == 0):
            errors['title'] = "Show title must contain at least one character."
        if(len(postData['image']) == 0):
            errors['image'] = "Image path must be included."

        return errors


class NetworkManager(models.Manager):
    def basicValidator(self, postData):
        errors = {}

        if(len(postData['name']) == 0):
            errors['name'] = "Show name must contain at least one character."
        if(len(postData['image']) == 0):
            errors['image'] = "Image path must be included."

        return errors


class Network(models.Model):
    user = models.ForeignKey(User, related_name="network", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    image = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = NetworkManager()


class Show(models.Model):
    user = models.ForeignKey(User, related_name="show", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(null=True)
    image = models.TextField(null=True)
    network = models.ForeignKey(Network, related_name="shows", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = ShowManager()


# class Review(models.Model):
#     reviewer = models.ForeignKey(User, related_name="rev")
#     show = models.ForeignKey(Show, related_name="review", on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=255)
#     score = models.IntegerField(ma)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now_add=True)


# class Comment(models.Model):
#     review = models.ForeignKey(Review, related_name="comments", on_delete=models.CASCADE, null=True)
#     score = models.IntegerField()
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now_add=True)
