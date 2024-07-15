from django import forms
from .models import Profile, ProfilePictures, Post


class ProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}))
    pronouns = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Pronouns", "class": "form-control"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Bio", "class": "form-control"}))
    class Meta:
        model = Profile
        fields = ["name", "pronouns", "bio"]


class ProfilePicturesForm(forms.ModelForm):
    picture = forms.ImageField()
    class Meta:
        model = ProfilePictures
        fields = ["picture"]


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "placeholder": "What's on your mind?"}))
    class Meta:
        model = Post
        fields = ["content"]



