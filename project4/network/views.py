import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

def index(request):
    if request.method == "POST":
        post = request.POST["text"]

        if not post:
            messages.warning(request, 'you must add post')
            return HttpResponseRedirect(reverse("index"))
            
        createPost = Post.objects.create(
            text=post,
            user = User.objects.get(pk = request.user.id)
        )
        createPost.save()   
        messages.success(request, 'Post have be success')
        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        posts = Post.objects.annotate(
            is_liked=Exists(
                Like.objects.filter(user=request.user, post=OuterRef('pk'))
            )
        ).select_related('user').order_by('created_at')[::-1]

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            'page_objects': page_obj
        })
    
    contact_list = Post.objects.all().select_related('user').order_by('created_at')[::-1]
    paginator = Paginator(contact_list, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    return render(request, 'network/index.html', {'page_obj': page_obj})

def following(request):
    posts = Post.objects.filter(
        user__followers__in = Follow.objects.filter(follower = request.user)
    ).annotate(
        is_liked=Exists(
            Like.objects.filter(user=request.user, post=OuterRef('pk')) 
        )
    ).select_related('user').order_by('created_at')[::-1]

    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)
    
    return render(request, 'network/following.html', {'page_objects': page_obj})

def profile(request, user_id):
    followers = Follow.objects.filter(following_id=user_id).count()
    following = Follow.objects.filter(follower_id=user_id).count()
    contact_list = Post.objects.filter(user=user_id).annotate(
            is_liked=Exists(
                Like.objects.filter(user=request.user, post=OuterRef('pk'))
            )
        ).select_related('user').select_related('user').order_by('created_at')[::-1]

    postCount = Post.objects.filter(user=user_id).count()
    is_followed = Follow.objects.filter(follower=request.user, following_id=user_id)
    paginator = Paginator(contact_list, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    try:
        profilePost = paginator.get_page(page_number)
    except EmptyPage:
        profilePost = paginator.get_page(1)

    return render(request, 'network/profile.html', {
        'page_objects': profilePost,
        "is_followed": is_followed,
        "followers": followers,
        "following": following,
        "profile": User.objects.get(pk=user_id),
        "postCount": postCount
    })

def editProfile(request, user_id):
    if request.method == "POST":
        image = request.POST["image"]
        bio = request.POST["changeBio"]
        user = User.objects.get(pk=user_id)

        if image:
            user.image = image
            user.save()
            return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))
        if bio:
            user.bio = bio
            user.save()
            return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))

        user.bio = user.bio
        user.image = user.image
        user.save()

    return render(request, 'network/profile.html')


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

def like(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    Like.objects.create(
        user=request.user,
        post=Post.objects.get(id=post_id),
        like=True
    )
    return HttpResponse(status=204)

def unlike(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    Like.objects.get(
        user=request.user,
        post=Post.objects.get(id=post_id)
    ).delete()
    return HttpResponse(status=204)


def follow(request, user_id):
    Follow.objects.create(follower=request.user, following_id=user_id)
    return HttpResponseRedirect(reverse("profile", kwargs=({"user_id": user_id})))

def unfollow(request, user_id):
    Follow.objects.filter(follower=request.user, following_id=user_id).delete()
    return HttpResponseRedirect(reverse("profile", kwargs=({"user_id": user_id})))

def comment(request, user_id):
    if request.method == "POST":
        comment = request.POST["comment"]
    
        if not comment:
            messages.warning(request, 'you must add comment')
            return HttpResponseRedirect(reverse("comment", kwargs={'user_id':user_id}))

        addcomment = Comment.objects.create(
            comment = comment,
            user = User.objects.get(pk = request.user.id),
            post = Post.objects.get(pk=user_id),
        ) 
        addcomment.save()
        
        messages.success(request, 'comment have be success')
        return HttpResponseRedirect(reverse("comment", args=(user_id,)))

    return render(request, "network/comments.html", {
        "comment": Post.objects.get(pk = user_id),
        "selectComment": Comment.objects.filter(post = user_id),
    })

@csrf_exempt
def editPost(request, post_id):
    post = Post.objects.get(pk=post_id);
    data = json.loads(request.body)
    if data.get("newPost") is not None:
        post.text = data["newPost"]
    post.save()
    return HttpResponse(status=204)


def deletePost(request, delete_id):
    try:
        Post.objects.get(pk=delete_id).delete()
    except:
        return HttpResponse(status=502)
    return HttpResponse(status=200)