from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .utils import ActivationMailMixin
from .models import Profile
from blog.models import Comment


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about', 'location', 'birth_date')


class CustomUserCreationForm(ActivationMailMixin, UserCreationForm):
    """
    Requires user to define his username, email and password1, password2
    If user is registered successfully, creates empty Profile for him,
        and sends activation email or log error
    """
    UserModel = get_user_model()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']

        disallowed_usernames = {'activate', 'api', 'blog', 'change', 'category', 'error', 'create', 'delete',
                                'detail', 'form', 'login', 'logout', 'password', 'profile', 'update', 'user',
                                'tag', 'register', 'secure', 'success', 'www'}

        if username in disallowed_usernames:
            raise ValidationError("This Username is illegal, please choose something different")

        return username

    def save(self, **kwargs):
        user = super().save(commit=False)

        if not user.pk:
            user.is_active = False

        user.save()
        self.save_m2m()

        Profile.objects.update_or_create(
            user=user,
            defaults={
                'slug': slugify(user.get_username())
            })

        self.send_activation_email(user=user, **kwargs)

        return user


class ResendActivationEmailForm(ActivationMailMixin, forms.Form):
    """
    If email exists then resend activation mail
    """
    email = forms.EmailField()
    send_mail_error_form_msg = 'We could not re-send you activation link, sorry.'
    UserModel = get_user_model()

    def clean(self):
        try:
            get_user = self.UserModel.objects.get(email=self.cleaned_data['email'])
        except self.UserModel.DoesNotExist as err:
            raise ValidationError("There is no such a user")

        if get_user.is_active is True:
            raise ValidationError("This user is already activated")

        # Saving the user so we don't have to fetch it again from db
        self.cleaned_data['user'] = get_user

    def save(self, **kwargs):
        user = self.cleaned_data['user']
        self.send_activation_email(user, **kwargs)

        return user


