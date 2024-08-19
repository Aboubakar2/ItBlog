from django import forms

from .models import BlogPost, Reply, Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['thumbnail', 'title', 'body', 'tags']
        labels = {
            'body': 'Content',
            'tags': 'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Add a content ...', 'class': '  text-2xl'}),
            'thumbnail': forms.FileInput(),
            'tags': forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add comment ...'})
        }
        labels = {
            'body': ''
        }


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add reply ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
        }
