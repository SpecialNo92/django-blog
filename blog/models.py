from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import validate_slug

from .managers import (PostManager, STATUS_PUBLISHED, STATUS_DRAFT)

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, validators=[validate_slug])

    class Meta:
        ordering = ['-name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, validators=[validate_slug])

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_tag_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_DRAFT, 'Draft'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PUBLISHED)
    title = models.CharField(max_length=110)
    slug = models.CharField(max_length=110, validators=[validate_slug],
                            help_text='URL name for post')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="blog_posts")
    category = models.ForeignKey(Category, related_name="blog_posts")
    text = models.TextField()
    image = models.ImageField(upload_to='post',
                              null=True, blank=True,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField("Image height", default=0,
                                       help_text="Not required")
    width_field = models.IntegerField("Image width", default=0,
                                      help_text="Not required")
    tag_list = models.ManyToManyField(Tag, related_name="blog_posts", blank=True)
    date_added = models.DateTimeField(verbose_name='Published', auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-date_added', 'title']
        get_latest_by = 'date_added'


    def __str__(self):
        return self.title

    def get_update_url(self):
        return reverse('blog_post_update', kwargs={'pk': self.pk,'slug': self.slug})

    def get_delete_url(self):
        return reverse('blog_post_delete', kwargs={'pk': self.pk,'slug': self.slug})

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'pk': self.pk,'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="post_comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_comments")
    comment = models.CharField(max_length=255)
    date_added = models.DateTimeField(verbose_name='Date added', auto_now_add=True)
