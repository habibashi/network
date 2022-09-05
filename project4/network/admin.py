from django.contrib import admin
from .models import Follow, User, Post, Like, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "created_at", "userId")

class UserAdmin(admin.ModelAdmin):
    list_display= ("username", "image", "bio")

class LikeAdmin(admin.ModelAdmin):
    list_display= ("like", "userId", "postId")

class CommentAdmin(admin.ModelAdmin):
    list_display= ("comment", "userId", "postId")

class FollowAdmin(admin.ModelAdmin):
    list_display= ("following", "follower")

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
