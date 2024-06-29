import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Profile, Followers, ProfilePictures, Post, Comments, Reply, Pictures, Hashtags
from .forms import ProfileForm, ProfilePicturesForm, PostForm, CommentsForm, ReplyForm, PicturesForm


def index(request):
    form = ProfileForm()
    pictureForm = ProfilePicturesForm()
    postForm = PostForm()
    print(request.user.id)
    if request.user.id is not None:
        id = request.user.id
        profile = Profile.objects.get(pk = id)
        picture = ProfilePictures.objects.get(pk = id)
        form = ProfileForm(instance=profile)
        pictureForm = ProfilePicturesForm(instance=picture)
    return render(request, "network/index.html", {
        "form": form,
        "pictureForm": pictureForm,
        "postForm": postForm,
    })


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
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(request, "network/register.html", {
                "message": "Passwords must match.",
                "form": form,
                "imageform": imageform,
            })
        form = ProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            pronouns = form.cleaned_data["pronouns"]
            bio = form.cleaned_data["bio"]
        else:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(request, "network/register.html", {
                "message": "Profile creation failed.",
                "form": form,
                "imageform": imageform,
            })
        imageform = ProfilePicturesForm(request.POST, request.FILES)
        if imageform.is_valid():
            picture = imageform.cleaned_data["picture"]
        else:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(request, "network/register.html", {
                "message": "Image upload failed.",
                "form": form,
                "imageform": imageform,
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(username=user, name=name, pronouns=pronouns, bio=bio)
            profile.save()
            profilepicture = ProfilePictures(user_id=profile.id, picture=picture)
            profilepicture.save()
        except IntegrityError:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(request, "network/register.html", {
                "message": "Username already taken.",
                "form": form,
                "imageform": imageform,
            })
        except:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(request, "network/register.html", {
                "message": "An unexpected error ocurred.",
                "form": form,
                "imageform": imageform,
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = ProfileForm()
        imageform = ProfilePicturesForm()
        return render(request, "network/register.html", {
            "form": form,
            "imageform": imageform,
        })
    

def watch_profile(request):
    profile = Profile.objects.get(pk = request.user.id)
    return JsonResponse([profile.serialize()], safe=False)

def watch_profile_picture(request):
    profilepicture = ProfilePictures.objects.get(pk = request.user.id)
    return JsonResponse([profilepicture.serialize()], safe=False)

def set_profile(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        id = request.user.id
        data = json.loads(request.body)
        profile = Profile.objects.get(pk=id)
        try:
            profile.name=data["name"]
            profile.pronouns=data["pronouns"]
            profile.bio=data["bio"]
            profile.save()
            return JsonResponse({"message": "Profile updated successfully."}, status=201)
        except:
            return JsonResponse({"error": "Profile update failed."}, status=500) 


def change_picture(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    if request.method == "POST":
        form = ProfilePicturesForm(request.POST, request.FILES)
        if form.is_valid():
            id = request.user.id
            profile = ProfilePictures.objects.get(pk=id)
            print(form.cleaned_data["picture"])
            try: 
                profile.picture = form.cleaned_data["picture"]
                profile.save()
            except:
                return render(request, "network/index.html", {
                    "error": "Image update failed"
                })
        form = ProfileForm()
    pictureForm = ProfilePicturesForm()
    print(request.user.id)
    if request.user.id is not None:
        id = request.user.id
        profile = Profile.objects.get(pk = id)
        picture = ProfilePictures.objects.get(pk = id)
        form = ProfileForm(instance=profile)
        pictureForm = ProfilePicturesForm(instance=picture)
    return render(request, "network/index.html", {
        "message": "Image updated successfully",
        "form": form,
        "pictureForm": pictureForm,
    })

def submit_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        id = request.user.id
        if id is not None:
            data = json.loads(request.body)
            try:
                post = Post(poster_id= id, content=data["content"])
                post.save()
                return JsonResponse({"message": "Post uploaded successfully."}, status=201)
            except:
                return JsonResponse({"error": "Post failed to be uploaded."}, status=500)
        else:
            return JsonResponse({"error": "User not logged in."}, status=400)

def watch_posts(request, page):
    if page == "posts":
        id = request.user.id
        if id is not None:
            user = User.objects.get(pk=id)
            posts = Post.objects.all()
            posts = [post.serialize(id) for post in posts]
            posts = [post for post in posts if post["poster"] != user.username]
            return JsonResponse(posts, safe=False)
        else:
            posts = Post.objects.all()
            return JsonResponse([post.serialize() for post in posts], safe=False)
    elif page == "followed":
        following = Followers.objects.filter(follower = request.user.id)
        posts = []
        for user in following:
            posts += Post.objects.filter(poster=user) 
        return JsonResponse([post.serialize() for post in posts], safe=False)
    
def like_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        data = json.loads(request.body)
        id = data["post_id"]
        post = Post.objects.get(pk=id)
        user = request.user.id
        try:
            post.likes.add(user)
            post.save()
            return JsonResponse({"message": "Post liked successfully.",
                                 "likes": post.likes.count()}, status=201)
        except:
            return JsonResponse({"error": "Post failed to be liked."}, status=500)

def unlike_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        data = json.loads(request.body)
        id = data["post_id"]
        post = Post.objects.get(pk=id)
        user = request.user.id
        try:
            post.likes.remove(user)
            post.save()
            return JsonResponse({"message": "Post unliked successfully.",
                                 "likes": post.likes.count()}, status=201)
        except:
            return JsonResponse({"error": "Post failed to be unliked."}, status=500)
