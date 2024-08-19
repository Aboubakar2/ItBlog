from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    LogoutView, PasswordResetCompleteView
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from it_blogpost.forms import ReplyCreateForm
from . import forms

User = get_user_model()


class LoginViewPage(LoginView):
    template_name = 'it_users/auth/login.html'


class PasswordReset(PasswordResetView):
    template_name = 'it_users/auth/pass_reset.html'
    email_template_name = 'it_users/auth/pass_reset_email.html'
    success_url = reverse_lazy("pass-reset-done")


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'it_users/auth/pass_reset_confirm.html'
    success_url = reverse_lazy("pass-reset-complete")


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'it_users/auth/pass_reset_done.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'it_users/auth/pass_reset_complete.html'


# class Logout(LogoutView):
#     http_method_names = ['post', 'options']
#     template_name = 'it_users/auth/logout.html'


def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully  Logged Out')
    return redirect('home')


def signup(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile-onboarding')
    return render(request, 'it_users/auth/signup.html', {'form': form})


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    posts = profile.user.posts.all()

    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=1).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=1).order_by(
                '-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html',
                          {'comments': comments, 'replyform': replyform})
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created')
        return render(request, 'snippets/loop_profile_posts.html', {'posts': posts})

    context = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'it_users/profile/profile.html', context)


def profile_edit(request):
    form = forms.ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-onboarding'):
        template = 'it_users/profile/profile_onboarding.html'
    else:
        template = 'it_users/profile/profile_edit.html'
    return render(request, template, {'form': form})
