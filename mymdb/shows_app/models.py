from django.db import models
from datetime import datetime
from login_app.models import User
import urllib.request
import os

# Create your models here.


class ShowManager(models.Manager):
    def basicValidator(self, postData):
        errors = {}

        if(len(postData['title']) == 0):
            errors['title'] = "Show title must contain at least one character."
        # if(len(postData['image']) == 0):
        #     errors['image'] = "Image path must be included."

        return errors


class NetworkManager(models.Manager):
    def basicValidator(self, postData):
        errors = {}

        if(len(postData['name']) == 0):
            errors['name'] = "Show name must contain at least one character."
        if(len(postData['image']) == 0):
            errors['image'] = "Image path must be included."

        return errors


class GenreManager(models.Manager):
    def basicValidator(self, postData):
        errors = {}

        if(len(postData['genre']) == 0):
            errors['genre'] = "Genre name must contain at least one character."

        return errors


class Network(models.Model):
    user = models.ForeignKey(User, related_name="network", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    image = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = NetworkManager()


class Genre(models.Model):
    user = models.ForeignKey(User, related_name="genres", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = GenreManager()


class Show(models.Model):
    user = models.ForeignKey(User, related_name="shows", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    medium = models.CharField(max_length=45, null=True)
    genre = models.ManyToManyField(Genre, related_name="shows")
    total_seasons = models.IntegerField(null=True)
    total_episodes = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    release_date = models.DateField(null=True)
    description = models.TextField(null=True)
    image = models.TextField(null=True)
    photo = models.FileField(upload_to=f"posters/", blank=True)
    network = models.ForeignKey(Network, related_name="shows", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = ShowManager()

    def cache(self):
        """Store image locally if we have a URL"""

        # if self.image and not self.photo:
        result = urllib.request.urlretrieve(self.image)
        if (self.image[-4:] == ".jpeg"):
            fileExtension = ".jpg"
        elif (self.image[-4:] != ".jpg" or self.image[-4:] != ".png"):
            fileExtension = ".jpg"
        else:
            fileExtension = self.image[-4:]
        self.photo.save(
            os.path.basename(f"{self.id}_poster{fileExtension}"),
            open(result[0], 'rb')
        )
        self.save()


class Wlist(models.Model):
    list_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, related_name="watchlist", on_delete=models.CASCADE)
    show = models.ManyToManyField(Show, related_name="watchlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE, null=True)
    show = models.ForeignKey(Show, related_name="reviews", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    score = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


# class Comment(models.Model):
#     review = models.ForeignKey(Review, related_name="comments", on_delete=models.CASCADE, null=True)
#     score = models.IntegerField()
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now_add=True)
