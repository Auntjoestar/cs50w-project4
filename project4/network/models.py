from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone, dateformat

class User(AbstractUser):
    def __str__(self):
        return self.username

class Profile(models.Model):
    username = models.OneToOneField(User, verbose_name="Username", related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, verbose_name="Name")
    PRONOUNS_CHOICES = [
        ("HH", "He/Him"),
        ("SS", "She/Her"),
        ("TT", "They/Them"),
        ("HT", "He/They"),
        ("ST", "She/They"),
        ("IR", "I rather not to say"),
        ("OT", "Other")
    ]
    pronouns = models.CharField(
        blank=False,
        choices=PRONOUNS_CHOICES,
        max_length=2,
        default=PRONOUNS_CHOICES[5][0],
        verbose_name="Pronouns"
    )
    bio = models.CharField(max_length=160, blank=False, verbose_name="Bio")
    joined = models.DateTimeField(default=timezone.now(), verbose_name="Joined at")
    followers = models.ManyToManyField(User, verbose_name="Followed by", related_name="follower")
    updated_at = models.DateTimeField(default=timezone.now(), verbose_name="Updated at")

    def save(self):
        ''' On save, update timestamps '''
        if not self.id:
            self.joined = timezone.now()
        self.updated_at = timezone.now()
        return super(Profile, self).save()

    def __str__(self):
        return f"{self.name} ({self.username})"
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username.username,
            "name": self.name,
            "pronouns": self.pronouns,
            "bio": self.bio,
            "joined": self.joined.strftime("%d %b %Y"),
            "updated_at": self.updated_at.strftime("%d %b %Y"),
            "following": self.followers.count(),
            "following_list": [follower.username for follower in self.followers.all()],
            "followers": self.username.follower.count(),
        }

class ProfilePictures(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="uploader", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="static/network/profilePictures", verbose_name="File")
    timestamp = models.DateTimeField(default=timezone.now(), verbose_name="Uploaded AT")
    def __str__(self):
        return f"Profile picture of {self.user.username}"
    def serialize(self):
        return {
            "id": self.id,
            "picture":self.picture.url,
            "timestamp": self.timestamp,
        }

class Post(models.Model):
    poster = models.ForeignKey(User, verbose_name="Posted By", related_name="poster", on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=280, blank=False, verbose_name="Content")
    likes = models.ManyToManyField(User, verbose_name="Liked By", related_name="liker")
    views = models.ManyToManyField(User, verbose_name="View By", related_name="viewer")
    postTime = models.DateTimeField(default=timezone.now(), verbose_name="Posted at")
    updateTime = models.DateTimeField(default=timezone.now(), verbose_name="Updated at")

    class Meta:
        ordering = ['-postTime']

    def save(self):
        ''' On save, update timestamps '''
        if not self.id:
            self.postTime = timezone.now()
        self.updateTime = timezone.now()
        return super(Post, self).save()

    def __str__(self):
        return f"Post by {self.poster.username if self.poster else 'Unknown'} at {self.postTime}"
    
    def serialize(self, liker=None):
        if liker is not None:
            liker = User.objects.get(pk=liker)
            if self.likes.filter(pk=liker.id).exists():
                liked = True
            else:
                liked = False
        else:
            liked = False
        return {
            "id": self.id,
            "poster": self.poster.username if self.poster else "Unknown",
            "poster_id": self.poster.id if self.poster else "Unknown",
            "poster_name": self.poster.profile.name if self.poster else "Unknown",
            "poster_picture": self.poster.uploader.picture.url if self.poster.uploader else "Unknown",
            "content": self.content,
            "likes": self.likes.count(),
            "views": self.views.count(),
            "postTime": self.postTime.strftime("%d %b %Y, %I:%M %p") if self.postTime.strftime("%d %b %Y, %I:%M:%S %p")  == self.updateTime.strftime("%d %b %Y, %I:%M:%S %p") else "" if self.postTime else "",
            "updateTime": f"Edited at: {self.updateTime.strftime("%d %b %Y, %I:%M %p")}" if self.postTime.strftime("%d %b %Y, %I:%M:%S %p")  != self.updateTime.strftime("%d %b %Y, %I:%M:%S %p") else "" if self.updateTime else "",
            "datetime": self.postTime if self.postTime.strftime("%Y-%m-%d %H:%M:%S") == self.updateTime.strftime("%Y-%m-%d %H:%M:%S") else self.updateTime,
            "likes": self.likes.count(),
            "liked": liked,
        }





