from operator import mod
from statistics import mode
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(max_length=700, null=True)
    bio = models.CharField(max_length=255, null=True)

class Post(models.Model):
    post = models.CharField(max_length=64)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.post} {self.userId} {self.created_at} {self.userId}"

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "following", null=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "follower", null=True)

    def __str__(self):
        return f"{self.following} {self.follower}"

class Like(models.Model):
    like = models.BooleanField(default=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.like} {self.userId} {self.postId}"

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.comment} {self.userId} {self.postId}"
