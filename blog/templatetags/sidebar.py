from django import template

from ..models import (Category, Tag)

register = template.Library()


@register.inclusion_tag('blog/includes/sidebar_category_list.html', takes_context=True)
def get_category_list(context):
    """
    Return published categories
    """
    return { 'category_list': Category.objects.all() }

@register.inclusion_tag('blog/includes/sidebar_tag_list.html', takes_context=True)
def get_tag_list(context):
    """
    Return published tags
    """
    return { 'tag_list': Tag.objects.all() }