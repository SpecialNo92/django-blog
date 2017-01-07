from django.conf.urls import url
from django.views.generic.base import RedirectView

from ..views.category import CategoryDetail

urlpatterns = [
    url(r'^(?P<slug>[\w\-]+)/$',
        CategoryDetail.as_view(),
        name="blog_category_detail"),
    url(r'^$', RedirectView.as_view(pattern_name='home', permanent=False), name='blog_category_list'),
]