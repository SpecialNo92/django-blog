from django.conf.urls import url
from ..views.post import (PostList, PostCreate, PostUpdate, PostDelete, PostDetail)

urlpatterns = [
    url(r'^create/$',
        PostCreate.as_view(),
        name='blog_post_create'),
    url(r'^(?P<pk>[\d]+)/'
        r'(?P<slug>[\w\-]+)/$',
        PostDetail.as_view(),
        name="blog_post_detail"),
    url(r'^(?P<pk>[\d]+)/'
        r'(?P<slug>[\w\-]+)/update/$',
        PostUpdate.as_view(),
        name="blog_post_update"),
    url(r'^(?P<pk>[\d]+)/'
        r'(?P<slug>[\w\-]+)/delete/$',
        PostDelete.as_view(),
        name="blog_post_delete"),
    url(r'^$',
        PostList.as_view(),
        name='blog_post_list'),
]