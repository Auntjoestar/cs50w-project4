from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    def __str__(self):
        return self.username

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
        blank=False,
        choices=PRONOUNS_CHOICES,
        max_length=2,
        default=PRONOUNS_CHOICES[5][0],
        verbose_name="Pronouns"
    )
    bio = models.CharField(max_length=160, blank=False, verbose_name="Bio")
    joined = models.DateTimeField(default=timezone.now(), verbose_name="Joined at")
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
            "joined": self.joined,
            "updated_at": self.updated_at
        }

class Followers(models.Model):
    user = models.ForeignKey(User, verbose_name="User", related_name="user", on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, verbose_name="Followed By", related_name="follower")
    timestamp = models.DateTimeField(default=timezone.now(), verbose_name="Followed at")

    def __str__(self):
        return f"{self.user.username} is followed by {self.follower.count()} users"

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

class Comments(models.Model):
    commenter = models.ForeignKey(User, verbose_name="Commented By", related_name="Commenter", null=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=280, blank=False, verbose_name="Comment")
    post = models.ForeignKey(Post, verbose_name="Commented On", related_name="commented_post", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, verbose_name="Comment Liked by", related_name="commentliker")
    commentedAt = models.DateTimeField(default=timezone.now(), verbose_name="Posted at")
    updatedAt = models.DateTimeField(default=timezone.now(), verbose_name="Updated at")

    class Meta:
        ordering = ['-commentedAt']

    def save(self):
        ''' On save, update timestamps '''
        if not self.id:
            self.commentedAt = timezone.now()
        self.updatedAt = timezone.now()
        return super(Comments, self).save()

    def __str__(self):
        return f"Comment by {self.commenter.username if self.commenter else 'Unknown'} on {self.post.content[:20]}"

class Reply(models.Model):
    replier = models.ForeignKey(User, verbose_name="Replied by", related_name="replier", null=True, on_delete=models.SET_NULL)
    reply = models.CharField(max_length=280, blank=False, verbose_name="Reply")
    repliedOn = models.ForeignKey(Comments, blank=False, verbose_name="Replied to", on_delete=models.CASCADE)
    repliedAt = models.DateTimeField(default=timezone.now(), verbose_name="Replied at")
    UpdatedAt = models.DateTimeField(default=timezone.now(), verbose_name="Updated at")

    class Meta:
        ordering = ['-repliedAt']

    def save(self):
        ''' On save, update timestamps '''
        if not self.id:
            self.repliedAt = timezone.now()
        self.UpdatedAt = timezone.now()
        return super(Reply, self).save()

    def __str__(self):
        return f"Reply by {self.replier.username if self.replier else 'Unknown'} on {self.repliedOn.comment[:20]}"

class Pictures(models.Model):
    post = models.ForeignKey(Post, verbose_name="Uploaded on", related_name="uploaded", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="static/network/pictures", verbose_name="File")
    timestamp = models.DateTimeField(default=timezone.now(), verbose_name="Uploaded at")

    def __str__(self):
        return f"Picture for post {self.post.id}"

class Hashtags(models.Model):
    post = models.ManyToManyField(Post, verbose_name="Post", related_name="post")
    hashtag = models.CharField(max_length=140, blank=True, verbose_name="Hashtag")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Uploaded at")

    def __str__(self):
        return f"Hashtag: {self.hashtag}"



