import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import (
    User,
    Profile,
    ProfilePictures,
    Post,
)
from .forms import (
    ProfileForm,
    ProfilePicturesForm,
    PostForm,
)


def index(request):
    form = ProfileForm()
    pictureForm = ProfilePicturesForm()
    postForm = PostForm()
    if request.user.id is not None:
        id = request.user.id
        profile = Profile.objects.get(pk=id)
        picture = ProfilePictures.objects.get(pk=id)
        form = ProfileForm(instance=profile)
        pictureForm = ProfilePicturesForm(instance=picture)
    return render(
        request,
        "network/index.html",
        {
            "form": form,
            "pictureForm": pictureForm,
            "postForm": postForm,
        },
    )


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request,
                "network/register.html",
                {
                    "message": "Passwords must match.",
                    "form": form,
                    "imageform": imageform,
                },
            )
        form = ProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            pronouns = form.cleaned_data["pronouns"]
            bio = form.cleaned_data["bio"]
        else:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(
                request,
                "network/register.html",
                {
                    "message": "Profile creation failed.",
                    "form": form,
                    "imageform": imageform,
                },
            )
        imageform = ProfilePicturesForm(request.POST, request.FILES)
        if imageform.is_valid():
            picture = imageform.cleaned_data["picture"]
        else:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(
                request,
                "network/register.html",
                {
                    "message": "Image upload failed.",
                    "form": form,
                    "imageform": imageform,
                },
            )
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            form = ProfileForm()
            imageform = ProfilePicturesForm()
            return render(
                request,
                "network/register.html",
                {
                    "message": "Username already taken.",
                    "form": form,
                    "imageform": imageform,
                },
            )
        profile = Profile(username_id=user.id, name=name, pronouns=pronouns, bio=bio)
        profile.save()
        profilePicture = ProfilePictures(user_id=user.id, picture=picture)
        profilePicture.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = ProfileForm()
        imageform = ProfilePicturesForm()
        return render(
            request,
            "network/register.html",
            {
                "form": form,
                "imageform": imageform,
            },
        )


def watch_profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    following_list = []
    following = [user.username for user in request.user.follower.all()]
    for user in following:
        following_list.append(user.profile.serialize())
    return JsonResponse(
        {"profile": [profile.serialize()], "following_list": following_list}, safe=False
    )


def watch_profile_picture(request):
    profilepicture = ProfilePictures.objects.get(pk=request.user.id)
    return JsonResponse([profilepicture.serialize()], safe=False)


