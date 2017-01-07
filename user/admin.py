from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'slug')
    list_display = ('user', 'slug')

admin.site.register(Permission)
admin.site.register(Profile, ProfileAdmin)