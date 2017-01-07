from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

#Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=150, unique=True)
    about = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def get_update_url(self):
        return reverse('user-auth:profile_update')

    def get_absolute_url(self):
        return reverse('user-auth:public_profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.get_username()
