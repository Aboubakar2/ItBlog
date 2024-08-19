from django.db.models import Count
from django.template import Library

from it_blogpost.models import Tag, BlogPost

register = Library()


@register.inclusion_tag('includes/sidebar.html')
def sidebar_view(tag=None, user=None):
    categories = Tag.objects.all()
    top_posts = BlogPost.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=1).order_by('-num_likes')
    context = {
        'categories': categories,
        'tag': tag,
        'top_posts': top_posts,
        'user': user,
    }
    return context


