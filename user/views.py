from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, DetailView, UpdateView
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (get_user_model, get_user, logout, login, authenticate)
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (CustomUserCreationForm, ResendActivationEmailForm, ProfileForm, UserForm)
from .utils import (ActivationMailMixin, RequireNotLogged, RequireAuthenticatedPermission)
from .models import Profile

# Create your views here.


class AccountRegister(RequireNotLogged, View):
    """
    View responsible for handling user registration
    """
    template_name = 'user/user_register.html'
    form_class = CustomUserCreationForm
    after_registered_redirect = reverse_lazy('user-auth:activate_resend')
    success_msg = ('You have successfully created an account, but we '
                   'need to confirm your e-mail. Please check your inbox')
    registered_but_failed_msg = ('You are successfully registered but we had '
                                 'problems with sending you activation email, '
                                 'please try to resend activation link')

    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)

        if bound_form.is_valid():
            bound_form.save(**{'request': request})

            if bound_form.was_mail_sent:
                messages.info(request, self.success_msg)
            else:
                messages.error(request, self.registered_but_failed_msg)

            return redirect(self.after_registered_redirect)

        return TemplateResponse(request, self.template_name, {'form': bound_form})


class AccountActivate(RequireNotLogged, ActivationMailMixin, View):
    """
    Checks if activation link is correct, if so then activate user
    If user is already activated just redirect to login
    """
    failure_redirect_url = reverse_lazy('user-auth:activate_resend')
    success_url = reverse_lazy('user-auth:login')
    success_msg = 'User successfully activated!, you can login now!'
    error_msg = 'Unfortunately, we could not activate your account, please try resend link again'

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        UserModel = get_user_model()

        try:
            userid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=userid)
        except:
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            messages.error(request. self.error_msg)
            return redirect(self.failure_redirect_url)

        user.is_active = True
        user.save()
        messages.success(request, self.success_msg)

        return redirect(self.success_url)


class ProfileDetail(LoginRequiredMixin, DetailView):
    template_name = 'user/profile_detail.html'
    model = Profile

    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user.profile


class ProfileUpdate(LoginRequiredMixin, View):
    """
    Allows user to update two forms at same time, some fields of User model and Profile model
    """
    template_name = 'user/profile_form_update.html'
    profile_form = ProfileForm
    user_form = UserForm
    success_url = reverse_lazy('user-auth:profile')
    success_msg = 'Successfully updated profile'

    def get(self, request):
        user = get_user(request)
        context = {
            'user_form': self.user_form(instance=user),
            'profile_form': self.profile_form(instance=user.profile)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        bound_user_form = self.user_form(request.POST, instance=request.user)
        bound_profile_form = self.profile_form(request.POST, instance=request.user.profile)

        if bound_profile_form.is_valid() and bound_profile_form.is_valid():
            bound_profile_form.save()
            bound_user_form.save()
            messages.success(request, self.success_msg)
            return redirect(self.success_url)


class PublicProfileDetail(DetailView):
    template_name = 'user/public_profile_detail.html'
    model = Profile


class ResendActivationEmail(RequireNotLogged, View):
    """
    If email is correct, resend activation link and create message
    """
    template_name = 'user/user_resend_activation.html'
    form_class = ResendActivationEmailForm
    success_msg = 'Successfully send you an e-mail, Please check your inbox'
    error_msg = 'We could not resend you activation email'

    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)

        if bound_form.is_valid():
            user = bound_form.save(**{'request': request})
            if user is not None and bound_form.was_mail_sent:
                messages.success(request, self.success_msg)
            else:
                messages.error(request, self.error_msg)

        return TemplateResponse(request, self.template_name, {'form': bound_form})


class PasswordResetComplete(View):
    """
    If password is successfully change create message and redirect
    """
    success_msg = 'Your password was successfully changed, you can login now'
    redirect_url = reverse_lazy('user-auth:login')

    def get(self, request):
        messages.success(request, self.success_msg)
        return redirect(self.redirect_url)























