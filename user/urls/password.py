from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from ..views import PasswordResetComplete

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(pattern_name='home', permanent=False)),


    # Urls for password change of registered user
    url(r'^change/$',
        auth_views.password_change,
        {'template_name': 'user/password_change_form.html',
            'post_change_redirect': reverse_lazy('user-auth:password_change_done')},
        name='password_change'),
    url(r'^change/done$',
        auth_views.password_change_done,
        {'template_name': 'user/password_change_done.html'},
        name='password_change_done'),


    # Urls for "forget password" option
    url(r'^reset/$',
        auth_views.password_reset,
        {'template_name': 'user/password_reset_form.html',
         'email_template_name': 'user/password_reset_email_text.txt',
         'subject_template_name': 'user/password_reset_email_title.txt',
         'post_reset_redirect': reverse_lazy('user-auth:password_reset_emailsent')},
        name='password_reset'),
    url(r'reset/emailsent/$',
        auth_views.password_reset_done,
        {'template_name': 'user/password_reset_emailsent.html'},
        name='password_reset_emailsent'),
    url(r'reset/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'user/password_reset_confirm.html',
         'post_reset_redirect': reverse_lazy('user-auth:password_reset_complete')},
        name="password_reset_confirm"),
    url(r'reset/completed',
        PasswordResetComplete.as_view(),
        name="password_reset_complete"),
]
