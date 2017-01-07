from django.contrib import admin

# Register your models here.
from .models import Category, Comment, Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_added')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'text')
    raw_id_fields = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date_added',)
    search_fields = ('comment', 'author')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
