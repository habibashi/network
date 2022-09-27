from operator import mod
from statistics import mode
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(max_length=700, null=True)
    bio = models.CharField(max_length=255, null=True)

class Post(models.Model):
    text = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text} {self.user} {self.created_at}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "following", null=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "followers", null=True)

    def __str__(self):
        return f"{self.following} {self.follower}"

class Like(models.Model):
    like = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postLiked" ,null=True)

    def __str__(self):
        return f"{self.like} {self.user} {self.post}"

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.comment} {self.user} {self.post}"
