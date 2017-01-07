from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import send_mail
from django.utils import six
from django.core.exceptions import PermissionDenied

import logging, traceback
from logging import ERROR, CRITICAL
logger = logging.getLogger(__name__)


class RequireNotLogged:
    """
    View will be allowed only for users that are NOT logged in
    """
    user_is_logged_msg = 'You should not perform this action while being logged in'
    redirect_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            messages.warning(request, self.user_is_logged_msg)
            return redirect(self.redirect_url)

        return super(RequireNotLogged, self).dispatch(request, *args, **kwargs)


class RequireAuthenticatedPermission(AccessMixin):
    """
    By default requires only login, unless you specify permission_required
    When user not logged redirect to login, when no permissions redirect to "no_permissions_redirect_url"

    Most important fields:
        permission_required = string/list/tuple of permissions needed to perform action
        raise_exception = Boolean, if user has no permissions raise exception and redirect to 403.html
    """
    raise_exception = False
    login_required_msg = 'Login is required to perform this action'
    permission_denied_msg = 'Permissions denied!'
    permission_required = ''
    no_permissions_redirect_url = reverse_lazy('home')

    def get_permission_required(self):
        if isinstance(self.permission_required, six.string_types):
            perms = (self.permission_required, )
        else:
            perms = self.permission_required
        return perms

    def handle_no_permission(self, request):
        if self.raise_exception:
            raise PermissionDenied(self.permission_denied_msg)

        messages.error(request, self.permission_denied_msg)
        return redirect(self.no_permissions_redirect_url)

    def handle_no_login(self, request):
        messages.warning(request, self.login_required_msg)
        return redirect(self.get_login_url())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            self.handle_no_login(request)

        elif not request.user.has_perms(self.get_permission_required()):
            self.handle_no_permission(request)

        return super(RequireAuthenticatedPermission, self).dispatch(request, *args, **kwargs)


class ActivationMailMixin:
    """
    Will send activation email with send_activation_email method
    send_activation_email(user[REQUIRED], **kwargs[passing request is REQUIRED])
    If email was sent properly, was_email_sent field will be True, if not then it will be false
    If it fails to send activation mail or recieve request it will log error/critical
    You can set-up email template files with:
        email_template_name(text) / subject_template_name(title)
    """
    _mail_sent = False
    email_template_name = 'user/user_register_email_text.txt'
    subject_template_name = 'user/user_register_email_subject.txt'
    send_mail_error_form_msg = 'We could not send you activation link, sorry.'

    @property
    def was_mail_sent(self):
        return self._mail_sent

    @was_mail_sent.setter
    def was_mail_sent(self, value):
        raise TypeError('Cannot set mail_was_sent attribute.')

    def generate_message(self, context):
        return render_to_string(
            self.email_template_name, context)

    def generate_subject(self, context):
        subject = render_to_string(
            self.subject_template_name, context)

        # making subject one line
        subject = ''.join(subject.splitlines())
        return subject

    def generate_email_context(self, request, user, context=None):
        if context is None:
            context = {}
        current_site = get_current_site(request)

        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'

        token = default_token_generator.make_token(user)
        userid = urlsafe_base64_encode(force_bytes(user.pk))
        context.update({
            'domain': current_site.domain,
            'protocol': protocol,
            'site_name': current_site.name,
            'token': token,
            'uid': userid,
            'user': user,
        })
        return context

    def handle_message_sending(self, request, user, **kwargs):
        context = kwargs['context'] = self.generate_email_context(
            request, user)
        mail_data = {
            "subject": self.generate_subject(context),
            "message": self.generate_message(context),
            "from_email": (
                settings.DEFAULT_FROM_EMAIL),
            "recipient_list": [user.email],
        }

        try:
            number_sent = send_mail(**mail_data)
        except Exception as err:
            logger.log(ERROR,
                       'Cant send the activation email, \n'
                       'Exception: {} \n'
                       'mail data : \n {}'.format(err, mail_data))
        else:
            if number_sent > 0:
                return True

        logger.log(CRITICAL, 'Cant send the activation email unknown error, mail data : \n {}'.format(mail_data))
        return False

    def send_activation_email(self, user, **kwargs):
        request = kwargs.pop('request', None)

        if request is None:
            tb = traceback.format_stack()
            tb = [' ' + line for line in tb]
            logger.log(CRITICAL, 'send_activation_email called without request '
                              '\nTraceback:\n {}'.format(''.join(tb)))
            return False

        self._mail_sent = self.handle_message_sending(request, user, **kwargs)

        return self.was_mail_sent