def set_profile(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        id = request.user.id
        data = json.loads(request.body)
        profile = Profile.objects.get(pk=id)
        try:
            profile.name = data["name"]
            profile.pronouns = data["pronouns"]
            profile.bio = data["bio"]
            profile.save()
            return JsonResponse(
                {"message": "Profile updated successfully."}, status=201
            )
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
            try:
                profile.picture = form.cleaned_data["picture"]
                profile.save()
            except:
                return render(
                    request, "network/index.html", {"error": "Image update failed"}
                )
        form = ProfileForm()
    pictureForm = ProfilePicturesForm()
    if request.user.id is not None:
        id = request.user.id
        profile = Profile.objects.get(pk=id)
        picture = ProfilePictures.objects.get(pk=id)
        form = ProfileForm(instance=profile)
        pictureForm = ProfilePicturesForm(instance=picture)
    return render(
        request,
        "network/index.html",
        {
            "message": "Image updated successfully",
            "form": form,
            "pictureForm": pictureForm,
        },
    )


def submit_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        id = request.user.id
        if id is not None:
            data = json.loads(request.body)
            try:
                post = Post(poster_id=id, content=data["content"])
                post.save()
                return JsonResponse(
                    {"message": "Post uploaded successfully."}, status=201
                )
            except:
                return JsonResponse(
                    {"error": "Post failed to be uploaded."}, status=500
                )
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
            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            max_page = paginator.num_pages
            page_obj = paginator.get_page(page_number)
            return JsonResponse(
                {
                    "maxPage": max_page,
                    "posts": [post for post in page_obj],
                },
                safe=False,
            )
        else:
            posts = Post.objects.all()
            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            max_page = paginator.num_pages
            page_obj = paginator.get_page(page_number)
            return JsonResponse(
                {
                    "maxPage": max_page,
                    "posts": [post.serialize(id) for post in page_obj],
                },
                safe=False,
            )
    elif page == "following":
        if request.user.id is not None:
            id = request.user.id
            profile = Profile.objects.get(pk=id)
            following = profile.followers.all()
            posts = Post.objects.all()
            posts = [post.serialize(id) for post in posts if post.poster in following]
            print(posts)
            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            max_page = paginator.num_pages
            page_obj = paginator.get_page(page_number)
            return JsonResponse(
                {
                    "maxPage": max_page,
                    "posts": [post for post in page_obj],
                },
                safe=False,
            )
        else:
            return JsonResponse({"error": "User not logged in."}, status=403)
    elif page == "profile":
        if request.user.id is not None:
            id = request.user.id
            profile = Profile.objects.get(pk=id)
            posts = Post.objects.all()
            posts = [
                post.serialize(id) for post in posts if post.poster == profile.username
            ]
            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            max_page = paginator.num_pages
            page_obj = paginator.get_page(page_number)
            return JsonResponse(
                {
                    "maxPage": max_page,
                    "posts": [post for post in page_obj],
                },
                safe=False,
            )
        else:
            return JsonResponse({"error": "User not logged in."}, status=403)
    else:
        return JsonResponse({"error": "Invalid page."}, status=400)


def watch_user_posts(request, username):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    try:
        user = User.objects.get(username=username)
        id = request.user.id
        posts = Post.objects.filter(poster=user)
        posts = [post.serialize(id) for post in posts]
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        max_page = paginator.num_pages
        page_obj = paginator.get_page(page_number)
        return JsonResponse(
            {
                "maxPage": max_page,
                "posts": [post for post in page_obj],
            },
            safe=False,
        )
    except:
        return JsonResponse({"error": "User not found."}, status=404)


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
            return JsonResponse(
                {"message": "Post liked successfully.", "likes": post.likes.count()},
                status=201,
            )
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
            return JsonResponse(
                {"message": "Post unliked successfully.", "likes": post.likes.count()},
                status=201,
            )
        except:
            return JsonResponse({"error": "Post failed to be unliked."}, status=500)


def watch_user(request, username):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(username_id=user.id)
        profilePicture = ProfilePictures.objects.get(user_id=user.id)
        following_list = []
        following = [user.username for user in user.follower.all()]
        for user in following:
            following_list.append(user.profile.serialize())
        if profile.username.follower.filter(pk=request.user.id).exists():
            followed = True
        else:
            followed = False
        return JsonResponse(
            {
                "profile": [profile.serialize()],
                "picture": [profilePicture.serialize()],
                "following_list": following_list,
                "followed": followed,
            },
            safe=False,
        )
    except:
        return JsonResponse({"error": "User not found."}, status=404)


def watch_user_picture(request, username):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    try:
        user = User.objects.get(username=username)
        profilePicture = ProfilePictures.objects.get(user_id=user.id)
        return JsonResponse([profilePicture.serialize()], safe=False)
    except:
        return JsonResponse({"error": "User not found."}, status=404)


def follow(request, method):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        if request.user.id is not None:
            if method == "follow":
                data = json.loads(request.body)
                user = User.objects.get(username=data["username"])
                follower = Profile.objects.get(username_id=request.user.id)
                try:
                    follower.followers.add(user)
                    follower.save()
                    return JsonResponse(
                        {
                            "message": "User followed successfully.",
                            "followers": user.follower.count(),
                        },
                        status=200,
                    )
                except:
                    return JsonResponse(
                        {"error": "User failed to be followed."}, status=500
                    )
            else:
                data = json.loads(request.body)
                user = User.objects.get(username=data["username"])
                follower = Profile.objects.get(username_id=request.user.id)
                try:
                    follower.followers.remove(user)
                    user.save()
                    return JsonResponse(
                        {
                            "message": "User unfollowed successfully.",
                            "followers": user.follower.count(),
                        },
                        status=200,
                    )
                except:
                    return JsonResponse(
                        {"error": "User failed to be unfollowed."}, status=500
                    )
        else:
            return JsonResponse({"error": "User not logged in."}, status=400)

def edit_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        data = json.loads(request.body)
        id = data["post_id"]
        post = Post.objects.get(pk=id)
        if post.poster == request.user:
            try:
                post.content = data["content"]
                post.save()
                return JsonResponse(
                    {"message": "Post edited successfully.", "content": post.content},
                    status=201,
                )
            except:
                return JsonResponse({"error": "Post failed to be edited."}, status=500)
        else:
            return JsonResponse({"error": "User not authorized."}, status=403)