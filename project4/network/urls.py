
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile", views.profile, name="profile"),
    path("editProfile", views.editProfile, name="editProfile"),
    path("post/like/<int:post_id>", views.like, name="like"),
    path("post/unlike/<int:post_id>", views.unlike, name="unlike")
]
