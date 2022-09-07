from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Post, User

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

def index(request):
    if request.method == "POST":
        post = request.POST["text"]

        if not post:
            messages.warning(request, 'you must add post')
            return HttpResponseRedirect(reverse("index"))
            
        createPost = Post.objects.create(
            post=post,
            userId = User.objects.get(pk = request.user.id)
            
        )
        createPost.save()
        messages.success(request, 'Post have be success')
        return HttpResponseRedirect(reverse("index"))
    
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 3) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    return render(request, 'network/index.html', {'page_obj': page_obj})

def following(request):
    return render(request, "network/following.html" )

def profile(request):
    return render(request, "network/profile.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
