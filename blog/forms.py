from django.forms import ModelForm
from django.utils.text import slugify
from django.contrib.auth import get_user
from django.core.exceptions import ValidationError
from django.conf import settings

# from django.conf import settings

from .models import Post, Comment


class PostForm(ModelForm):
    """
    Form for post with generated slug from title
    """
    class Meta:
        model = Post
        fields = ['status', 'title', 'image', 'text', 'category', 'tag_list']

    def save(self, *args, **kwargs):
        post = super().save(commit=False)

        if not post.pk:
            request = kwargs.get('request')
            post.author = get_user(request)

        post.slug = slugify(post.title)

        post.save()
        self.save_m2m()

        return post


class CommentForm(ModelForm):
    """
    Form for comments of the post, save method needs to
    """
    class Meta:
        model = Comment
        fields = ['comment']

    def save(self, *args, **kwargs):
        comment = super().save(commit=False)
        request = kwargs.get('request')
        post_pk = kwargs.get('post_pk')

        comment.author = get_user(request)

        post_object = Post.objects.get(pk=post_pk)
        comment.post = post_object

        comment.save()
        self.save_m2m()

        return comment
