from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timezone


class User(AbstractUser):
    pass

class Profile(models.Model):
    username = models.OneToOneField(User, verbose_name="Username", on_delete=models.CASCADE)
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
        blank=True,
        choices=PRONOUNS_CHOICES,
        max_length=2,
        default=PRONOUNS_CHOICES[4][1],
        verbose_name="Category"
    )
    bio = models.CharField(max_length=160, blank=False, verbose_name="Bio")
    joined = models.DateTimeField(default=timezone.now(), verbose_name="Joined at")

class Followers(models.Model):
    user = models.ForeignKey(User, verbose_name="User", related_name="user", on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, verbose_name="Followed By", related_name="follower")

class ProfilePictures(models.Model):
    user = models.models.OneToOneField(User, verbose_name="User", related_name="uploader", on_delete=models.CASCADE)
    picture = models.FileField(upload_to="static/network/profilePictures",verbose_name="File")

class Post(models.Model):
    poster = models.ForeignKey(User, verbose_name="Posted By", related_name="poster", on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=280, blank=False, verbose_name="Content")
    likes = models.ManyToManyField(User, verbose_name="Liked By", related_name="liker",)
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
        return super(User, self).save()


class Comments(models.Model):
    commenter = models.ForeignKey(User, verbose_name="Commented By", related_name="Commenter", on_delete=models.SET_NULL)
    comment = models.models.CharField(max_lenght=280, blank=False, verbose_name="Comment")
    post = models.ForeignKey(Post, verbose_name="Commented On", related_name="commented_post", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, verbose_name="Liked by", related_name="liker")
    commentedAt = models.DateTimeField(default=timezone.now(), verbose_name="Posted at")
    updatedAt =  models.DateTimeField(default=timezone.now(), verbose_name="Updated at")
    class Meta:
        ordering = ['-commentedAt']

class Reply(models.Model):
    replier = models.ForeignKey(User, verbose_name="Replied by", related_name="replier", on_delete=models.SET_NULL)
    reply = models.CharField(max_length=280, blank=False, verbose_name="Reply")
    repliedOn = models.ForeignKey(Comments, blank=False, verbose_name="Replied to", on_delete=models.CASCADE)
    repliedAt = models.DateTimeField(default=timezone.now(), verbose_name="Replied at")
    UpdatedAt= models.DateTimeField(default=timezone.now(), verbose_name="Updated at")
    class Meta:
        ordering = ['-repliedAt']

class Pictures(models.Model):
    post = models.ForeignKey(Post, verbose_name="Uploaded on", related_name="uploaded", on_delete=models.CASCADE)
    picture = models.ForeignKey(upload_to="static/network/pictures", verbose_name="File")


class hashtags(models.Model):
    post = models.ManyToManyField(Post, verbose_name="Post", related_name="post")
    hashtag = models.CharField(max_length=140, blank=True, verbose_name="Hashtag")



