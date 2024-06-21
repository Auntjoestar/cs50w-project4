from django import forms
from .models import Profile, ProfilePictures, Post, Comments, Reply, Pictures


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "pronouns", "bio"]


class ProfilePicturesForm(forms.ModelForm):
    class Meta:
        model = ProfilePictures
        fields = ["picture"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["reply"]


class PicturesForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ["picture"]

