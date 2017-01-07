from django.conf.urls import url
from django.views.generic.base import RedirectView

from ..views.tag import TagDetail


urlpatterns = [
    url(r'^(?P<slug>[\w\-]+)/$',
        TagDetail.as_view(),
        name="blog_tag_detail"),
    url(r'^$', RedirectView.as_view(pattern_name='home', permanent=False), name='blog_tag_list'),
]