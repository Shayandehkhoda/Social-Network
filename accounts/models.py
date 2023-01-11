from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.shortcuts import get_object_or_404

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    img = models.ImageField(upload_to='profile-pic', default='default.jpg')
    bio = models.TextField(default='No bio available')

    def img_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.img.url))
    img_tag.short_description = 'thumbnail'


class FollowRelation(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} followed {self.followed}'
