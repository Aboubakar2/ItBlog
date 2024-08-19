from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


"""Here I'm creating my own User Model inherit from AbstractUser to be able to scale
 up my user model as the project  grow up or as needed"""


class User(AbstractUser):
    pass


# this is the profile Model
class Profile(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='avatars/')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    realname = models.CharField(unique=True, max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, )
    bio = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar_default.svg')
        return avatar

    @property
    def name(self):
        if self.realname:
            name = self.realname

        else:
            name = self.user.username
        return name
