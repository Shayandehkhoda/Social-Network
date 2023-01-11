from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'img')

    def clean_title(self):
        title = self.cleaned_data.get("title")
        title_exists = Post.objects.filter(title=title).exists()
        if title_exists:
            raise ValidationError('title exists')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )