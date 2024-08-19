from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import BlogPost, Tag, Comment, Reply
from .forms import BlogPostForm, ReplyCreateForm, CommentCreateForm


def home(request):
    return render(request, 'it_blogpost/home.html', )


def blogposts(request, tag=None):
    if tag:
        posts = BlogPost.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = BlogPost.objects.filter(published=True)

    paginator = Paginator(posts, 2)
    page = int(request.GET.get('page', 1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')

    context = {
        'posts': posts,
        'tag': tag,
        'page': page,
    }
    if request.htmx:
        return render(request, 'snippets/loop_blogposts.html', context)

    return render(request, 'it_blogpost/blogposts.html', context)


def blogpost(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    # if request.META.get("HTTP_HX_REQUEST"): (without installing the django_htmx package)

    # with the django_htmx package =>

    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request, 'snippets/loop_postdetail_comments.html', {'comments': comments, 'replyform': replyform})

    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,

    }

    return render(request, 'it_blogpost/post_detail.html', context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(BlogPost, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    context = {
        'comment': comment,
        'post': post,
        'replyform': replyform,
    }
    return render(request, 'snippets/add_comment.html', context)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post-detail', comment.parent_post.slug)
    return render(request, 'it_blogpost/comment_delete.html', {'comment': comment})


@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {'comment': comment,
               'reply': reply,
               'replyform': replyform
               }

    return render(request, 'snippets/add_reply.html', context)


@login_required
def reply_delete(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted')
        return redirect('post-detail', reply.parent_comment.parent_post.slug)
    return render(request, 'it_blogpost/reply_delete.html', {'reply': reply})


@login_required()
def blogpost_create(request):
    form = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post Created')
            return redirect('blogposts')

    return render(request, 'it_blogpost/post_create.html', {'form': form})


@login_required()
def blogpost_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    form = BlogPostForm(instance=post)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Edited')
            return redirect('blogposts')
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'it_blogpost/post_edit.html', context)


@login_required
def blogpost_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('blogposts')
    return render(request, 'it_blogpost/post_delete.html', {'post': post})


# creating a custom decorator for like funtionality
def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()

            if user_exist:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return func(request, post)

        return wrapper

    return inner_func


@login_required
@like_toggle(BlogPost)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post': post})


@login_required
@like_toggle(Comment)
def like_comment(request, post):
    return render(request, 'snippets/likes_comment.html', {'comment': post})


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'snippets/likes_reply.html', {'reply': post})
