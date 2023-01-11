from django import template
from social.models import Post

register = template.Library()


@register.inclusion_tag('social/inc/widget-latestpost.html')
def latest_post():
    latest_posts = Post.objects.all()
    return {'latest_posts': latest_posts}

