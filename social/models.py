from django.db import models
from accounts.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.template.defaultfilters import slugify


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    slug = models.SlugField()
    img = models.ImageField(upload_to='posts/%Y/%m/%d/',)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def thumbnail(self):
        return format_html(f"<img width=100 height=45 style='border-radius: 5px;' src='{self.img.url}'>")

    def trunc_title(self):
        return self.title[:30] + ' ...'
    trunc_title.short_description = 'Title'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('social:detail', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:20])
        return super().save(*args, **kwargs)

    def like_count(self):
        return self.likepost.count()

    def like_existance(self, user):
        return Like.objects.filter(user=user, post=self).exists()


    class Meta:
        ordering = ('-created',)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likeuser')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likepost')

    def __str__(self):
        return f'{self.user} Liked {self.post.title[:20]}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercm')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postcm')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} on {self.post}'

    class Meta:
        ordering = ('-created',)
