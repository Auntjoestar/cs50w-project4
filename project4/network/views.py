import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Profile, Followers, ProfilePictures, Post, Comments, Reply, Pictures, Hashtags
from .forms import ProfileForm, ProfilePicturesForm, PostForm, CommentsForm, ReplyForm, PicturesForm


def index(request):
    form = ProfileForm()
    pictureForm = ProfilePicturesForm()
    if request.user.id is not None:
        id = request.user.id
        profile = Profile.objects.get(pk = id)
        picture = ProfilePictures.objects.get(pk = id)
        form = ProfileForm(instance=profile)
        pictureForm = ProfilePicturesForm(instance=picture)
    return render(request, "network/index.html", {
        "form": form,
        "pictureForm": pictureForm,
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        form = ProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            pronouns = form.cleaned_data["pronouns"]
            bio = form.cleaned_data["bio"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(username=user, name=name, pronouns=pronouns, bio=bio)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = ProfileForm()
        return render(request, "network/register.html", {
            "form": form
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
        data = ProfilePicturesForm(request.FILES.keys())
        profile = Profile.objects.get(pk = id)
        try:
            profile.name=data["name"]
            profile.pronouns=data["pronouns"]
            profile.bio=data["bio"]
            profile.save()
            return JsonResponse({"message": "Profile updated successfully."}, status=201)
        except:
            return JsonResponse({"message": "Profile update failed."}, status=500) 


def change_picture(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"})
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
                    "message": "Image update failed"
                })
        return render(request, "network/index.html", {
                    "message": "Image updated successfully"
                })
