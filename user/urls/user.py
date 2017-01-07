from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from ..views import (AccountActivate, AccountRegister,
                     ProfileDetail, ProfileUpdate,
                     PublicProfileDetail, ResendActivationEmail)

from . import password as password_urls


urlpatterns = [
    url(r'^$',
        RedirectView.as_view(pattern_name='user-auth:login',
                             permanent=False)),

    url(r'login/$',
        auth_views.login,
        {'template_name': 'user/login.html',
         'redirect_authenticated_user': True},
         name='login'),
    url(r'logout/$',
        auth_views.logout,
        {'next_page': reverse_lazy('user-auth:login')},
        name='logout'),
    url(r'register/$',
        AccountRegister.as_view(),
        name='register'),
    url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        AccountActivate.as_view(),
        name='activate'),
    url(r'^activate/resend/$',
        ResendActivationEmail.as_view(),
        name='activate_resend'),

    url(r'profile/update/$',
        ProfileUpdate.as_view(),
        name='profile_update'),
    url(r'profile/$',
        ProfileDetail.as_view(),
        name='profile'),
    url(r'profile/'
        r'(?P<slug>[\w\-]+)/$',
        PublicProfileDetail.as_view(),
        name='public_profile'),

    url(r'password/',
        include(password_urls)),
]
