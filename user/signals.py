from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save


@receiver(user_logged_in)
def display_login_message(sender, **kwargs):
    """
    Creates message after login
    """
    request = kwargs.get('request')
    messages.success(request, 'Successfully logged in', fail_silently=True)


@receiver(user_logged_out)
def display_logout_message(sender, **kwargs):
    """
    Creates message after logout
    """
    request = kwargs.get('request')
    messages.success(request, 'Successfully logged out',fail_silently=True)
