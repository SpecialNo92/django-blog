"""sublog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from blog.urls import (blog as blog_urls, category as category_urls, tag as tag_urls)
from user.urls import user as user_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='blog_post_list', permanent=False), name='home'),
    url(r'^blog/', include(blog_urls)),
    url(r'^user/', include(user_urls, app_name='user', namespace='user-auth')),
    url(r'^category/', include(category_urls)),
    url(r'^tag/', include(tag_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

