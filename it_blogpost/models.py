import uuid

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()


class BlogPost(models.Model):
    IMAGE_MAX_SIZE = (800, 800)

    title = models.CharField(max_length=255, unique=True, verbose_name="title")
    thumbnail = models.ImageField(blank=True, upload_to='blogposts-thumbnails/')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    body = models.TextField()
    tags = models.ManyToManyField('Tag')
    likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    created_on = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False, verbose_name="published")
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-created_on']

    def resize_image(self):
        image = Image.open(self.thumbnail)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # saving the resized image in file system
        # this is not the save() method of the model!
        image.save(self.thumbnail.path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        self.resize_image()

    def get_absolute_url(self):
        return f'/post/{self.slug}/'

    @property
    def author_or_default(self):
        return self.author.username if self.author else "no author"


class LikedPost(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.post.title}'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

    def get_absolute_url(self):
        return f'/category/{self.slug}/'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username}: {self.body[:30]}'
        except:
            return f'no author: {self.body[:30]}'

    class Meta:
        ordering = ['-created']


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username}: {self.body[:30]}'
        except:
            return f'no author: {self.body[:30]}'

    class Meta:
        ordering = ['-created']


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.reply.body[:30]}'
